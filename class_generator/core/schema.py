"""Schema management functions for resource definitions."""

import json
import re
import shlex
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from packaging.version import Version
from pyhelper_utils.shell import run_command
from simple_logger.logger import get_logger

from class_generator.constants import DEFINITIONS_FILE, RESOURCES_MAPPING_FILE, SCHEMA_DIR
from ocp_resources.utils.archive_utils import save_json_archive
from ocp_resources.utils.schema_validator import SchemaValidator

LOGGER = get_logger(name=__name__)


class ClusterVersionError(Exception):
    """Raised when there are issues with cluster version operations."""

    pass


def get_client_binary() -> str:
    """Determine whether to use 'oc' or 'kubectl' binary."""
    # Check if 'oc' binary exists
    if run_command(command=shlex.split("which oc"), check=False)[0]:
        return "oc"

    # Fall back to kubectl
    if run_command(command=shlex.split("which kubectl"), check=False)[0]:
        return "kubectl"

    raise RuntimeError("Neither 'oc' nor 'kubectl' binary found in PATH")


def read_resources_mapping_file(skip_cache: bool = False) -> dict[Any, Any]:
    """Read resources mapping using SchemaValidator for consistency"""
    # Use SchemaValidator to load and get mappings data
    if SchemaValidator.load_mappings_data(skip_cache=skip_cache):
        mappings = SchemaValidator.get_mappings_data(skip_cache=skip_cache)
        if mappings is not None:
            return mappings

    # If we couldn't load the file, return empty dict
    return {}


def extract_group_kind_version(kind_schema: dict[str, Any]) -> dict[str, str]:
    """Extract group, kind, and version from schema.

    Args:
        kind_schema: Schema dictionary containing Kubernetes metadata

    Returns:
        dict: Dictionary with group, kind, and version information

    Raises:
        KeyError: If required x-kubernetes-group-version-kind key is missing
        ValueError: If x-kubernetes-group-version-kind list is empty
    """
    if "x-kubernetes-group-version-kind" not in kind_schema:
        raise KeyError(
            "Required key 'x-kubernetes-group-version-kind' not found in schema. "
            f"Available keys: {list(kind_schema.keys())}"
        )

    group_kind_versions: list[dict[str, str]] = kind_schema["x-kubernetes-group-version-kind"]

    if not group_kind_versions:
        raise ValueError("x-kubernetes-group-version-kind list is empty")

    group_kind_version = group_kind_versions[0]

    for group_kind_version in group_kind_versions:
        if group_kind_version.get("group"):
            break

    return group_kind_version


def get_server_version(client: str) -> str:
    """Get the server version from the cluster."""
    rc, out, _ = run_command(command=shlex.split(f"{client} version -o json"), check=False)
    if not rc:
        error_msg = "Failed to get server version"
        LOGGER.error(error_msg)
        raise RuntimeError(error_msg)

    jout = json.loads(out)
    server_version = jout["serverVersion"]["gitVersion"]
    LOGGER.info(f"Server version: {server_version}")
    return server_version


def build_namespacing_dict(client: str) -> dict[str, bool]:
    """Build a dictionary of resource kinds and their namespaced status"""
    namespacing_dict = {}

    # Process both namespaced and cluster-scoped resources
    for namespaced in [True, False]:
        cmd = f"{client} api-resources --namespaced={str(namespaced).lower()} --no-headers"
        success, output, _ = run_command(command=shlex.split(cmd), check=False, log_errors=False)
        if success and output:
            for line in output.strip().split("\n"):
                # Split and filter out empty strings
                parts = [p for p in line.split() if p]
                if parts:
                    kind = parts[-1]  # KIND is the last column
                    namespacing_dict[kind] = namespaced

    LOGGER.info(f"Built namespacing dictionary with {len(namespacing_dict)} resources")
    return namespacing_dict


def check_and_update_cluster_version(client: str) -> bool:
    """
    Check and update the cluster version file.

    Args:
        client: Path to kubectl/oc client binary

    Returns:
        bool: True if version is same or newer, False otherwise

    Raises:
        ClusterVersionError: If cluster version file cannot be read
    """
    cluster_version_file = Path("class_generator/schema/__cluster_version__.txt")
    last_cluster_version_generated: str = ""

    try:
        with open(cluster_version_file, "r") as fd:
            last_cluster_version_generated = fd.read().strip()
    except (FileNotFoundError, IOError) as exp:
        error_msg = f"Failed to read cluster version file: {exp}"
        LOGGER.error(error_msg)
        raise ClusterVersionError(error_msg) from exp

    cluster_version = get_server_version(client=client)
    cluster_version = cluster_version.split("+")[0]

    same_or_newer_version: bool = Version(cluster_version) >= Version(last_cluster_version_generated)

    if same_or_newer_version:
        with open(cluster_version_file, "w") as fd:
            fd.write(cluster_version)

    return same_or_newer_version


def fetch_all_api_schemas(client: str, paths: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Fetch all API schemas from the cluster in parallel.

    Args:
        client: Path to kubectl/oc client binary
        paths: Dictionary of API paths from v3 index

    Returns:
        dict: Mapping of API path to schema data
    """
    schemas: dict[str, dict[str, Any]] = {}

    # Function to fetch and process a single API group
    def fetch_api_group(api_path: str, api_info: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
        api_url = api_info.get("serverRelativeURL", "")
        if not api_url:
            return api_path, None

        LOGGER.info(f"Processing {api_path}...")
        success, schema_data, _ = run_command(command=shlex.split(f"{client} get --raw {api_url}"), check=False)

        if not success:
            LOGGER.warning(f"Failed to fetch schema for {api_path}")
            return api_path, None

        try:
            schema = json.loads(schema_data)
            return api_path, schema
        except json.JSONDecodeError as e:
            LOGGER.warning(f"Failed to parse schema for {api_path}: {e}")
            return api_path, None

    # Use ThreadPoolExecutor to parallelize API fetching
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all fetch tasks
        future_to_path = {
            executor.submit(fetch_api_group, api_path, api_info): api_path for api_path, api_info in paths.items()
        }

        # Process results as they complete
        for future in as_completed(future_to_path):
            api_path, schema = future.result()
            if schema:
                schemas[api_path] = schema

    return schemas


def process_schema_definitions(
    schemas: dict[str, dict[str, Any]],
    namespacing_dict: dict[str, bool],
    existing_resources_mapping: dict[str, Any],
    allow_updates: bool = True,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Process schema definitions to extract resource information.

    Args:
        schemas: Dictionary of API schemas
        namespacing_dict: Dictionary of resource namespacing info
        existing_resources_mapping: Existing resources mapping
        allow_updates: Whether to update existing resources or only add new ones

    Returns:
        tuple: (resources_mapping, definitions)
    """
    # Start with ALL existing resources (NEVER DELETE)
    resources_mapping = existing_resources_mapping.copy()
    existing_count = len(resources_mapping)
    LOGGER.info(f"Starting with {existing_count} existing resource types - preserving all")

    definitions = {}
    processed_schemas = set()
    total_schemas = 0
    new_resources = 0
    updated_resources = 0

    for api_path, schema in schemas.items():
        # Process schema definitions
        for def_name, def_data in schema.get("components", {}).get("schemas", {}).items():
            if def_name in processed_schemas:
                continue

            processed_schemas.add(def_name)

            # Extract schema info
            gvk_list = def_data.get("x-kubernetes-group-version-kind", [])
            if not gvk_list:
                continue

            # Get the proper GVK
            group_kind_version = gvk_list[0]
            for gvk in gvk_list:
                if gvk.get("group"):
                    group_kind_version = gvk
                    break

            kind = group_kind_version.get("kind", "")
            group = group_kind_version.get("group", "")
            version = group_kind_version.get("version", "")

            if not kind:
                continue

            # Determine if resource is namespaced
            is_namespaced = namespacing_dict.get(kind, True)

            # Build schema name
            if group:
                schema_name = f"{group}/{version}/{kind}"
            else:
                schema_name = f"{version}/{kind}"

            # Create schema data in the format expected by SchemaValidator
            schema_data = {
                "description": def_data.get("description", ""),
                "properties": def_data.get("properties", {}),
                "required": def_data.get("required", []),
                "type": def_data.get("type", "object"),
                "x-kubernetes-group-version-kind": [group_kind_version],
                "namespaced": is_namespaced,
            }

            # Store in resources_mapping as an array (multiple schemas per kind)
            kind_lower = kind.lower()
            if kind_lower not in resources_mapping:
                # NEW resource - always add
                resources_mapping[kind_lower] = [schema_data]
                new_resources += 1
                LOGGER.debug(f"Added new resource: {kind_lower}")
            elif allow_updates:
                # UPDATE existing resource - replace schema with same group/version or add new one
                existing_schemas = resources_mapping[kind_lower]
                updated = False

                for i, existing_schema in enumerate(existing_schemas):
                    existing_gvk = existing_schema.get("x-kubernetes-group-version-kind", [{}])[0]
                    new_gvk = group_kind_version

                    # Check if this is the same group/version combination
                    if existing_gvk.get("group") == new_gvk.get("group") and existing_gvk.get("version") == new_gvk.get(
                        "version"
                    ):
                        # UPDATE: Replace existing schema with newer version
                        existing_schemas[i] = schema_data
                        updated = True
                        updated_resources += 1
                        LOGGER.debug(
                            f"Updated existing resource schema: {kind_lower} ({new_gvk.get('group', 'core')}/{new_gvk.get('version')})"
                        )
                        break

                if not updated:
                    # ADD: New group/version for existing resource kind
                    existing_schemas.append(schema_data)
                    updated_resources += 1
                    LOGGER.debug(
                        f"Added new schema version for existing resource: {kind_lower} ({group_kind_version.get('group', 'core')}/{group_kind_version.get('version')})"
                    )
            else:
                # Don't update existing resources when cluster version is older
                LOGGER.debug(f"Skipping update for existing resource: {kind_lower}")
                continue

            # Also store in definitions for separate definitions file
            definitions[schema_name] = schema_data
            total_schemas += 1

    final_count = len(resources_mapping)
    LOGGER.info("Schema processing complete:")
    LOGGER.info(f"  - Started with: {existing_count} resource types")
    LOGGER.info(f"  - Added new: {new_resources} resource types")
    LOGGER.info(f"  - Updated: {updated_resources} resource schemas")
    LOGGER.info(f"  - Final total: {final_count} resource types")
    LOGGER.info(f"  - Processed: {total_schemas} unique schemas")
    LOGGER.info("  - NEVER DELETED any existing resources")

    return resources_mapping, definitions


def _parse_oc_explain_output(output: str) -> dict[str, Any]:
    """
    Parse oc explain output to extract field information, descriptions, and required fields.
    Clean up descriptions to remove technical artifacts and make them human-readable.
    """
    lines = output.strip().split("\n")
    schema = {"type": "object", "properties": {}, "required": []}

    # Find the FIELDS section
    fields_start = -1
    for i, line in enumerate(lines):
        if line.strip() == "FIELDS:":
            fields_start = i + 1
            break

    if fields_start == -1:
        LOGGER.debug("No FIELDS section found in explain output")
        return schema

    # Parse fields starting from FIELDS section
    fields_lines = lines[fields_start:]
    properties: dict[str, Any] = {}
    required_fields: list[str] = []

    current_field: dict[str, Any] | None = None
    current_description_lines: list[str] = []

    i = 0
    while i < len(fields_lines):
        line = fields_lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Check if this is a field definition line (starts with 2 spaces, not 4 or more)
        if line.startswith("  ") and not line.startswith("    "):
            # Save previous field if we have one
            if current_field:
                field_schema = _convert_type_to_schema(current_field["type"])
                if current_description_lines:
                    description = _clean_description(current_description_lines)
                    if description:
                        field_schema["description"] = description
                properties[current_field["name"]] = field_schema

                if current_field["required"]:
                    required_fields.append(current_field["name"])

            # Parse new field - handle both tab-separated and space-separated formats
            stripped = line.strip()

            # Try tab-separated format first
            if "\t" in stripped:
                field_name = stripped.split("\t")[0].strip()
                type_and_flags = stripped.split("\t", 1)[1].strip()
            # Handle space-separated format as fallback
            elif " " in stripped and ("<" in stripped and ">" in stripped):
                parts = stripped.split(None, 1)  # Split on whitespace, max 1 split
                if len(parts) >= 2:
                    field_name = parts[0].strip()
                    type_and_flags = parts[1].strip()
                else:
                    # Skip malformed lines
                    i += 1
                    continue
            else:
                # Skip lines without proper field format
                i += 1
                continue

            # Check if field is marked as required (ends with " -required-")
            is_required = type_and_flags.endswith(" -required-")
            if is_required:
                # Remove the " -required-" suffix before extracting type
                type_and_flags = type_and_flags[:-11].strip()
            else:
                # Also check for the format "<type> -required-" within the string
                if " -required-" in type_and_flags:
                    is_required = True
                    type_and_flags = type_and_flags.replace(" -required-", "").strip()

            # Extract type from <type> format
            if "<" in type_and_flags and ">" in type_and_flags:
                type_part = type_and_flags.split("<")[1].split(">")[0].strip()
            else:
                type_part = type_and_flags.strip()

            current_field = {"name": str(field_name), "type": str(type_part), "required": is_required}
            current_description_lines = []

        # Check if this is a description line (starts with 4 or more spaces)
        elif line.startswith("    ") and current_field:
            # This is a description line for the current field
            description_text = line.strip()
            if description_text and not description_text.startswith("Possible enum values:"):
                current_description_lines.append(description_text)

        i += 1

    # Don't forget the last field
    if current_field:
        field_schema = _convert_type_to_schema(current_field["type"])
        if current_description_lines:
            description = _clean_description(current_description_lines)
            if description:
                field_schema["description"] = description
        properties[current_field["name"]] = field_schema

        if current_field["required"]:
            required_fields.append(current_field["name"])

    schema["properties"] = properties
    schema["required"] = required_fields
    return schema


def _clean_description(description_lines: list[str]) -> str:
    """
    Clean up description lines to extract meaningful text and remove technical artifacts.

    Args:
        description_lines: List of description lines from explain output

    Returns:
        Clean, human-readable description string
    """
    if not description_lines:
        return ""

    # Join all lines into a single text block
    full_text = " ".join(description_lines).strip()

    # Remove "Possible enum values:" sections and everything after (including bullet points)
    enum_pattern = r"\s*Possible enum values:.*$"
    full_text = re.sub(enum_pattern, "", full_text, flags=re.DOTALL)

    # Remove bullet point enum descriptions that start with "- `"
    bullet_pattern = r"\s*-\s*`[^`]*`.*?(?=\s*-\s*`|$)"
    full_text = re.sub(bullet_pattern, "", full_text, flags=re.DOTALL)

    # Remove common technical patterns and artifacts
    # Remove patterns like "<string> -required-", "<[]string>", etc.
    full_text = re.sub(r"<[^>]*>\s*-?(?:required|optional)?-?\s*", "", full_text)

    # Remove technical markers like "-required-", "-optional-"
    full_text = re.sub(r"\s*-(?:required|optional)-\s*", " ", full_text)

    # Remove multiple consecutive spaces and clean up
    full_text = re.sub(r"\s+", " ", full_text).strip()

    # Remove leading/trailing punctuation artifacts
    full_text = full_text.strip(".,;:- ")

    # If the description is too short or just technical info, return empty
    if len(full_text) < 10 or full_text.lower() in ["no description", "description not available"]:
        return ""

    # Ensure the description ends with a period for consistency
    if full_text and not full_text.endswith("."):
        full_text += "."

    return full_text


def _convert_type_to_schema(type_info: str) -> dict[str, Any]:
    """Convert oc explain type information to JSON schema format."""
    if not type_info:
        return {"type": "object"}

    # Handle array types
    if type_info.startswith("[]"):
        item_type = type_info[2:]
        return {"type": "array", "items": _convert_type_to_schema(item_type)}

    # Handle map types
    if type_info.startswith("map["):
        match = re.match(r"map\[(.+?)\](.+)", type_info)
        if match:
            return {"type": "object"}

    # Handle basic types
    type_mapping = {"integer": "integer", "string": "string", "boolean": "boolean", "number": "number"}

    if type_info in type_mapping:
        return {"type": type_mapping[type_info]}

    # Everything else is treated as an object
    return {"type": "object"}


def _detect_missing_refs_from_schemas(schemas: dict[str, dict[str, Any]], definitions: dict[str, Any]) -> set[str]:
    """
    Analyze schemas to detect missing $ref definitions dynamically.

    Args:
        schemas: All fetched API schemas
        definitions: Current definitions dictionary

    Returns:
        Set of missing reference names that need to be fetched
    """
    missing_refs = set()

    def find_refs_in_schema(schema_data: dict[str, Any]) -> None:
        """Recursively find all $ref references in a schema."""
        if isinstance(schema_data, dict):
            if "$ref" in schema_data:
                ref_path = schema_data["$ref"]
                # Ensure ref_path is a string
                if isinstance(ref_path, str):
                    # Extract reference name from paths like:
                    # "#/definitions/io.k8s.api.core.v1.PodSpec" or "#/components/schemas/..."
                    ref_name = ref_path.split("/")[-1]

                    # Check if this ref exists in definitions with various key formats
                    possible_keys = [
                        ref_name,  # io.k8s.api.core.v1.PodSpec
                        ref_name.split(".")[-1],  # PodSpec
                        "/".join(ref_name.split(".")[-2:]) if "." in ref_name else ref_name,  # v1/PodSpec
                    ]

                    exists = any(key in definitions for key in possible_keys)
                    if not exists:
                        missing_refs.add(ref_name)

            # Recursively check nested structures
            for value in schema_data.values():
                find_refs_in_schema(value)
        elif isinstance(schema_data, list):
            for item in schema_data:
                find_refs_in_schema(item)

    # Analyze all schemas to find missing refs
    for api_path, schema in schemas.items():
        find_refs_in_schema(schema)

    LOGGER.info(f"Detected {len(missing_refs)} missing $ref definitions: {sorted(missing_refs)}")
    return missing_refs


def _infer_oc_explain_path(ref_name: str) -> str | None:
    """
    Infer oc explain path from a reference name.

    Args:
        ref_name: Reference name like "io.k8s.api.core.v1.PodSpec"

    Returns:
        oc explain path or None if can't be inferred
    """
    # Handle common patterns in Kubernetes API references
    if not ref_name.startswith("io.k8s."):
        return None

    # Split the reference to extract components
    parts = ref_name.split(".")
    if len(parts) < 4:
        return None

    # Extract the type name (last part)
    type_name = parts[-1]

    # Try to infer resource and field from type name
    if type_name.endswith("Spec"):
        resource_base = type_name[:-4].lower()  # Remove "Spec"
        field = "spec"
    elif type_name.endswith("Status"):
        resource_base = type_name[:-6].lower()  # Remove "Status"
        field = "status"
    elif type_name == "ObjectMeta":
        # ObjectMeta can be found under any resource's metadata
        return "pod.metadata"
    elif type_name == "LabelSelector":
        # LabelSelector is commonly found in deployment spec
        return "deployment.spec.selector"
    else:
        # For other types, try to infer from API path
        api_parts = parts[2:-1]  # Skip "io.k8s" and type name

        # Handle common patterns
        if "core" in api_parts and "v1" in api_parts:
            # Core API types
            if type_name in ["Container", "EnvVar", "VolumeMount", "ResourceRequirements", "SecurityContext"]:
                return "pod.spec.containers"
            elif type_name in ["Volume", "ConfigMapVolumeSource", "SecretVolumeSource"]:
                return "pod.spec.volumes"
            elif type_name == "ContainerPort":
                return "pod.spec.containers.ports"

        # Can't reliably infer path for this type
        return None

    # Map common resource bases to their actual resource names
    resource_mapping = {
        "pod": "pod",
        "deployment": "deployment",
        "service": "service",
        "configmap": "configmap",
        "secret": "secret",  # pragma: allowlist secret
        "replicaset": "replicaset",
        "daemonset": "daemonset",
        "statefulset": "statefulset",
        "job": "job",
        "cronjob": "cronjob",
        "ingress": "ingress",
        "networkpolicy": "networkpolicy",
        "persistentvolume": "persistentvolume",
        "persistentvolumeclaim": "persistentvolumeclaim",
        "serviceaccount": "serviceaccount",
    }

    resource_name = resource_mapping.get(resource_base)
    if resource_name:
        return f"{resource_name}.{field}"

    return None


def _supplement_schema_with_field_descriptions(definitions: dict[str, Any], client: str) -> dict[str, Any]:
    """
    Supplement existing definitions with field descriptions and required field information from explain.

    Args:
        definitions: Current definitions dictionary
        client: oc/kubectl client binary path

    Returns:
        Dictionary with supplemented field descriptions and required field information
    """
    # Core resource types that commonly have missing descriptions
    critical_specs = [
        ("io.k8s.api.core.v1.PodSpec", "pod.spec"),
        ("io.k8s.api.core.v1.Container", "pod.spec.containers"),
        ("io.k8s.api.apps.v1.DeploymentSpec", "deployment.spec"),
        ("io.k8s.api.apps.v1.ReplicaSetSpec", "replicaset.spec"),
        ("io.k8s.api.apps.v1.DaemonSetSpec", "daemonset.spec"),
        ("io.k8s.api.apps.v1.StatefulSetSpec", "statefulset.spec"),
        ("io.k8s.api.batch.v1.JobSpec", "job.spec"),
        ("io.k8s.api.core.v1.ServiceSpec", "service.spec"),
        ("io.k8s.api.core.v1.ConfigMapData", "configmap.data"),
        ("io.k8s.api.core.v1.SecretData", "secret.data"),
        ("io.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta", "pod.metadata"),
        ("com.github.openshift.api.route.v1.RouteSpec", "route.spec"),
    ]

    supplemented_definitions = definitions.copy()

    def _run_explain_and_parse(ref_name: str, explain_path: str) -> tuple[dict[str, Any], list[str]] | None:
        """Helper function to run oc explain and parse the output."""
        try:
            cmd = [client, "explain", explain_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                explain_schema = _parse_oc_explain_output(result.stdout)
                explain_properties = explain_schema.get("properties", {})
                explain_required = explain_schema.get("required", [])
                return explain_properties, explain_required
            else:
                LOGGER.warning(f"Failed to get {client} explain for {explain_path}: {result.stderr}")
                return None

        except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError) as e:
            LOGGER.warning(f"Failed to run {client} explain for {explain_path}: {e}")
            return None

    for ref_name, explain_path in critical_specs:
        if ref_name in definitions:
            current_schema = definitions[ref_name]

            LOGGER.info(f"Supplementing schema for {ref_name} using {client} explain {explain_path}")
            result = _run_explain_and_parse(ref_name, explain_path)

            if result:
                explain_properties, explain_required = result

                # Start with the current schema
                updated_schema = current_schema.copy()
                current_properties = updated_schema.get("properties", {})

                # Update properties with descriptions from explain
                for field_name, explain_field in explain_properties.items():
                    if field_name in current_properties:
                        # Merge the current property with the explain description
                        updated_property = current_properties[field_name].copy()
                        if "description" in explain_field and "description" not in updated_property:
                            updated_property["description"] = explain_field["description"]
                        current_properties[field_name] = updated_property

                updated_schema["properties"] = current_properties

                # Update required fields if they're missing
                current_required = updated_schema.get("required")
                if (not current_required or current_required is None) and explain_required:
                    updated_schema["required"] = explain_required
                    LOGGER.info(f"Added {len(explain_required)} required fields to {ref_name}: {explain_required}")
                elif not current_required:
                    updated_schema["required"] = []

                supplemented_definitions[ref_name] = updated_schema

                # Count how many descriptions were added
                desc_count = sum(1 for field in explain_properties.values() if "description" in field)
                if desc_count > 0:
                    LOGGER.info(f"Added {desc_count} field descriptions to {ref_name}")
            else:
                # Set to empty list if explain fails
                if current_schema.get("required") is None:
                    supplemented_definitions[ref_name] = {**current_schema, "required": []}
        else:
            # Handle missing definitions - create them from oc explain output
            LOGGER.info(f"Creating missing schema definition for {ref_name} using {client} explain {explain_path}")
            result = _run_explain_and_parse(ref_name, explain_path)

            if result:
                explain_properties, explain_required = result

                # Create new schema from explain output
                new_schema = {"type": "object", "properties": explain_properties, "required": explain_required}

                supplemented_definitions[ref_name] = new_schema
                LOGGER.info(
                    f"Created new schema definition for {ref_name} with {len(explain_properties)} properties and {len(explain_required)} required fields: {explain_required}"
                )

    # Second, supplement top-level resource schemas with their required fields
    _supplement_resource_level_required_fields(supplemented_definitions, client)

    return supplemented_definitions


def _supplement_resource_level_required_fields(definitions: dict[str, Any], client: str) -> None:
    """
    Supplement resource-level schemas with required field information from explain.

    This function focuses on top-level required fields like 'spec', 'metadata', etc.
    that are marked as required in explain but missing in the schema.

    Args:
        definitions: Definitions dictionary to update in-place
        client: oc/kubectl client binary path
    """
    # Map resource schemas to their explain paths for top-level required fields
    resource_explain_mappings = [
        # Core API resources
        ("v1/Pod", "pod"),
        ("v1/Service", "service"),
        ("v1/ConfigMap", "configmap"),
        ("v1/Secret", "secret"),
        ("v1/PersistentVolume", "persistentvolume"),
        ("v1/PersistentVolumeClaim", "persistentvolumeclaim"),
        ("v1/ServiceAccount", "serviceaccount"),
        ("v1/Namespace", "namespace"),
        # Apps API resources
        ("apps/v1/Deployment", "deployment"),
        ("apps/v1/ReplicaSet", "replicaset"),
        ("apps/v1/DaemonSet", "daemonset"),
        ("apps/v1/StatefulSet", "statefulset"),
        # Batch API resources
        ("batch/v1/Job", "job"),
        ("batch/v1/CronJob", "cronjob"),
        # Networking API resources
        ("networking.k8s.io/v1/NetworkPolicy", "networkpolicy"),
        ("networking.k8s.io/v1/Ingress", "ingress"),
        # RBAC API resources
        ("rbac.authorization.k8s.io/v1/Role", "role"),
        ("rbac.authorization.k8s.io/v1/RoleBinding", "rolebinding"),
        ("rbac.authorization.k8s.io/v1/ClusterRole", "clusterrole"),
        ("rbac.authorization.k8s.io/v1/ClusterRoleBinding", "clusterrolebinding"),
        # OpenShift-specific resources that commonly have required spec
        ("route.openshift.io/v1/Route", "route"),
        ("build.openshift.io/v1/BuildConfig", "buildconfig"),
        ("apps.openshift.io/v1/DeploymentConfig", "deploymentconfig"),
        ("image.openshift.io/v1/ImageStream", "imagestream"),
        ("template.openshift.io/v1/Template", "template"),
        ("config.openshift.io/v1/ClusterVersion", "clusterversion"),
        ("config.openshift.io/v1/Infrastructure", "infrastructure"),
        ("config.openshift.io/v1/DNS", "dns"),
        ("config.openshift.io/v1/Ingress", "ingress.config.openshift.io"),
        ("config.openshift.io/v1/Network", "network.config.openshift.io"),
        ("operator.openshift.io/v1/Console", "console"),
        ("operator.openshift.io/v1/DNS", "dns.operator.openshift.io"),
        ("operator.openshift.io/v1/Network", "network.operator.openshift.io"),
    ]

    for schema_key, explain_path in resource_explain_mappings:
        if schema_key in definitions:
            current_schema = definitions[schema_key]
            current_required = current_schema.get("required")

            # Only supplement if required field is missing or empty
            if not current_required:
                try:
                    LOGGER.info(
                        f"Supplementing top-level required fields for {schema_key} using {client} explain {explain_path}"
                    )
                    cmd = [client, "explain", explain_path]

                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                    if result.returncode == 0:
                        explain_schema = _parse_oc_explain_output(result.stdout)
                        explain_required = explain_schema.get("required", [])

                        if explain_required:
                            # Update the schema with required fields from explain
                            updated_schema = current_schema.copy()
                            updated_schema["required"] = explain_required
                            definitions[schema_key] = updated_schema

                            LOGGER.info(
                                f"Added {len(explain_required)} top-level required fields to {schema_key}: {explain_required}"
                            )
                        else:
                            # Set empty list if explain returns no required fields
                            updated_schema = current_schema.copy()
                            updated_schema["required"] = []
                            definitions[schema_key] = updated_schema
                    else:
                        LOGGER.debug(
                            f"{client} explain failed for {explain_path}, skipping required field supplementation"
                        )
                        # Set empty list if explain fails
                        updated_schema = current_schema.copy()
                        updated_schema["required"] = []
                        definitions[schema_key] = updated_schema

                except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError) as e:
                    LOGGER.warning(f"Failed to run {client} explain for {explain_path}: {e}")
                    # Set empty list if explain fails
                    updated_schema = current_schema.copy()
                    updated_schema["required"] = []
                    definitions[schema_key] = updated_schema


def _get_missing_core_definitions(
    definitions: dict[str, Any], client: str, schemas: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """
    Dynamically detect and fetch missing core Kubernetes type definitions using oc explain.
    Only called during schema updates.

    Args:
        definitions: Current definitions dictionary
        client: oc/kubectl client binary path
        schemas: All fetched API schemas for analyzing missing refs

    Returns:
        Dictionary of missing definitions populated from oc explain
    """
    # Dynamically detect missing $ref definitions
    missing_refs = _detect_missing_refs_from_schemas(schemas, definitions)

    missing_definitions = {}

    for ref_name in missing_refs:
        # Try to infer the oc explain path
        oc_path = _infer_oc_explain_path(ref_name)

        if oc_path:
            try:
                LOGGER.info(f"Fetching missing definition for {ref_name} using oc explain {oc_path}")
                cmd = [client, "explain", oc_path, "--recursive"]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    schema = _parse_oc_explain_output(result.stdout)
                    # Store with the full reference name
                    missing_definitions[ref_name] = schema
                    LOGGER.info(f"Successfully fetched definition for {ref_name}")
                else:
                    LOGGER.warning(f"Failed to get oc explain for {oc_path}: {result.stderr}")

            except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError) as e:
                LOGGER.warning(f"Failed to run oc explain for {oc_path}: {e}")
        else:
            # For types we can't infer paths for, provide basic object schema
            if any(core_type in ref_name for core_type in ["ObjectMeta", "TypeMeta", "Status", "LabelSelector"]):
                LOGGER.info(f"Using basic object schema for core type: {ref_name}")
                missing_definitions[ref_name] = {"type": "object", "additionalProperties": True}
            else:
                LOGGER.warning(f"Cannot infer oc explain path for {ref_name}, skipping")

    if missing_definitions:
        LOGGER.info(f"Retrieved {len(missing_definitions)} missing core definitions using oc explain")

    return missing_definitions


def write_schema_files(
    resources_mapping: dict[str, Any],
    definitions: dict[str, Any],
    client: str | None = None,
    schemas: dict[str, dict[str, Any]] | None = None,
) -> None:
    """
    Write schema files to disk.

    Args:
        resources_mapping: Resources mapping dictionary
        definitions: Schema definitions dictionary
        client: Optional oc/kubectl client binary path for fetching missing definitions
        schemas: Optional all fetched API schemas for analyzing missing refs

    Raises:
        IOError: If files cannot be written
    """
    # Ensure schema directory exists
    try:
        Path(SCHEMA_DIR).mkdir(parents=True, exist_ok=True)
    except (OSError, IOError) as e:
        error_msg = f"Failed to create schema directory {SCHEMA_DIR}: {e}"
        LOGGER.error(error_msg)
        raise IOError(error_msg) from e

    # If client is provided (during schema update), fetch missing core definitions
    if client and schemas:
        missing_definitions = _get_missing_core_definitions(definitions, client, schemas)
        if missing_definitions:
            definitions.update(missing_definitions)
            LOGGER.info(f"Added {len(missing_definitions)} missing core definitions to schema")

    # If client is provided, supplement existing definitions with field descriptions and required field information
    if client:
        definitions = _supplement_schema_with_field_descriptions(definitions, client)
        LOGGER.info("Supplemented definitions with field descriptions and required field information")

    # Write updated definitions
    definitions_file = DEFINITIONS_FILE
    try:
        # Wrap definitions in a "definitions" object for jsonschema compatibility
        definitions_data = {"definitions": definitions}
        with open(definitions_file, "w") as fd:
            json.dump(definitions_data, fd, indent=2, sort_keys=True)
        LOGGER.info(f"Written {len(definitions)} definitions to {definitions_file}")
    except (OSError, IOError, TypeError) as e:
        error_msg = f"Failed to write definitions file {definitions_file}: {e}"
        LOGGER.error(error_msg)
        raise IOError(error_msg) from e

    # Write and archive resources mapping
    try:
        save_json_archive(resources_mapping, RESOURCES_MAPPING_FILE)
    except (OSError, IOError, TypeError) as e:
        error_msg = f"Failed to save and archive resources mapping file {RESOURCES_MAPPING_FILE}: {e}"
        LOGGER.error(error_msg)
        raise IOError(error_msg) from e


def update_kind_schema() -> None:
    """Update schema files using OpenAPI v3 endpoints"""
    client = get_client_binary()

    # Build namespacing dictionary once
    namespacing_dict = build_namespacing_dict(client=client)

    # Get v3 API index
    LOGGER.info("Fetching OpenAPI v3 index...")
    success, v3_data, _ = run_command(command=shlex.split(f"{client} get --raw /openapi/v3"), check=False)
    if not success:
        error_msg = "Failed to fetch OpenAPI v3 index"
        LOGGER.error(error_msg)
        raise RuntimeError(error_msg)

    v3_index = json.loads(v3_data)
    paths = v3_index.get("paths", {})
    LOGGER.info(f"Found {len(paths)} API groups to process")

    # Check and update cluster version
    try:
        should_update = check_and_update_cluster_version(client=client)
    except ClusterVersionError as e:
        LOGGER.error(f"Cannot proceed without cluster version information: {e}")
        raise

    # Load existing resources mapping
    resources_mapping = read_resources_mapping_file()

    # Fetch all API schemas in parallel
    schemas = fetch_all_api_schemas(client=client, paths=paths)

    # Process schema definitions
    LOGGER.info(
        f"Cluster version is {'same or newer' if should_update else 'older'}. {'Allowing updates to existing resources' if should_update else 'Only adding new resources, keeping existing ones unchanged'}."
    )
    resources_mapping, definitions = process_schema_definitions(
        schemas=schemas,
        namespacing_dict=namespacing_dict,
        existing_resources_mapping=resources_mapping,
        allow_updates=should_update,
    )

    # Write schema files
    try:
        write_schema_files(resources_mapping=resources_mapping, definitions=definitions, client=client, schemas=schemas)
    except IOError as e:
        LOGGER.error(f"Failed to write schema files: {e}")
        raise

    # Clear cached mapping data in SchemaValidator to force reload
    SchemaValidator.clear_cache()
    SchemaValidator.load_mappings_data()
