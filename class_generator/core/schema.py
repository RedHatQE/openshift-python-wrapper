"""Schema management functions for resource definitions."""

import json
import shlex
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from packaging.version import Version
from pyhelper_utils.shell import run_command
from simple_logger.logger import get_logger

from class_generator.constants import RESOURCES_MAPPING_FILE, SCHEMA_DIR
from ocp_resources.utils.schema_validator import SchemaValidator

LOGGER = get_logger(name=__name__)


def get_client_binary() -> str:
    """Determine whether to use 'oc' or 'kubectl' binary."""
    # Check if 'oc' binary exists
    rc, _, _ = run_command(command=shlex.split("which oc"), check=False)
    if rc == 0:
        return "oc"

    # Fall back to kubectl
    rc, _, _ = run_command(command=shlex.split("which kubectl"), check=False)
    if rc == 0:
        return "kubectl"

    raise RuntimeError("Neither 'oc' nor 'kubectl' binary found in PATH")


def read_resources_mapping_file() -> dict[Any, Any]:
    """Read resources mapping using SchemaValidator for consistency"""
    # Try to use SchemaValidator first
    if SchemaValidator.load_mappings_data():
        mappings = SchemaValidator.get_mappings_data()
        if mappings is not None:
            return mappings

    # Fallback for cases where schema files don't exist yet (e.g., initial generation)
    try:
        with open(RESOURCES_MAPPING_FILE) as fd:
            return json.load(fd)
    except (FileNotFoundError, json.JSONDecodeError):
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
        LOGGER.error("Failed to get server version")
        sys.exit(1)

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
    """
    cluster_version_file = Path("class_generator/schema/__cluster_version__.txt")
    last_cluster_version_generated: str = ""

    try:
        with open(cluster_version_file, "r") as fd:
            last_cluster_version_generated = fd.read().strip()
    except (FileNotFoundError, IOError) as exp:
        LOGGER.error(f"Failed to read cluster version file: {exp}")
        sys.exit(1)

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
    schemas: dict[str, dict[str, Any]], namespacing_dict: dict[str, bool], existing_resources_mapping: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Process schema definitions to extract resource information.

    Args:
        schemas: Dictionary of API schemas
        namespacing_dict: Dictionary of resource namespacing info
        existing_resources_mapping: Existing resources mapping

    Returns:
        tuple: (resources_mapping, definitions)
    """
    resources_mapping = existing_resources_mapping.copy()
    definitions = {}
    processed_schemas = set()
    total_schemas = 0

    for api_path, schema in schemas.items():
        # Process schema definitions
        for def_name, def_data in schema.get("definitions", {}).items():
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
                resources_mapping[kind_lower] = []

            # Add this schema to the kind's array
            resources_mapping[kind_lower].append(schema_data)

            # Also store in definitions for separate definitions file
            definitions[schema_name] = schema_data
            total_schemas += 1

    LOGGER.info(f"Processed {total_schemas} unique schemas")
    return resources_mapping, definitions


def write_schema_files(resources_mapping: dict[str, Any], definitions: dict[str, Any]) -> None:
    """
    Write schema files to disk.

    Args:
        resources_mapping: Resources mapping dictionary
        definitions: Schema definitions dictionary
    """
    # Ensure schema directory exists
    Path(SCHEMA_DIR).mkdir(parents=True, exist_ok=True)

    # Write updated definitions
    definitions_file = Path(SCHEMA_DIR) / "_definitions.json"
    with open(definitions_file, "w") as fd:
        json.dump(definitions, fd, indent=2, sort_keys=True)
    LOGGER.info(f"Written definitions to {definitions_file}")

    # Write updated resources mapping
    with open(RESOURCES_MAPPING_FILE, "w") as fd:
        json.dump(resources_mapping, fd, indent=2, sort_keys=True)
    LOGGER.info(f"Written resources mapping to {RESOURCES_MAPPING_FILE}")


def update_kind_schema() -> None:
    """Update schema files using OpenAPI v3 endpoints"""
    client = get_client_binary()

    # Build namespacing dictionary once
    namespacing_dict = build_namespacing_dict(client=client)

    # Get v3 API index
    LOGGER.info("Fetching OpenAPI v3 index...")
    success, v3_data, _ = run_command(command=shlex.split(f"{client} get --raw /openapi/v3"), check=False)
    if not success:
        LOGGER.error("Failed to fetch OpenAPI v3 index")
        sys.exit(1)

    v3_index = json.loads(v3_data)
    paths = v3_index.get("paths", {})
    LOGGER.info(f"Found {len(paths)} API groups to process")

    # Check and update cluster version
    check_and_update_cluster_version(client)

    # Load existing resources mapping
    resources_mapping = read_resources_mapping_file()

    # Fetch all API schemas in parallel
    schemas = fetch_all_api_schemas(client, paths)

    # Process schema definitions
    resources_mapping, definitions = process_schema_definitions(schemas, namespacing_dict, resources_mapping)

    # Write schema files
    write_schema_files(resources_mapping, definitions)

    # Clear cached mapping data in SchemaValidator to force reload
    SchemaValidator.clear_cache()
    SchemaValidator.load_mappings_data()
