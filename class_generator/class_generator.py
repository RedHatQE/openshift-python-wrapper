import ast
import filecmp
import json
import keyword
import os
import shlex
import shutil
import sys
import textwrap
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from io import StringIO
from pathlib import Path
from tempfile import gettempdir
from typing import Any

import cloup
import pytest
from cloup.constraints import If, IsSet, accept_none, require_one
from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta
from kubernetes.dynamic import DynamicClient
from packaging.version import Version
from pyhelper_utils.shell import run_command
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from simple_logger.logger import get_logger

from fake_kubernetes_client.dynamic_client import FakeDynamicClient
from ocp_resources.resource import Resource, get_client
from ocp_resources.utils.schema_validator import SchemaValidator
from ocp_resources.utils.utils import convert_camel_case_to_snake_case

# Set global logging
LOGGER = get_logger(name="class_generator")
SPEC_STR: str = "SPEC"
FIELDS_STR: str = "FIELDS"
TESTS_MANIFESTS_DIR: str = "class_generator/tests/manifests"
SCHEMA_DIR: str = "class_generator/schema"
RESOURCES_MAPPING_FILE: str = os.path.join(SCHEMA_DIR, "__resources-mappings.json")
MISSING_DESCRIPTION_STR: str = "No field description from API"

# Python keyword mappings for safe variable names
PYTHON_KEYWORD_MAPPINGS = {
    # Map Python keywords to safe alternatives by appending underscore
    kw: f"{kw}_"
    for kw in keyword.kwlist
}


def sanitize_python_name(name: str) -> tuple[str, str]:
    """
    Sanitize a name to be a valid Python identifier.

    Args:
        name: The original field name

    Returns:
        tuple: (python_safe_name, original_name)
    """
    if name in PYTHON_KEYWORD_MAPPINGS:
        return PYTHON_KEYWORD_MAPPINGS[name], name
    return name, name


def discover_cluster_resources(
    client: DynamicClient | FakeDynamicClient | None = None, api_group_filter: str | None = None
) -> dict[str, list[dict[str, Any]]]:
    """
    Discover all resources available in the cluster.

    Args:
        client: Kubernetes dynamic client. If None, will create one.
        api_group_filter: Filter resources by API group (e.g., "apps", "route.openshift.io")

    Returns:
        Dictionary mapping API version to list of resources
    """
    if not client:
        client = get_client()
        if not isinstance(client, DynamicClient):
            raise ValueError(f"Expected DynamicClient instance, got {type(client).__name__}")

    discovered_resources: dict[str, list[dict[str, Any]]] = {}

    try:
        # Use the underlying kubernetes client to get API resources
        k8s_client = client.client

        # Create a thread pool for parallel discovery
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures: list[Future] = []

            # Function to process core API resources
            def process_core_api() -> tuple[str, list[dict[str, Any]]]:
                try:
                    response = k8s_client.call_api(
                        resource_path="/api/v1",
                        method="GET",
                        auth_settings=["BearerToken"],
                        response_type="object",
                        _return_http_data_only=True,
                    )

                    if response and "resources" in response:
                        resources = []
                        for r in response["resources"]:
                            if "/" not in r.get("name", ""):  # Filter out subresources
                                resources.append({
                                    "name": r.get("name"),
                                    "kind": r.get("kind"),
                                    "namespaced": r.get("namespaced", True),
                                })
                        return "v1", resources
                except Exception as e:
                    LOGGER.debug(f"Failed to get core API resources: {e}")
                return "v1", []

            # Submit core API discovery
            futures.append(executor.submit(process_core_api))

            # Function to process a specific API group version
            def process_api_group_version(group_version: str) -> tuple[str, list[dict[str, Any]]]:
                try:
                    api_path = f"/apis/{group_version}"
                    resources_response = k8s_client.call_api(
                        resource_path=api_path,
                        method="GET",
                        auth_settings=["BearerToken"],
                        response_type="object",
                        _return_http_data_only=True,
                    )

                    if resources_response and "resources" in resources_response:
                        resources = []
                        for r in resources_response["resources"]:
                            if "/" not in r.get("name", ""):  # Filter out subresources
                                resources.append({
                                    "name": r.get("name"),
                                    "kind": r.get("kind"),
                                    "namespaced": r.get("namespaced", True),
                                })
                        return group_version, resources
                except Exception as e:
                    LOGGER.debug(f"Failed to get resources for {group_version}: {e}")
                return group_version, []

            # Get all API groups
            try:
                groups_response = k8s_client.call_api(
                    resource_path="/apis",
                    method="GET",
                    auth_settings=["BearerToken"],
                    response_type="object",
                    _return_http_data_only=True,
                )

                if groups_response and "groups" in groups_response:
                    for group in groups_response["groups"]:
                        group_name = group.get("name", "")

                        # Apply filter if specified
                        if api_group_filter and group_name != api_group_filter:
                            if api_group_filter not in group_name:
                                continue

                        # Process each version in the group
                        for version in group.get("versions", []):
                            group_version = version.get("groupVersion", "")
                            if group_version:
                                # Submit API group version discovery to thread pool
                                futures.append(executor.submit(process_api_group_version, group_version))

            except Exception as e:
                LOGGER.debug(f"Failed to get API groups: {e}")

            # Function to process CRDs
            def process_crds() -> list[tuple[str, list[dict[str, Any]]]]:
                results = []
                try:
                    crd_resources = client.resources.get(
                        api_version="apiextensions.k8s.io/v1", kind="CustomResourceDefinition"
                    )
                    crds = crd_resources.get()

                    # Check if items is iterable
                    crd_items = crds.items if hasattr(crds, "items") else []
                    if callable(crd_items):
                        crd_items = crd_items()

                    for crd in crd_items:
                        crd_group = crd.spec.group

                        # Apply filter if specified
                        if api_group_filter and crd_group != api_group_filter:
                            if api_group_filter not in crd_group:
                                continue

                        for version in crd.spec.versions:
                            if version.served:
                                group_version = f"{crd_group}/{version.name}"
                                resource_info = {
                                    "name": crd.spec.names.plural,
                                    "kind": crd.spec.names.kind,
                                    "namespaced": crd.spec.scope == "Namespaced",
                                }
                                results.append((group_version, [resource_info]))

                except Exception as e:
                    LOGGER.debug(f"Failed to discover CRDs: {e}")
                return results

            # Submit CRD discovery
            crd_future = executor.submit(process_crds)

            # Collect results from all futures
            for future in as_completed(futures):
                try:
                    api_version, resources = future.result()
                    if resources:
                        if api_version in discovered_resources:
                            # Merge resources, avoiding duplicates
                            existing_kinds = {r["kind"] for r in discovered_resources[api_version]}
                            for resource in resources:
                                if resource["kind"] not in existing_kinds:
                                    discovered_resources[api_version].append(resource)
                        else:
                            discovered_resources[api_version] = resources
                except Exception as e:
                    LOGGER.debug(f"Failed to process discovery result: {e}")

            # Process CRD results
            try:
                crd_results = crd_future.result()
                for group_version, resources in crd_results:
                    if group_version in discovered_resources:
                        # Merge, avoiding duplicates
                        existing_kinds = {r["kind"] for r in discovered_resources[group_version]}
                        for resource in resources:
                            if resource["kind"] not in existing_kinds:
                                discovered_resources[group_version].append(resource)
                    else:
                        discovered_resources[group_version] = resources
            except Exception as e:
                LOGGER.debug(f"Failed to process CRD results: {e}")

    except Exception as e:
        LOGGER.error(f"Failed to discover cluster resources: {e}")
        raise

    return discovered_resources


def analyze_coverage(
    discovered_resources: dict[str, list[dict[str, Any]]], resources_dir: str = "ocp_resources"
) -> dict[str, Any]:
    """
    Analyze coverage of implemented resources vs discovered resources.

    Args:
        discovered_resources: Resources discovered from cluster
        resources_dir: Directory containing resource implementation files

    Returns:
        Dictionary containing:
        - implemented_resources: List of resource kinds that have implementations
        - missing_resources: List of resources that need implementation
        - coverage_stats: Statistics about coverage
    """
    implemented_resources: list[str] = []

    # Scan the resources directory
    try:
        if not os.path.exists(resources_dir):
            LOGGER.warning(f"Resources directory '{resources_dir}' not found")
            files = []
        else:
            files = os.listdir(resources_dir)
    except Exception as e:
        LOGGER.error(f"Failed to scan resources directory: {e}")
        files = []

    # Parse each Python file to find implemented resources
    for filename in files:
        # Skip non-Python files and special files
        if not filename.endswith(".py") or filename == "__init__.py":
            continue

        # Skip utility/helper files
        if filename in ["utils.py", "constants.py", "exceptions.py", "resource.py"]:
            continue

        filepath = os.path.join(resources_dir, filename)
        if not os.path.isfile(filepath):
            continue

        try:
            with open(filepath, "r") as f:
                content = f.read()

            # Parse the file to find class definitions
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if this is a resource class (not a helper/base class)
                    # Look for classes that inherit from Resource, NamespacedResource, etc.
                    for base in node.bases:
                        base_name = ""
                        if isinstance(base, ast.Name):
                            base_name = base.id
                        elif isinstance(base, ast.Attribute):
                            base_name = base.attr

                        if "Resource" in base_name:
                            # This is a resource class
                            resource_kind = node.name
                            # Avoid duplicates (e.g., DNS implemented in multiple files)
                            if resource_kind not in implemented_resources:
                                implemented_resources.append(resource_kind)
                            break

        except Exception as e:
            LOGGER.debug(f"Failed to parse {filename}: {e}")
            continue

    # Calculate missing resources and coverage
    missing_resources: list[dict[str, Any]] = []
    total_discovered = 0
    covered_resources = 0

    for api_version, resources in discovered_resources.items():
        for resource in resources:
            total_discovered += 1
            resource_kind = resource.get("kind", "")

            if resource_kind not in implemented_resources:
                missing_resources.append({
                    "kind": resource_kind,
                    "api_version": api_version,
                    "name": resource.get("name", ""),
                    "namespaced": resource.get("namespaced", True),
                })
            else:
                covered_resources += 1

    # Calculate coverage statistics
    total_missing = len(missing_resources)

    if total_discovered > 0:
        coverage_percentage = (covered_resources / total_discovered) * 100
    else:
        coverage_percentage = 0.0

    return {
        "implemented_resources": implemented_resources,
        "missing_resources": missing_resources,
        "coverage_stats": {
            "total_discovered": total_discovered,
            "total_implemented": len(implemented_resources),
            "covered_resources": covered_resources,
            "total_missing": total_missing,
            "coverage_percentage": round(coverage_percentage, 2),
        },
    }


def generate_report(coverage_analysis: dict[str, Any], output_format: str = "human") -> str:
    """
    Generate a report from coverage analysis results.

    Args:
        coverage_analysis: Results from analyze_coverage()
        output_format: Either "human" for Rich-formatted text or "json"

    Returns:
        Formatted report string
    """

    def calculate_priority(resource: dict[str, Any]) -> int:
        """Calculate priority score for a resource (higher = more important)."""
        api_version = resource.get("api_version", "")

        # Core resources (v1) have highest priority
        if api_version == "v1":
            return 100

        # Standard Kubernetes APIs
        if any(api in api_version for api in ["apps/", "batch/", "networking.k8s.io/", "storage.k8s.io/"]):
            return 80

        # OpenShift core APIs
        if any(api in api_version for api in ["route.openshift.io/", "image.openshift.io/", "config.openshift.io/"]):
            return 70

        # Operator resources
        if any(api in api_version for api in ["operators.coreos.com/", ".operator.openshift.io/"]):
            return 50

        # Other CRDs
        return 30

    def generate_class_generator_command(resource: dict[str, Any]) -> str:
        """Generate class-generator command for a resource."""
        kind = resource.get("kind", "")
        # For now, class-generator only accepts the kind parameter
        # API version/group selection is handled automatically by the tool
        cmd = f"class-generator -k {kind}"
        return cmd

    missing_resources = coverage_analysis.get("missing_resources", [])

    # Add priority scores
    for resource in missing_resources:
        resource["priority"] = calculate_priority(resource=resource)

    # Sort by priority
    missing_resources.sort(key=lambda x: x["priority"], reverse=True)

    if output_format == "json":
        # JSON format for CI/CD
        generation_commands = [generate_class_generator_command(r) for r in missing_resources]

        # Group by API version for batch commands
        batch_commands = []
        api_groups: dict[str, list[str]] = {}
        for resource in missing_resources:
            api_version = resource.get("api_version", "")
            kind = resource.get("kind", "")
            if api_version not in api_groups:
                api_groups[api_version] = []
            api_groups[api_version].append(kind)

        for api_version, kinds in api_groups.items():
            if len(kinds) > 1:
                cmd = f"class-generator -k {','.join(kinds)}"
                batch_commands.append(cmd)

        report_data = {
            "coverage_stats": coverage_analysis.get("coverage_stats", {}),
            "implemented_resources": coverage_analysis.get("implemented_resources", []),
            "missing_resources": missing_resources,
            "generation_commands": generation_commands,
            "batch_generation_commands": batch_commands,
        }

        return json.dumps(report_data, indent=2)

    else:
        # Human-readable format with Rich
        # Create string buffer to capture Rich output
        string_buffer = StringIO()
        console = Console(file=string_buffer, force_terminal=True, width=120)

        # Title
        console.print("\n[bold cyan]Resource Coverage Report[/bold cyan]\n")

        # Coverage Statistics Panel
        stats = coverage_analysis.get("coverage_stats", {})
        stats_text = f"""
Total Discovered Resources: [bold]{stats.get("total_discovered", 0)}[/bold]
Implemented Resources: [bold green]{stats.get("total_implemented", 0)}[/bold green]
Covered Resources: [bold green]{stats.get("covered_resources", 0)}[/bold green]
Missing Resources: [bold red]{stats.get("total_missing", 0)}[/bold red]
Coverage Percentage: [bold yellow]{stats.get("coverage_percentage", 0)}%[/bold yellow]
"""
        console.print(Panel(stats_text.strip(), title="Coverage Statistics", border_style="cyan"))

        # Missing Resources Table
        if missing_resources:
            console.print("\n[bold]Missing Resources[/bold] (sorted by priority)\n")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Priority", style="cyan", width=10)
            table.add_column("Kind", style="yellow")
            table.add_column("API Version", style="green")
            table.add_column("Namespaced", style="blue")
            table.add_column("Command", style="white")

            for resource in missing_resources:
                priority = resource.get("priority", 0)
                priority_label = "HIGH" if priority >= 80 else "MEDIUM" if priority >= 50 else "LOW"
                if resource.get("api_version") == "v1":
                    priority_label = "[bold red]CORE[/bold red]"

                table.add_row(
                    priority_label,
                    resource.get("kind", ""),
                    resource.get("api_version", ""),
                    "Yes" if resource.get("namespaced", True) else "No",
                    generate_class_generator_command(resource),
                )

            console.print(table)

            # Batch generation tip
            if len(missing_resources) > 3:
                console.print("\n[bold]Tip:[/bold] You can generate multiple resources at once:")
                # Show first batch command as example
                example_groups: dict[str, list[str]] = {}
                for resource in missing_resources[:5]:  # Just first 5 as example
                    api_version = resource.get("api_version", "")
                    kind = resource.get("kind", "")
                    if api_version not in example_groups:
                        example_groups[api_version] = []
                    example_groups[api_version].append(kind)

                for api_version, kinds in example_groups.items():
                    if len(kinds) > 1:
                        cmd = f"class-generator -k {','.join(kinds)}"
                        console.print(f"\n  [green]{cmd}[/green]")
                        break
        else:
            console.print("\n[bold green]All resources are implemented! 🎉[/bold green]\n")

        # Get the string output
        output = string_buffer.getvalue()
        string_buffer.close()

        return output


def _is_kind_and_namespaced(
    client: str, _key: str, _data: dict[str, Any], kind: str, group: str, version: str
) -> dict[str, Any]:
    _group_and_version = f"{group}/{version}" if group else version
    not_resource_dict = {"is_kind": False, "kind": _key}

    # if explain command failed, this is not a resource
    if not run_command(command=shlex.split(f"{client} explain {kind}"), check=False, log_errors=False)[0]:
        return not_resource_dict

    api_resources_base_cmd = f"bash -c '{client} api-resources"

    # check if this as a valid version for the resource.
    if run_command(
        command=shlex.split(f"{api_resources_base_cmd} | grep -w {kind} | grep {_group_and_version}'"),
        check=False,
        log_errors=False,
    )[0]:
        # Check if the resource if namespaced.
        _data["namespaced"] = (
            run_command(
                command=shlex.split(
                    f"{api_resources_base_cmd} --namespaced | grep -w {kind} | grep {_group_and_version} | wc -l'"
                ),
                check=False,
                log_errors=False,
            )[1].strip()
            == "1"
        )
        return {"is_kind": True, "kind": _key, "data": _data}

    return not_resource_dict


def map_kind_to_namespaced(client: str, newer_cluster_version: bool, schema_definition_file: Path) -> None:
    not_kind_file: str = os.path.join(SCHEMA_DIR, "__not-kind.txt")

    resources_mapping = read_resources_mapping_file()

    if os.path.isfile(not_kind_file):
        with open(not_kind_file) as fd:
            not_kind_list = fd.read().split("\n")
    else:
        not_kind_list = []

    with open(schema_definition_file) as fd:
        _definitions_json_data = json.load(fd)

    _kind_data_futures: list[Future] = []
    with ThreadPoolExecutor() as executor:
        for _key, _data in _definitions_json_data["definitions"].items():
            if not _data.get("x-kubernetes-group-version-kind"):
                continue

            if _key in not_kind_list:
                continue

            x_kubernetes_group_version_kind = extract_group_kind_version(_kind_schema=_data)
            _kind = x_kubernetes_group_version_kind["kind"]
            _group = x_kubernetes_group_version_kind.get("group", "")
            _version = x_kubernetes_group_version_kind.get("version", "")

            # Do not add the resource if it is already in the mapping and the cluster version is not newer than the last
            if resources_mapping.get(_kind.lower()) and not newer_cluster_version:
                continue

            _kind_data_futures.append(
                executor.submit(
                    _is_kind_and_namespaced,
                    client=client,
                    _key=_key,
                    _data=_data,
                    kind=_kind,
                    group=_group,
                    version=_version,
                )
            )

    _temp_resources_mappings: dict[Any, Any] = {}
    for res in as_completed(_kind_data_futures):
        _res = res.result()
        # _res["kind"] is group.version.kind, set only kind as key in the final dict
        kind_key = _res["kind"].rsplit(".", 1)[-1].lower()

        if _res["is_kind"]:
            _temp_resources_mappings.setdefault(kind_key, []).append(_res["data"])
        else:
            not_kind_list.append(_res["kind"])

    # Update the resources mapping dict with the one that we filled to avoid duplication in the lists
    resources_mapping.update(_temp_resources_mappings)

    with open(RESOURCES_MAPPING_FILE, "w") as fd:
        json.dump(resources_mapping, fd, indent=4)

    with open(not_kind_file, "w") as fd:
        fd.writelines("\n".join(not_kind_list))

    # Clear SchemaValidator cache so it reloads the updated files
    SchemaValidator.clear_cache()


def read_resources_mapping_file() -> dict[Any, Any]:
    """Read resources mapping using SchemaValidator for consistency"""
    # Try to use SchemaValidator first
    if SchemaValidator.load_mappings_data():
        return SchemaValidator._mappings_data or {}

    # Fallback for cases where schema files don't exist yet (e.g., initial generation)
    try:
        with open(RESOURCES_MAPPING_FILE) as fd:
            return json.load(fd)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_server_version(client: str) -> str:
    rc, out, _ = run_command(command=shlex.split(f"{client} version -o json"), check=False)
    if not rc:
        LOGGER.error("Failed to get server version")
        sys.exit(1)

    json_out = json.loads(out)
    return json_out["serverVersion"]["gitVersion"]


def get_client_binary() -> str:
    if shutil.which("oc"):
        LOGGER.debug("Using 'oc' client.")
        return "oc"

    elif shutil.which("kubectl"):
        LOGGER.debug("Using 'kubectl' client.")
        return "kubectl"

    else:
        LOGGER.error("Failed to find 'oc' or 'kubectl' in PATH.")
        sys.exit(1)


def update_kind_schema() -> None:
    openapi2jsonschema_str: str = "openapi2jsonschema"
    client = get_client_binary()

    if not run_command(command=shlex.split("which openapi2jsonschema"), check=False, log_errors=False)[0]:
        LOGGER.error(
            f"{openapi2jsonschema_str} not found. Install it using `pipx install --python python3.9 openapi2jsonschema`"
        )
        sys.exit(1)

    data = run_command(command=shlex.split(f"{client} get --raw /openapi/v2"))[1]

    cluster_version_file = Path("class_generator/__cluster_version__.txt")
    last_cluster_version_generated: str = ""
    try:
        with open(cluster_version_file, "r") as fd:
            last_cluster_version_generated = fd.read().strip()
    except (FileNotFoundError, IOError) as exp:
        LOGGER.error(f"Failed to read cluster version file: {exp}")
        sys.exit(1)

    cluster_version = get_server_version(client=client)
    cluster_version = cluster_version.split("+")[0]
    ocp_openapi_json_file = Path(gettempdir()) / f"__k8s-openapi-{cluster_version}__.json"

    same_or_newer_version: bool = Version(cluster_version) >= Version(last_cluster_version_generated)

    if same_or_newer_version:
        with open(cluster_version_file, "w") as fd:
            fd.write(cluster_version)

    with open(ocp_openapi_json_file, "w") as fd:
        fd.write(data)

    tmp_schema_dir = Path(gettempdir()) / f"{SCHEMA_DIR}-{cluster_version}"

    if not run_command(command=shlex.split(f"{openapi2jsonschema_str} {ocp_openapi_json_file} -o {tmp_schema_dir}"))[0]:
        LOGGER.error("Failed to generate schema.")
        sys.exit(1)

    if same_or_newer_version:
        # copy all files from tmp_schema_dir to schema dir
        shutil.copytree(src=tmp_schema_dir, dst=SCHEMA_DIR, dirs_exist_ok=True)

    else:
        # Copy only new files from tmp_schema_dir to schema dir
        for root, _, files in os.walk(tmp_schema_dir):
            for file_ in files:
                dst_file = Path(SCHEMA_DIR) / file_
                try:
                    if not os.path.isfile(dst_file):
                        shutil.copy(src=Path(root) / file_, dst=dst_file)
                except (OSError, IOError) as exp:
                    LOGGER.error(f"Failed to copy file {file_}: {exp}")
                    sys.exit(1)

    map_kind_to_namespaced(
        client=client, newer_cluster_version=same_or_newer_version, schema_definition_file=ocp_openapi_json_file
    )

    # Extract schemas from CRDs with OpenAPIV3Schema
    # This supplements the openapi2jsonschema extraction for CRDs that don't fully expose their schemas
    extract_crd_schemas(client=client)

    # Clear SchemaValidator cache after updating schemas
    SchemaValidator.clear_cache()


def parse_user_code_from_file(file_path: str) -> tuple[str, str]:
    with open(file_path) as fd:
        data = fd.read()

    end_of_generated_code_line = "    # End of generated code"
    user_code: str = ""
    user_imports: str = ""

    if end_of_generated_code_line in data:
        _end_of_generated_code_index = data.index(end_of_generated_code_line)
        user_code = data[_end_of_generated_code_index + len(end_of_generated_code_line) :]

        tree = ast.parse(data)
        imports = [imp for imp in tree.body if isinstance(imp, ast.Import) or isinstance(imp, ast.ImportFrom)]
        splited_data = data.splitlines()

        for _import in imports:
            end_import_no = _import.end_lineno

            if end_import_no and _import.lineno != end_import_no:
                for num in range(_import.lineno - 1, end_import_no):
                    user_imports += f"{splited_data[num]}\n"
            else:
                user_imports += f"{splited_data[_import.lineno - 1]}\n"

    return user_code, user_imports


def render_jinja_template(template_dict: dict[Any, Any], template_dir: str, template_name: str) -> str:
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=DebugUndefined,
    )

    template = env.get_template(name=template_name)
    rendered = template.render(template_dict)
    undefined_variables = meta.find_undeclared_variables(env.parse(rendered))

    if undefined_variables:
        LOGGER.error(f"The following variables are undefined: {undefined_variables}")
        sys.exit(1)

    return rendered


def _should_update_schema(schema_filepath: Path, existing_schema: dict[str, Any], crd_schema: dict[str, Any]) -> bool:
    """
    Determine if a schema file should be updated based on its current state.

    Args:
        schema_filepath: Path to the schema file
        existing_schema: The current schema content
        crd_schema: The schema from the CRD

    Returns:
        bool: True if the schema should be updated
    """
    if not schema_filepath.exists():
        return True

    # If the existing schema has no properties defined, we should update it
    if not existing_schema.get("properties"):
        return True

    # Also check if existing schema has properties but is different from CRD schema
    crd_props = crd_schema.get("properties", {})
    existing_props = existing_schema.get("properties", {})
    if existing_props != crd_props and len(crd_props) > len(existing_props):
        return True

    return False


def _format_crd_schema(schema: dict[str, Any], group: str, kind: str, version: str) -> dict[str, Any]:
    """
    Format a CRD schema in the format expected by the class generator.

    Args:
        schema: The OpenAPIV3Schema from the CRD
        group: API group
        kind: Resource kind
        version: API version

    Returns:
        dict: Formatted schema
    """
    formatted_schema = {
        "type": "object",
        "x-kubernetes-group-version-kind": [{"group": group, "kind": kind, "version": version}],
        "$schema": "http://json-schema.org/schema#",
    }

    # Merge the OpenAPIV3Schema content
    formatted_schema.update(schema)

    return formatted_schema


def _update_resource_mapping(
    resources_mapping: dict[str, Any],
    kind_lower: str,
    full_schema: dict[str, Any],
    namespaced: bool,
    group: str,
    version: str,
) -> bool:
    """
    Update or add a resource in the resources mapping.

    Args:
        resources_mapping: The resources mapping dictionary
        kind_lower: Lowercase kind name
        full_schema: The complete schema
        namespaced: Whether the resource is namespaced
        group: API group
        version: API version

    Returns:
        bool: True if an existing mapping was updated, False if a new one was added
    """
    # Initialize or update the resource mapping
    if kind_lower not in resources_mapping:
        resources_mapping[kind_lower] = []

    # Check if this version already exists
    for i, mapping in enumerate(resources_mapping[kind_lower]):
        # Check if this mapping matches the group/version
        mapping_group_version_kinds = mapping.get("x-kubernetes-group-version-kind", [])
        for gvk in mapping_group_version_kinds:
            if gvk.get("group") == group and gvk.get("version") == version:
                # Create new mapping with full schema to ensure atomic update
                new_mapping = full_schema.copy()
                new_mapping["namespaced"] = namespaced
                # Replace the old mapping atomically
                resources_mapping[kind_lower][i] = new_mapping
                return True

    # Add new mapping with full schema
    new_mapping = full_schema.copy()
    new_mapping["namespaced"] = namespaced
    resources_mapping[kind_lower].append(new_mapping)
    return False


def extract_crd_schemas(client: str) -> None:
    """
    Extract schemas from CRDs that have OpenAPIV3Schema defined.
    This supplements the openapi2jsonschema extraction for CRDs that don't expose their full schema via /openapi/v2.
    """
    LOGGER.info("Extracting schemas from CRDs with OpenAPIV3Schema")

    # Get all CRDs
    success, output, _ = run_command(command=shlex.split(f"{client} get crd -o json"), check=False, log_errors=False)
    if not success:
        LOGGER.warning("Failed to get CRDs, skipping CRD schema extraction")
        return

    resources_mapping = read_resources_mapping_file()
    schemas_updated = False

    try:
        crds_data = json.loads(output)
        crds = crds_data.get("items", [])

        for crd in crds:
            crd_name = crd.get("metadata", {}).get("name", "")
            spec = crd.get("spec", {})
            group = spec.get("group", "")

            # Process each version of the CRD
            versions = spec.get("versions", [])
            for version_spec in versions:
                version = version_spec.get("name", "")
                schema = version_spec.get("schema", {}).get("openAPIV3Schema", {})

                if not schema or not version:
                    continue

                # Extract the kind from CRD spec
                kind = spec.get("names", {}).get("kind", "")
                kind_lower = kind.lower()
                if not kind:
                    continue

                # Create the schema file name (same format as openapi2jsonschema)
                schema_filename = f"{kind_lower}.json"
                schema_filepath = Path(SCHEMA_DIR) / schema_filename

                # Check if the schema file should be updated
                existing_schema = {}
                if schema_filepath.exists():
                    with open(schema_filepath, "r") as f:
                        existing_schema = json.load(f)

                if _should_update_schema(schema_filepath, existing_schema, schema):
                    # Format the schema
                    formatted_schema = _format_crd_schema(schema=schema, group=group, kind=kind, version=version)

                    # Write the schema file
                    with open(schema_filepath, "w") as f:
                        json.dump(formatted_schema, f, indent=2)

                    LOGGER.info(f"Updated schema for {kind} from CRD {crd_name}")
                    schemas_updated = True

                    # Read the schema file back to get the full schema
                    with open(schema_filepath, "r") as f:
                        full_schema = json.load(f)

                    # Update resources mapping
                    namespaced = spec.get("scope", "") == "Namespaced"
                    _update_resource_mapping(
                        resources_mapping=resources_mapping,
                        kind_lower=kind_lower,
                        full_schema=full_schema,
                        namespaced=namespaced,
                        group=group,
                        version=version,
                    )

    except json.JSONDecodeError as e:
        LOGGER.warning(f"Failed to parse CRD JSON output: {e}")
    except Exception as e:
        LOGGER.warning(f"Error extracting CRD schemas: {e}")

    # Update the resources mapping file if any schemas were updated
    if schemas_updated:
        with open(RESOURCES_MAPPING_FILE, "w") as fd:
            json.dump(resources_mapping, fd, indent=2)
        LOGGER.info("Updated resources mapping file with CRD schemas")


def generate_resource_file_from_dict(
    resource_dict: dict[str, Any],
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    add_tests: bool = False,
    output_file_suffix: str = "",
    output_dir: str = "",
) -> tuple[str, str]:
    base_dir = output_dir or "ocp_resources"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    rendered = render_jinja_template(
        template_dict=resource_dict,
        template_dir="class_generator/manifests",
        template_name="class_generator_template.j2",
    )

    output = "# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md\n\n"
    formatted_kind_str = convert_camel_case_to_snake_case(name=resource_dict["kind"])
    _file_suffix: str = f"{'_' + output_file_suffix if output_file_suffix else ''}"

    if add_tests:
        overwrite = True
        tests_path = os.path.join(TESTS_MANIFESTS_DIR, resource_dict["kind"])
        if not os.path.exists(tests_path):
            os.makedirs(tests_path)

        _output_file = os.path.join(tests_path, f"{formatted_kind_str}{_file_suffix}.py")

    elif output_file:
        _output_file = output_file

    else:
        _output_file = os.path.join(base_dir, f"{formatted_kind_str}{_file_suffix}.py")

    _output_file_exists: bool = os.path.exists(_output_file)
    _user_code: str = ""
    _user_imports: str = ""

    if _output_file_exists and not add_tests:
        _user_code, _user_imports = parse_user_code_from_file(file_path=_output_file)

    orig_filename = _output_file
    if _output_file_exists:
        if overwrite:
            LOGGER.warning(f"Overwriting {_output_file}")

        else:
            temp_output_file = _output_file.replace(".py", "_TEMP.py")
            LOGGER.warning(f"{_output_file} already exists, using {temp_output_file}")
            _output_file = temp_output_file

    if _user_code.strip() and _user_imports.strip():
        output += f"{_user_imports}{rendered}{_user_code}"
    else:
        output += rendered

    if dry_run:
        _code = Syntax(code=output, lexer="python", line_numbers=True)
        Console().print(_code)

    else:
        write_and_format_rendered(filepath=_output_file, output=output)

    return orig_filename, _output_file


def types_generator(key_dict: dict[str, Any]) -> dict[str, str]:
    type_for_docstring: str = "Any"
    type_from_dict_for_init: str = ""
    # A resource field may be defined with `x-kubernetes-preserve-unknown-fields`. In this case, `type` is not provided.
    resource_type = key_dict.get("type")

    # All fields must be set with Optional since resource can have yaml_file to cover all args.
    if resource_type == "array":
        type_for_docstring = "list[Any]"

    elif resource_type == "string":
        type_for_docstring = "str"
        type_from_dict_for_init = f"{type_for_docstring} | None = None"

    elif resource_type == "boolean":
        type_for_docstring = "bool"

    elif resource_type == "integer":
        type_for_docstring = "int"

    elif resource_type == "object":
        type_for_docstring = "dict[str, Any]"

    if not type_from_dict_for_init:
        type_from_dict_for_init = f"{type_for_docstring} | None = None"

    return {"type-for-init": type_from_dict_for_init, "type-for-doc": type_for_docstring}


def get_property_schema(property_: dict[str, Any]) -> dict[str, Any]:
    if _ref := property_.get("$ref"):
        with open(f"{SCHEMA_DIR}/{_ref.rsplit('.')[-1].lower()}.json") as fd:
            return json.load(fd)
    return property_


def format_description(description: str) -> str:
    _res = ""
    _text = textwrap.wrap(text=description, subsequent_indent="    ")
    for _txt in _text:
        _res += f"{_txt}\n"

    return _res


def prepare_property_dict(
    schema: dict[str, Any],
    required: list[str],
    resource_dict: dict[str, Any],
    dict_key: str,
) -> dict[str, Any]:
    keys_to_ignore: list[str] = ["kind", "apiVersion", "status", SPEC_STR.lower()]
    keys_to_rename: set[str] = {"annotations", "labels"}
    if dict_key != SPEC_STR.lower():
        keys_to_ignore.append("metadata")

    for key, val in schema.items():
        if key in keys_to_ignore:
            continue

        val_schema = get_property_schema(property_=val)
        type_dict = types_generator(key_dict=val_schema)
        python_name = convert_camel_case_to_snake_case(name=f"{dict_key}_{key}" if key in keys_to_rename else key)

        # Sanitize Python reserved keywords
        safe_python_name, original_name = sanitize_python_name(name=python_name)
        is_keyword_renamed = safe_python_name != original_name

        resource_dict[dict_key].append({
            "name-for-class-arg": safe_python_name,
            "property-name": key,
            "original-python-name": python_name,  # Store original for reference
            "is-keyword-renamed": is_keyword_renamed,  # Flag for template
            "required": key in required,
            "description": format_description(description=val_schema.get("description", MISSING_DESCRIPTION_STR)),
            "type-for-docstring": type_dict["type-for-doc"],
            "type-for-class-arg": f"{safe_python_name}: {type_dict['type-for-init']}",
        })

    return resource_dict


def parse_explain(
    kind: str,
) -> list[dict[str, Any]]:
    _schema_definition = read_resources_mapping_file()
    _resources: list[dict[str, Any]] = []

    _kinds_schema = _schema_definition[kind.lower()]
    for _kind_schema in _kinds_schema:
        namespaced = _kind_schema["namespaced"]
        resource_dict: dict[str, Any] = {
            "base_class": "NamespacedResource" if namespaced else "Resource",
            "description": _kind_schema.get("description", MISSING_DESCRIPTION_STR),
            "fields": [],
            "spec": [],
        }

        schema_properties: dict[str, Any] = _kind_schema.get("properties", {})

        # If the mapping doesn't have properties, try to read from the schema file
        if not schema_properties:
            schema_file = Path(SCHEMA_DIR) / f"{kind.lower()}.json"
            if schema_file.exists():
                with open(schema_file, "r") as f:
                    full_schema = json.load(f)
                    schema_properties = full_schema.get("properties", {})
                    # Update the description if available
                    if full_schema.get("description"):
                        resource_dict["description"] = full_schema["description"]

        fields_required = _kind_schema.get("required", [])

        resource_dict.update(extract_group_kind_version(_kind_schema=_kind_schema))

        if spec_schema := schema_properties.get("spec", {}):
            spec_schema = get_property_schema(property_=spec_schema)
            spec_required = spec_schema.get("required", [])
            resource_dict = prepare_property_dict(
                schema=spec_schema.get("properties", {}),
                required=spec_required,
                resource_dict=resource_dict,
                dict_key="spec",
            )

        resource_dict = prepare_property_dict(
            schema=schema_properties,
            required=fields_required,
            resource_dict=resource_dict,
            dict_key="fields",
        )

        api_group_real_name = resource_dict.get("group")
        # If API Group is not present in resource, try to get it from VERSION
        if not api_group_real_name:
            version_splited = resource_dict["version"].split("/")
            if len(version_splited) == 2:
                api_group_real_name = version_splited[0]

        if api_group_real_name:
            api_group_for_resource_api_group = api_group_real_name.upper().replace(".", "_").replace("-", "_")
            resource_dict["group"] = api_group_for_resource_api_group
            missing_api_group_in_resource: bool = not hasattr(Resource.ApiGroup, api_group_for_resource_api_group)

            if missing_api_group_in_resource:
                LOGGER.warning(
                    f"Missing API Group in Resource\n"
                    f"Please add `Resource.ApiGroup.{api_group_for_resource_api_group} = {api_group_real_name}` "
                    "manually into ocp_resources/resource.py under Resource class > ApiGroup class."
                )

        else:
            api_version_for_resource_api_version = resource_dict["version"].upper()
            missing_api_version_in_resource: bool = not hasattr(
                Resource.ApiVersion, api_version_for_resource_api_version
            )

            if missing_api_version_in_resource:
                LOGGER.warning(
                    f"Missing API Version in Resource\n"
                    f"Please add `Resource.ApiVersion.{api_version_for_resource_api_version} = {resource_dict['version']}` "
                    "manually into ocp_resources/resource.py under Resource class > ApiGroup class."
                )

        _resources.append(resource_dict)

    return _resources


def extract_group_kind_version(_kind_schema: dict[str, Any]) -> dict[str, str]:
    group_kind_versions: list[dict[str, str]] = _kind_schema["x-kubernetes-group-version-kind"]
    group_kind_version = group_kind_versions[0]

    for group_kind_version in group_kind_versions:
        if group_kind_version.get("group"):
            break

    return group_kind_version


def class_generator(
    kind: str,
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    output_dir: str = "",
    add_tests: bool = False,
    called_from_cli: bool = True,
    update_schema_executed: bool = False,
) -> list[str]:
    """
    Generates a class for a given Kind.
    """
    LOGGER.info(f"Generating class for {kind}")
    kind = kind.lower()
    kind_and_namespaced_mappings = read_resources_mapping_file().get(kind)
    if not kind_and_namespaced_mappings:
        if called_from_cli:
            if update_schema_executed:
                LOGGER.error(f"{kind} not found in {RESOURCES_MAPPING_FILE} after update-schema executed.")
                sys.exit(1)

            run_update_schema = input(
                f"{kind} not found in {RESOURCES_MAPPING_FILE}, Do you want to run --update-schema and retry? [Y/N]"
            )
            if run_update_schema.lower() == "n":
                sys.exit(1)

            elif run_update_schema.lower() == "y":
                update_kind_schema()

                return class_generator(
                    overwrite=overwrite,
                    dry_run=dry_run,
                    kind=kind,
                    output_file=output_file,
                    output_dir=output_dir,
                    add_tests=add_tests,
                    called_from_cli=True,
                    update_schema_executed=True,
                )

        else:
            LOGGER.error(f"{kind} not found in {RESOURCES_MAPPING_FILE}, Please run --update-schema.")
            return []

    resources = parse_explain(kind=kind)

    use_output_file_suffix: bool = len(resources) > 1
    generated_files: list[str] = []
    for resource_dict in resources:
        output_file_suffix = resource_dict["group"].lower() if use_output_file_suffix else ""

        orig_filename, generated_py_file = generate_resource_file_from_dict(
            resource_dict=resource_dict,
            overwrite=overwrite,
            dry_run=dry_run,
            output_file=output_file,
            add_tests=add_tests,
            output_file_suffix=output_file_suffix,
            output_dir=output_dir,
        )

        if not dry_run:
            run_command(
                command=shlex.split(f"uvx pre-commit run --files {generated_py_file}"),
                verify_stderr=False,
                check=False,
            )

            if orig_filename != generated_py_file and filecmp.cmp(orig_filename, generated_py_file):
                LOGGER.warning(f"File {orig_filename} was not updated, deleting {generated_py_file}")
                Path.unlink(Path(generated_py_file))

        generated_files.append(generated_py_file)

    return generated_files


def write_and_format_rendered(filepath: str, output: str) -> None:
    with open(filepath, "w") as fd:
        fd.write(output)

    for op in ("format", "check"):
        run_command(
            command=shlex.split(f"uvx ruff {op} {filepath}"),
            verify_stderr=False,
            check=False,
        )


def generate_class_generator_tests() -> None:
    tests_info: dict[str, list[dict[str, str]]] = {"template": []}
    dirs_to_ignore: list[str] = ["__pycache__"]

    for _dir in os.listdir(TESTS_MANIFESTS_DIR):
        if _dir in dirs_to_ignore:
            continue

        dir_path = os.path.join(TESTS_MANIFESTS_DIR, _dir)
        if os.path.isdir(dir_path):
            test_data = {"kind": _dir}

            for _file in os.listdir(dir_path):
                if _file.endswith("_res.py"):
                    test_data["res_file"] = _file

            tests_info["template"].append(test_data)

    rendered = render_jinja_template(
        template_dict=tests_info,
        template_dir=TESTS_MANIFESTS_DIR,
        template_name="test_parse_explain.j2",
    )

    write_and_format_rendered(
        filepath=os.path.join(Path(TESTS_MANIFESTS_DIR).parent, "test_class_generator.py"),
        output=rendered,
    )


@cloup.command("Resource class generator", show_constraints=True)
@cloup.option(
    "-k",
    "--kind",
    type=cloup.STRING,
    help="""
    \b
    The Kind to generate the class for, Needs working cluster with admin privileges.
    multiple kinds can be sent separated by comma (without psaces)
    Example: -k Deployment,Pod,ConfigMap
""",
)
@cloup.option(
    "-o",
    "--output-file",
    help="The full filename path to generate a python resource file. If not sent, resource kind will be used",
    type=cloup.Path(),
)
@cloup.option(
    "--overwrite",
    is_flag=True,
    help="Output file overwrite existing file if passed",
)
@cloup.option("--dry-run", is_flag=True, help="Run the script without writing to file")
@cloup.option(
    "--add-tests",
    help=f"Add a test to `test_class_generator.py` and test files to `{TESTS_MANIFESTS_DIR}` dir",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--update-schema",
    help="Update kind schema files",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--discover-missing",
    help="Discover resources in the cluster that don't have wrapper classes",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--coverage-report",
    help="Generate a coverage report of implemented vs discovered resources",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--json",
    "json_output",
    help="Output reports in JSON format",
    is_flag=True,
    default=False,
    show_default=True,
)
@cloup.option(
    "--generate-missing",
    help="Generate classes for all missing resources after discovery",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--use-cache/--no-cache",
    help="Use cached discovery results if available",
    default=True,
    show_default=True,
)
@cloup.constraint(
    If("update_schema", then=accept_none),
    [
        "add_tests",
        "dry_run",
        "kind",
        "output_file",
        "overwrite",
        "discover_missing",
        "coverage_report",
        "generate_missing",
    ],
)
@cloup.constraint(
    If(
        IsSet("add_tests"),
        then=accept_none,
    ),
    ["output_file", "dry_run", "update_schema", "overwrite"],
)
@cloup.constraint(require_one, ["kind", "update_schema", "discover_missing", "coverage_report"])
def main(
    kind: str,
    overwrite: bool,
    dry_run: bool,
    output_file: str,
    add_tests: bool,
    update_schema: bool,
    discover_missing: bool,
    coverage_report: bool,
    json_output: bool,
    generate_missing: bool,
    use_cache: bool,
) -> None:
    if update_schema:
        return update_kind_schema()

    # Handle discovery and coverage report options
    if discover_missing or coverage_report:
        # Set up cache file path
        cache_dir = os.path.expanduser("~/.cache/openshift-python-wrapper")
        try:
            os.makedirs(cache_dir, exist_ok=True)
        except OSError as e:
            LOGGER.error(f"Failed to create cache directory '{cache_dir}': {e}")
            # Fall back to temporary directory if cache directory creation fails
            cache_dir = os.path.join(gettempdir(), "openshift-python-wrapper-cache")
            try:
                os.makedirs(cache_dir, exist_ok=True)
                LOGGER.warning(f"Using fallback cache directory: {cache_dir}")
            except OSError as fallback_e:
                LOGGER.error(f"Failed to create fallback cache directory: {fallback_e}")
                # Disable cache usage if both attempts fail
                use_cache = False
                LOGGER.warning("Cache functionality disabled due to directory creation failures")

        cache_file = os.path.join(cache_dir, "discovery_cache.json") if use_cache else None

        # Check cache if enabled
        discovered_resources = None
        if use_cache and cache_file and os.path.exists(cache_file):
            try:
                # Check cache age (24 hours)
                cache_age = time.time() - os.path.getmtime(cache_file)
                if cache_age < 86400:  # 24 hours
                    with open(cache_file, "r") as f:
                        cached_data = json.load(f)
                    discovered_resources = cached_data.get("discovered_resources")
                    LOGGER.info("Using cached discovery results")
            except Exception as e:
                LOGGER.warning(f"Failed to load cache: {e}")

        # Discover resources if not cached
        if discovered_resources is None:
            try:
                LOGGER.info("Discovering cluster resources...")
                discovered_resources = discover_cluster_resources()

                # Cache the results
                if use_cache and cache_file:
                    try:
                        with open(cache_file, "w") as f:
                            json.dump(
                                {"discovered_resources": discovered_resources, "timestamp": time.time()}, f, indent=2
                            )
                    except Exception as e:
                        LOGGER.warning(f"Failed to cache results: {e}")
            except Exception as e:
                LOGGER.error(f"Failed to discover resources: {e}")
                sys.exit(1)

        # Analyze coverage
        coverage_analysis = analyze_coverage(discovered_resources=discovered_resources)

        # Generate report if requested
        if coverage_report or discover_missing:
            output_format = "json" if json_output else "human"
            report = generate_report(coverage_analysis=coverage_analysis, output_format=output_format)
            print(report)

        # Generate missing resources if requested
        if generate_missing and coverage_analysis["missing_resources"]:
            LOGGER.info(f"Generating {len(coverage_analysis['missing_resources'])} missing resources...")

            # Group by API version for batch generation
            api_groups: dict[str, list[str]] = {}
            for resource in coverage_analysis["missing_resources"]:
                api_version = resource.get("api_version", "")
                kind_name = resource.get("kind", "")
                if api_version not in api_groups:
                    api_groups[api_version] = []
                api_groups[api_version].append(kind_name)

            # Generate classes
            for api_version, kinds in api_groups.items():
                if kinds:
                    LOGGER.info(f"Generating resources for {api_version}: {', '.join(kinds)}")
                    # Call class_generator for batch of kinds
                    # Reuse the existing generation logic
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        gen_futures = []
                        for _kind in kinds:
                            gen_futures.append(
                                executor.submit(
                                    class_generator,
                                    kind=_kind,
                                    overwrite=overwrite,
                                    dry_run=dry_run,
                                    output_file="",
                                    add_tests=add_tests,
                                    called_from_cli=False,
                                )
                            )

                        for future in as_completed(gen_futures):
                            try:
                                future.result()
                            except Exception as e:
                                LOGGER.error(f"Failed to generate resource: {e}")

        # Exit if we only did discovery/report
        if not kind:
            return

    _kwargs: dict[str, Any] = {
        "overwrite": overwrite,
        "dry_run": dry_run,
        "output_file": output_file,
        "add_tests": add_tests,
    }

    kind_list: list[str] = kind.split(",")
    futures: list[Future] = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for _kind in kind_list:
            _kwargs["kind"] = _kind

            if len(kind_list) == 1:
                class_generator(**_kwargs)

            else:
                futures.append(
                    executor.submit(
                        class_generator,
                        kind=_kwargs["kind"],
                        overwrite=overwrite,
                        dry_run=dry_run,
                        output_file=output_file,
                        add_tests=add_tests,
                    )
                )

        for _ in as_completed(futures):
            # wait for all tasks to complete
            pass

    if add_tests:
        generate_class_generator_tests()
        pytest.main(["-k", "test_class_generator"])


if __name__ == "__main__":
    main()
