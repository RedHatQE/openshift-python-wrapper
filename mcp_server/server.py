#!/usr/bin/env python
"""
MCP Server for OpenShift Python Wrapper (ocp_resources)

This MCP server provides tools to interact with OpenShift/Kubernetes resources
using the ocp_resources library through the Model Context Protocol.
"""

import importlib
import inspect
import io
import os
import tempfile
import traceback
from pathlib import Path
from typing import Any

import yaml
from fastmcp import FastMCP
from simple_logger.logger import get_logger, logging

import ocp_resources
from ocp_resources.event import Event
from ocp_resources.exceptions import ExecOnPodError
from ocp_resources.pod import Pod

# OpenShift specific resources
# Import ocp_resources modules
from ocp_resources.resource import NamespacedResource, Resource, get_client

# Configure logging to show debug messages
log_file = os.path.join(tempfile.gettempdir(), "mcp_server_debug.log")
LOGGER = get_logger(name=__name__, filename=log_file, level=logging.DEBUG)

# Initialize the MCP server
mcp = FastMCP(name="openshift-python-wrapper")

# Global client variable
_client = None


def get_dynamic_client(fake: bool = False) -> Any:
    """Get or create a dynamic client for Kubernetes/OpenShift"""
    global _client
    if _client is None:
        LOGGER.debug("Creating new dynamic client")
        _client = get_client(fake=fake)
    return _client


def _scan_resource_classes():
    """Scan ocp_resources modules and return a dict mapping resource types to their classes."""
    resource_map = {}
    LOGGER.debug("Starting to scan ocp_resources module for resource types")

    # Get the ocp_resources directory path
    ocp_resources_path = Path(ocp_resources.__file__).parent

    # Scan all .py files in the ocp_resources directory
    for file_path in ocp_resources_path.glob("*.py"):
        if file_path.name.startswith("_") or file_path.name == "utils.py":
            continue

        module_name = file_path.stem
        try:
            # Import the module dynamically
            module = importlib.import_module(f"ocp_resources.{module_name}")

            # Look for classes in the module
            for name in dir(module):
                if name.startswith("_"):
                    continue

                obj = getattr(module, name)
                if inspect.isclass(obj) and hasattr(obj, "kind"):
                    try:
                        if obj.kind:  # Some base classes might not have a kind
                            resource_type = obj.kind.lower()
                            # Store the class in the map (later occurrences override earlier ones)
                            resource_map[resource_type] = obj
                            LOGGER.debug(f"Added resource type from {module_name}: {resource_type}")
                    except Exception as e:
                        LOGGER.debug(f"Error processing {name} in {module_name}: {e}")
                        continue
        except Exception as e:
            LOGGER.debug(f"Error importing module {module_name}: {e}")
            continue

    LOGGER.debug(f"Found {len(resource_map)} resource types total")
    return resource_map


def _get_available_resource_types():
    """Get all available resource types from the resource map."""
    return sorted(RESOURCE_CLASS_MAP.keys())


# Use it in the server initialization
# Initialize resource class map and available resource types
RESOURCE_CLASS_MAP = _scan_resource_classes()
RESOURCE_TYPES = _get_available_resource_types()
LOGGER.info(f"Available resource types: {RESOURCE_TYPES}")
LOGGER.info(f"Total resource types found: {len(RESOURCE_TYPES)}")


def get_resource_class(resource_type: str) -> type[Resource] | None:
    """Get the resource class for a given resource type"""
    # Convert resource_type to lowercase for comparison
    resource_type_lower = resource_type.lower()

    # Look up the resource class in the pre-scanned map
    resource_class = RESOURCE_CLASS_MAP.get(resource_type_lower)

    if resource_class:
        LOGGER.debug(f"Found resource class for type {resource_type}")
        return resource_class

    LOGGER.warning(f"Resource type '{resource_type}' not found in RESOURCE_CLASS_MAP")
    return None


def _validate_resource_type(resource_type: str) -> tuple[type[Resource] | None, dict[str, Any] | None]:
    """Validate resource type and return (resource_class, error_dict) tuple."""
    resource_class = get_resource_class(resource_type=resource_type)
    if not resource_class:
        return None, {"error": f"Unknown resource type: {resource_type}", "available_types": RESOURCE_TYPES}
    return resource_class, None


def _create_resource_instance(
    resource_class: type[Resource],
    name: str,
    namespace: str | None = None,
    client: Any | None = None,
) -> tuple[Any, dict[str, Any] | None]:
    """Create a resource instance with proper namespace handling.
    Returns (resource, error_dict) tuple."""
    if client is None:
        client = get_dynamic_client()

    # Check if resource is namespaced
    is_namespaced = issubclass(resource_class, NamespacedResource)
    if is_namespaced and not namespace:
        return None, {"error": f"Namespace is required for {resource_class.kind} resources"}

    # Create resource instance
    kwargs = {"name": name, "client": client}
    if is_namespaced:
        kwargs["namespace"] = namespace

    resource = resource_class(**kwargs)
    return resource, None


def _format_not_found_error(resource_type: str, name: str, namespace: str | None = None) -> dict[str, Any]:
    """Format a consistent not found error message."""
    return {"error": f"{resource_type} '{name}' not found" + (f" in namespace '{namespace}'" if namespace else "")}


def _format_exception_error(action: str, resource_info: str, exception: Exception) -> dict[str, Any]:
    """Format a consistent exception error message.

    Args:
        action: The action that failed (e.g., "Failed to create", "Failed to get")
        resource_info: Resource description (e.g., "Pod 'my-pod'", "configmap")
        exception: The exception that occurred
    """
    return {"error": f"{action} {resource_info}: {str(exception)}", "type": type(exception).__name__}


def format_resource_info(resource: Any) -> dict[str, Any]:
    """Format resource information for output"""
    try:
        metadata = resource.instance.metadata
        status = getattr(resource.instance, "status", None)

        info = {
            "name": metadata.name,
            "namespace": getattr(metadata, "namespace", None),
            "uid": metadata.uid,
            "resourceVersion": metadata.resourceVersion,
            "creationTimestamp": metadata.creationTimestamp,
            "labels": dict(metadata.labels) if metadata.labels else {},
            "annotations": dict(metadata.annotations) if metadata.annotations else {},
        }

        if status:
            if hasattr(status, "phase"):
                info["phase"] = status.phase
            if hasattr(status, "conditions"):
                info["conditions"] = [dict(c) for c in status.conditions] if status.conditions else []

        return info
    except Exception as e:
        return {"name": getattr(resource, "name", "unknown"), "error": str(e)}


# Tools for resource management


@mcp.tool
def list_resources(
    resource_type: str,
    namespace: str | None = None,
    label_selector: str | None = None,
    field_selector: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """
    List Kubernetes/OpenShift resources of a specific type.

    Returns a list of resources with their basic information.
    """
    try:
        LOGGER.info(f"Listing resources: type={resource_type}, namespace={namespace}")
        # Validate resource type
        resource_class, error_response = _validate_resource_type(resource_type=resource_type)
        if error_response:
            return error_response

        client = get_dynamic_client()
        assert resource_class is not None  # Type checker hint - we already checked this above
        # Build kwargs for the get method
        kwargs: dict[str, Any] = {}
        if namespace:
            kwargs["namespace"] = namespace
        if label_selector:
            kwargs["label_selector"] = label_selector
        if field_selector:
            kwargs["field_selector"] = field_selector
        if limit:
            kwargs["limit"] = limit

        resources = []
        for resource in resource_class.get(dyn_client=client, **kwargs):
            resources.append(format_resource_info(resource))

        return {
            "resource_type": resource_type,
            "namespace": namespace or "all",
            "count": len(resources),
            "resources": resources,
        }
    except Exception as e:
        return _format_exception_error("Failed to list", f"{resource_type} resources", e)


@mcp.tool
def get_resource(
    resource_type: str,
    name: str,
    namespace: str | None = None,
    output_format: str = "info",
) -> dict[str, Any]:
    """
    Get a specific Kubernetes/OpenShift resource by name.

    Returns detailed information about the resource.
    """
    try:
        # Validate resource type
        resource_class, error_response = _validate_resource_type(resource_type=resource_type)
        if error_response:
            return error_response

        client = get_dynamic_client()
        assert resource_class is not None  # Type checker hint - we already validated this
        resource_instance, error = _create_resource_instance(
            resource_class=resource_class, name=name, namespace=namespace, client=client
        )
        if error:
            return error

        if not resource_instance.exists:
            return _format_not_found_error(resource_type=resource_type, name=name, namespace=namespace)

        if output_format == "yaml":
            return {
                "resource_type": resource_type,
                "name": name,
                "namespace": namespace,
                "yaml": yaml.dump(resource_instance.instance.to_dict(), default_flow_style=False),
            }
        elif output_format == "json":
            return {
                "resource_type": resource_type,
                "name": name,
                "namespace": namespace,
                "json": resource_instance.instance.to_dict(),
            }
        else:  # info format
            info = format_resource_info(resource_instance)
            info["resource_type"] = resource_type

            # Add resource-specific information
            if resource_type.lower() == "pod":
                info["node"] = getattr(resource_instance.instance.spec, "nodeName", None)
                info["containers"] = (
                    [c.name for c in resource_instance.instance.spec.containers]
                    if hasattr(resource_instance.instance.spec, "containers")
                    else []
                )

                # Get container statuses
                if hasattr(resource_instance.instance.status, "containerStatuses"):
                    info["container_statuses"] = []
                    for cs in resource_instance.instance.status.containerStatuses:
                        status_info = {
                            "name": cs.name,
                            "ready": cs.ready,
                            "restartCount": cs.restartCount,
                        }
                        if cs.state.running:
                            status_info["state"] = "running"
                        elif cs.state.waiting:
                            status_info["state"] = "waiting"
                            status_info["reason"] = cs.state.waiting.reason
                        elif cs.state.terminated:
                            status_info["state"] = "terminated"
                            status_info["reason"] = cs.state.terminated.reason
                        info["container_statuses"].append(status_info)

            elif resource_type.lower() == "deployment":
                if hasattr(resource_instance.instance.status, "replicas"):
                    info["replicas"] = resource_instance.instance.status.replicas
                    info["readyReplicas"] = getattr(resource_instance.instance.status, "readyReplicas", 0)
                    info["availableReplicas"] = getattr(resource_instance.instance.status, "availableReplicas", 0)

            elif resource_type.lower() == "service":
                if hasattr(resource_instance.instance.spec, "type"):
                    info["type"] = resource_instance.instance.spec.type
                    info["clusterIP"] = resource_instance.instance.spec.clusterIP
                    info["ports"] = (
                        [
                            {"port": p.port, "targetPort": str(p.targetPort), "protocol": p.protocol}
                            for p in resource_instance.instance.spec.ports
                        ]
                        if hasattr(resource_instance.instance.spec, "ports")
                        else []
                    )

            return info
    except Exception as e:
        return _format_exception_error("Failed to get", f"{resource_type} '{name}'", e)


@mcp.tool
def create_resource(
    resource_type: str,
    name: str,
    namespace: str | None = None,
    yaml_content: str | None = None,
    spec: dict[str, Any] | None = None,
    labels: dict[str, str] | None = None,
    annotations: dict[str, str] | None = None,
    wait: bool = False,
) -> dict[str, Any]:
    """
    Create a new Kubernetes/OpenShift resource.

    You can provide either yaml_content or spec to define the resource.
    """
    try:
        if yaml_content and spec:
            return {"error": "Provide either yaml_content or spec, not both"}

        if not yaml_content and not spec:
            return {"error": "Either yaml_content or spec must be provided"}

        client = get_dynamic_client()

        if yaml_content:
            # Parse YAML content
            yaml_data = yaml.safe_load(io.StringIO(yaml_content))

            # Extract resource info from YAML
            resource_type = yaml_data.get("kind", resource_type).lower()
            name = yaml_data.get("metadata", {}).get("name", name)
            namespace = yaml_data.get("metadata", {}).get("namespace", namespace)

            resource_class, error_response = _validate_resource_type(resource_type=resource_type)
            if error_response:
                return error_response

            # Create resource from parsed YAML using kind_dict
            assert resource_class is not None  # Type checker hint
            kwargs = {"client": client, "kind_dict": yaml_data}
            resource_instance = resource_class(**kwargs)
        else:
            # Create resource from spec
            resource_class, error_response = _validate_resource_type(resource_type=resource_type)
            if error_response:
                return error_response

            # Check if resource is namespaced
            assert resource_class is not None  # Type checker hint
            is_namespaced = issubclass(resource_class, NamespacedResource)
            if is_namespaced and not namespace:
                return {"error": f"Namespace is required for {resource_type} resources"}

            # Build kwargs
            kwargs = {
                "name": name,
                "client": client,
                "label": labels,
                "annotations": annotations,
            }
            if is_namespaced:
                kwargs["namespace"] = namespace

            # Add spec-specific parameters based on resource type
            if spec:
                kwargs.update(spec)

            resource_instance = resource_class(**kwargs)

        # Deploy the resource
        resource_instance.deploy(wait=wait)

        return {
            "success": True,
            "resource_type": resource_type,
            "name": resource_instance.name,
            "namespace": getattr(resource_instance, "namespace", None),
            "message": f"{resource_type} '{resource_instance.name}' created successfully",
        }
    except Exception as e:
        return _format_exception_error("Failed to create", resource_type, e)


@mcp.tool
def update_resource(
    resource_type: str,
    name: str,
    patch: dict[str, Any],
    namespace: str | None = None,
    patch_type: str = "merge",
) -> dict[str, Any]:
    """
    Update an existing Kubernetes/OpenShift resource using a patch.

    The patch should be a dictionary containing the fields to update.
    """
    try:
        # Validate resource type
        resource_class, error_response = _validate_resource_type(resource_type=resource_type)
        if error_response:
            return error_response

        client = get_dynamic_client()
        assert resource_class is not None  # Type checker hint - we already validated this
        resource_instance, error = _create_resource_instance(
            resource_class=resource_class, name=name, namespace=namespace, client=client
        )
        if error:
            return error

        if not resource_instance.exists:
            return _format_not_found_error(resource_type=resource_type, name=name, namespace=namespace)

        # Apply the patch
        content_type = (
            "application/merge-patch+json" if patch_type == "merge" else "application/strategic-merge-patch+json"
        )
        resource_instance.api.patch(body=patch, namespace=namespace, content_type=content_type)

        return {
            "success": True,
            "resource_type": resource_type,
            "name": name,
            "namespace": namespace,
            "message": f"{resource_type} '{name}' updated successfully",
        }
    except Exception as e:
        return _format_exception_error("Failed to update", f"{resource_type} '{name}'", e)


@mcp.tool
def delete_resource(
    resource_type: str,
    name: str,
    namespace: str | None = None,
    wait: bool = True,
    timeout: int = 60,
) -> dict[str, Any]:
    """
    Delete a Kubernetes/OpenShift resource.
    """
    try:
        # Validate resource type
        resource_class, error_response = _validate_resource_type(resource_type=resource_type)
        if error_response:
            return error_response

        client = get_dynamic_client()
        assert resource_class is not None  # Type checker hint - we already validated this
        resource_instance, error = _create_resource_instance(
            resource_class=resource_class, name=name, namespace=namespace, client=client
        )
        if error:
            return error

        if not resource_instance.exists:
            return {
                "warning": f"{resource_type} '{name}' not found"
                + (f" in namespace '{namespace}'" if namespace else ""),
                "success": True,
            }

        # Delete the resource
        success = resource_instance.delete(wait=wait, timeout=timeout)

        return {
            "success": success,
            "resource_type": resource_type,
            "name": name,
            "namespace": namespace,
            "message": f"{resource_type} '{name}' deleted successfully"
            if success
            else f"Failed to delete {resource_type} '{name}'",
        }
    except Exception as e:
        return _format_exception_error("Failed to delete", f"{resource_type} '{name}'", e)


@mcp.tool
def get_pod_logs(
    name: str,
    namespace: str,
    container: str | None = None,
    previous: bool = False,
    since_seconds: int | None = None,
    tail_lines: int | None = None,
) -> dict[str, Any]:
    """
    Get logs from a pod container.
    """
    try:
        client = get_dynamic_client()
        pod = Pod(client=client, name=name, namespace=namespace)

        if not pod.exists:
            return _format_not_found_error(resource_type="Pod", name=name, namespace=namespace)

        # Build kwargs for log method
        kwargs: dict[str, Any] = {}
        if container:
            kwargs["container"] = container
        if previous:
            kwargs["previous"] = previous
        if tail_lines:
            kwargs["tail_lines"] = tail_lines
        if since_seconds:
            kwargs["since_seconds"] = since_seconds

        logs = pod.log(**kwargs)

        return {"pod": name, "namespace": namespace, "container": container, "logs": logs}
    except Exception as e:
        return _format_exception_error("Failed to get logs for", f"pod '{name}'", e)


@mcp.tool
def exec_in_pod(
    name: str,
    namespace: str,
    command: list[str],
    container: str | None = None,
) -> dict[str, Any]:
    """
    Execute a command in a pod container.
    """
    try:
        client = get_dynamic_client()
        pod = Pod(client=client, name=name, namespace=namespace)

        if not pod.exists:
            return _format_not_found_error(resource_type="Pod", name=name, namespace=namespace)

        # Execute command
        try:
            if container:
                stdout = pod.execute(command=command, container=container)
            else:
                stdout = pod.execute(command=command)

            return {
                "pod": name,
                "namespace": namespace,
                "container": container,
                "command": command,
                "stdout": stdout,
                "stderr": "",
                "returncode": 0,
            }
        except ExecOnPodError as e:
            return {
                "pod": name,
                "namespace": namespace,
                "container": container,
                "command": command,
                "stdout": e.out,
                "stderr": str(e.err),
                "returncode": e.rc,
            }
    except Exception as e:
        return _format_exception_error("Failed to execute command in", f"pod '{name}'", e)


def _build_event_field_selector(
    resource_class: Any,
    name: str,
    namespace: str | None,
    resource_type: str,
) -> str | None:
    """
    Build field selector for events with correct format.

    Args:
        resource_class: The resource class object
        name: Name of the resource
        namespace: Namespace of the resource
        resource_type: Type of the resource

    Returns:
        Field selector string or None
    """
    field_selectors = []
    if name:
        field_selectors.append(f"involvedObject.name=={name}")
    if namespace:
        field_selectors.append(f"involvedObject.namespace=={namespace}")
    if resource_type:
        # Get the correct Kind value from the resource class
        kind = resource_class.kind if resource_class else resource_type
        field_selectors.append(f"involvedObject.kind=={kind}")

    field_selector = ",".join(field_selectors) if field_selectors else None
    LOGGER.debug(f"Using field selector: {field_selector}")
    return field_selector


def _extract_event_info(watch_event: dict[str, Any]) -> dict[str, Any]:
    """
    Extract event information from a watch event.

    Args:
        watch_event: The watch event dictionary

    Returns:
        Dictionary containing extracted event information
    """
    # Debug logging to understand the structure
    LOGGER.debug(f"watch_event type: {type(watch_event)}")

    # Extract the event object from the watch event
    # The watch event is a dict with keys: ['type', 'object', 'raw_object']
    if isinstance(watch_event, dict) and "object" in watch_event:
        event_obj = watch_event["object"]
        event_type = watch_event.get("type", "UNKNOWN")  # ADDED, MODIFIED, DELETED
        LOGGER.debug(f"Watch event type: {event_type}, object type: {type(event_obj)}")
    else:
        # Fallback for unexpected structure
        event_obj = watch_event
        event_type = "UNKNOWN"

    # The event_obj is a kubernetes.dynamic.resource.ResourceInstance
    # We can access its attributes directly
    try:
        event_info = {
            "type": event_obj.type,
            "reason": event_obj.reason,
            "message": event_obj.message,
            "count": getattr(event_obj, "count", 1),
            "firstTimestamp": str(getattr(event_obj, "firstTimestamp", "")),
            "lastTimestamp": str(getattr(event_obj, "lastTimestamp", "")),
            "source": {
                "component": event_obj.source.get("component") if hasattr(event_obj, "source") else None,
                "host": event_obj.source.get("host") if hasattr(event_obj, "source") else None,
            },
            "involvedObject": {
                "kind": event_obj.involvedObject.get("kind") if hasattr(event_obj, "involvedObject") else None,
                "name": event_obj.involvedObject.get("name") if hasattr(event_obj, "involvedObject") else None,
                "namespace": event_obj.involvedObject.get("namespace")
                if hasattr(event_obj, "involvedObject")
                else None,
            },
        }
        LOGGER.debug(f"Successfully extracted event: {event_info['reason']} - {event_info['message'][:50]}...")
        return event_info
    except Exception as e:
        LOGGER.error(f"Failed to extract event data: {e}")
        # Try to get whatever we can
        return {
            "type": "Unknown",
            "reason": "ExtractionError",
            "message": str(e),
            "count": 0,
            "firstTimestamp": "",
            "lastTimestamp": "",
            "source": {"component": None, "host": None},
            "involvedObject": {"kind": None, "name": None, "namespace": None},
        }


def _process_watch_events(
    client: Any,
    namespace: str | None,
    field_selector: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    """
    Process watch events and collect event information.

    Args:
        client: Dynamic client instance
        namespace: Namespace of the resource
        field_selector: Field selector string
        limit: Maximum number of events to return

    Returns:
        List of event information dictionaries
    """
    events = []
    # Event.get() returns a generator of watch events
    for watch_event in Event.get(
        client,  # Pass as positional argument, not keyword
        namespace=namespace,
        field_selector=field_selector,
        timeout=5,  # Add timeout to avoid hanging
    ):
        event_info = _extract_event_info(watch_event=watch_event)
        events.append(event_info)

        if len(events) >= limit:
            break

    return events


@mcp.tool
def get_resource_events(
    resource_type: str,
    name: str,
    namespace: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """
    Get events related to a specific resource.

    Args:
        resource_type: Type of the resource (e.g., 'pod', 'deployment')
        name: Name of the resource
        namespace: Namespace of the resource
        limit: Maximum number of events to return (default: 10)

    Returns:
        Dictionary containing event information
    """
    try:
        LOGGER.info(f"Getting events for {resource_type}/{name} in namespace {namespace}")
        client = get_dynamic_client()

        # Validate resource type and get the resource class
        resource_class, error_response = _validate_resource_type(resource_type=resource_type)
        if error_response:
            return error_response

        # Build field selector for events
        field_selector = _build_event_field_selector(
            resource_class=resource_class, name=name, namespace=namespace, resource_type=resource_type
        )

        # Process watch events and collect event information
        events = _process_watch_events(client=client, namespace=namespace, field_selector=field_selector, limit=limit)

        return {
            "resource_type": resource_type,
            "name": name,
            "namespace": namespace,
            "event_count": len(events),
            "events": events,
        }
    except Exception as e:
        error_dict = _format_exception_error("Failed to get", "events", e)
        error_dict["traceback"] = traceback.format_exc()
        return error_dict


@mcp.tool
def apply_yaml(
    yaml_content: str,
    namespace: str | None = None,
) -> dict[str, Any]:
    """
    Apply YAML content containing one or more Kubernetes/OpenShift resources.
    """
    # Acknowledge parameter (reserved for future use)
    _ = namespace

    try:
        client = get_dynamic_client()
        results = []
        successful = 0
        failed = 0

        # Parse YAML content (could contain multiple documents)
        documents = yaml.safe_load_all(yaml_content)

        for doc in documents:
            if not doc:
                continue

            kind = doc.get("kind", "").lower()
            if not kind:
                results.append({"error": "Missing 'kind' field in YAML document", "success": False})
                failed += 1
                continue

            # Validate resource type
            resource_class, error_response = _validate_resource_type(resource_type=kind)
            if error_response:
                results.append({
                    "kind": kind,
                    "name": doc.get("metadata", {}).get("name", "unknown"),
                    "error": error_response.get("error", f"Unknown resource type: {kind}"),
                    "success": False,
                })
                failed += 1
                continue

            try:
                # Create resource using kind_dict which is more efficient than YAML string
                assert resource_class is not None  # Type checker hint
                kwargs = {"client": client, "kind_dict": doc}
                resource_instance = resource_class(**kwargs)
                resource_instance.deploy()

                results.append({
                    "kind": kind,
                    "name": resource_instance.name,
                    "namespace": getattr(resource_instance, "namespace", None),
                    "success": True,
                    "message": f"Created {kind} '{resource_instance.name}'",
                })
                successful += 1
            except Exception as e:
                results.append({"kind": kind, "name": doc.get("metadata", {}).get("name", "unknown"), "error": str(e)})
                failed += 1

        # Summary
        return {"total_resources": len(results), "successful": successful, "failed": failed, "results": results}
    except Exception as e:
        return _format_exception_error("Failed to apply", "YAML", e)


@mcp.tool
def get_resource_types(random_string: str) -> dict[str, Any]:
    """
    Get a list of all available resource types that can be managed.

    Args:
        random_string: This parameter is required by the MCP protocol but is not used
                     in this implementation and may be ignored.

    Returns:
        Dictionary containing available resource types and their categories
    """
    # Acknowledge MCP protocol parameter (required but unused)
    _ = random_string

    return {
        "resource_types": sorted(RESOURCE_TYPES),  # RESOURCE_TYPES is already a list
        "total_count": len(RESOURCE_TYPES),
        "categories": {
            "workloads": ["pod", "deployment", "replicaset", "daemonset", "job", "cronjob"],
            "services": ["service", "route", "networkpolicy"],
            "config": ["configmap", "secret"],
            "storage": ["persistentvolume", "persistentvolumeclaim", "storageclass"],
            "rbac": ["serviceaccount", "role", "rolebinding", "clusterrole", "clusterrolebinding"],
            "cluster": ["namespace", "node", "event", "limitrange", "resourcequota"],
            "custom": ["customresourcedefinition"],
            "openshift": ["project", "route", "imagestream", "template"],
        },
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
