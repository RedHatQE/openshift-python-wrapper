"""Discovery functions for finding cluster resources and generated files."""

from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from kubernetes.dynamic import DynamicClient
from simple_logger.logger import get_logger

from class_generator.constants import END_OF_GENERATED_CODE
from class_generator.utils import ResourceScanner
from ocp_resources.resource import get_client

LOGGER = get_logger(name=__name__)


def discover_cluster_resources(
    client: DynamicClient | None = None, api_group_filter: str | None = None
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


def discover_generated_resources() -> list[dict[str, Any]]:
    """
    Discover all generated resource files in the ocp_resources directory.

    Returns:
        List of dictionaries containing:
        - path: Full path to the file
        - kind: Resource class name
        - filename: File name without extension
        - has_user_code: Whether file contains user modifications
    """
    # Reuse existing ResourceScanner
    scanner = ResourceScanner()
    resource_infos = scanner.scan_resources()

    resources = []
    for info in resource_infos:
        # Read file to check for user code
        try:
            with open(info.file_path, encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            LOGGER.warning(f"File not found: {info.file_path}, skipping...")
            continue
        except UnicodeDecodeError as e:
            LOGGER.error(f"Failed to decode file {info.file_path}: {e}, skipping...")
            continue
        except Exception as e:
            LOGGER.error(f"Unexpected error reading file {info.file_path}: {e}, skipping...")
            continue

        has_user_code = END_OF_GENERATED_CODE in content and len(content.split(END_OF_GENERATED_CODE)[1].strip()) > 0

        resources.append({
            "path": info.file_path,
            "kind": info.name,
            "filename": Path(info.file_path).stem,
            "has_user_code": has_user_code,
        })

    return resources
