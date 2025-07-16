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
from typing import Any, Type

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


def get_dynamic_client(config_file: str | None = None, context: str | None = None) -> Any:
    """Get or create a dynamic client for Kubernetes/OpenShift"""
    global _client
    if _client is None:
        LOGGER.debug("Creating new dynamic client")
        _client = get_client(config_file=config_file, context=context)
    return _client


def _get_available_resource_types():
    """Dynamically get all available resource types from ocp_resources module."""
    resource_types = []
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
                if inspect.isclass(obj) and hasattr(obj, "kind") and hasattr(obj, "api_group"):
                    try:
                        if obj.kind:  # Some base classes might not have a kind
                            resource_types.append(obj.kind.lower())
                            LOGGER.debug(f"Added resource type from {module_name}: {obj.kind.lower()}")
                    except Exception as e:
                        LOGGER.debug(f"Error processing {name} in {module_name}: {e}")
                        continue
        except Exception as e:
            LOGGER.debug(f"Error importing module {module_name}: {e}")
            continue

    LOGGER.debug(f"Found {len(resource_types)} resource types total")
    return sorted(set(resource_types))


# Use it in the server initialization
RESOURCE_TYPES = _get_available_resource_types()
LOGGER.info(f"Available resource types: {RESOURCE_TYPES}")
LOGGER.info(f"Total resource types found: {len(RESOURCE_TYPES)}")


def get_resource_class(resource_type: str) -> Type[Resource] | None:
    """Get the resource class for a given resource type"""
    # Convert resource_type to lowercase for comparison
    resource_type_lower = resource_type.lower()

    # Check if the resource type exists in our list
    if resource_type_lower not in RESOURCE_TYPES:
        LOGGER.warning(f"Resource type '{resource_type}' not found in RESOURCE_TYPES")
        return None

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
                        if obj.kind and obj.kind.lower() == resource_type_lower:
                            LOGGER.debug(
                                f"Found resource class {name} in module {module_name} for type {resource_type}"
                            )
                            return obj
                    except Exception:
                        continue
        except Exception:
            continue

    LOGGER.warning(f"Could not find class for resource type '{resource_type}'")
    return None


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
        resource_class = get_resource_class(resource_type=resource_type)
        if not resource_class:
            return {"error": f"Unknown resource type: {resource_type}", "available_types": RESOURCE_TYPES}

        client = get_dynamic_client()

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
        assert resource_class is not None  # Type checker hint - we already checked this above
        for resource in resource_class.get(dyn_client=client, **kwargs):
            resources.append(format_resource_info(resource))

        return {
            "resource_type": resource_type,
            "namespace": namespace or "all",
            "count": len(resources),
            "resources": resources,
        }
    except Exception as e:
        return {"error": f"Failed to list {resource_type} resources: {str(e)}", "type": type(e).__name__}


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
        resource_class = get_resource_class(resource_type=resource_type)
        if not resource_class:
            return {"error": f"Unknown resource type: {resource_type}", "available_types": RESOURCE_TYPES}

        client = get_dynamic_client()

        # Check if resource is namespaced
        is_namespaced = issubclass(resource_class, NamespacedResource)
        if is_namespaced and not namespace:
            return {"error": f"Namespace is required for {resource_type} resources"}

        # Create resource instance
        kwargs = {"name": name, "client": client}
        if is_namespaced:
            kwargs["namespace"] = namespace

        resource = resource_class(**kwargs)

        if not resource.exists:
            return {
                "error": f"{resource_type} '{name}' not found" + (f" in namespace '{namespace}'" if namespace else "")
            }

        if output_format == "yaml":
            return {
                "resource_type": resource_type,
                "name": name,
                "namespace": namespace,
                "yaml": yaml.dump(resource.instance.to_dict(), default_flow_style=False),
            }
        elif output_format == "json":
            return {
                "resource_type": resource_type,
                "name": name,
                "namespace": namespace,
                "json": resource.instance.to_dict(),
            }
        else:  # info format
            info = format_resource_info(resource)
            info["resource_type"] = resource_type

            # Add resource-specific information
            if resource_type.lower() == "pod":
                info["node"] = getattr(resource.instance.spec, "nodeName", None)
                info["containers"] = (
                    [c.name for c in resource.instance.spec.containers]
                    if hasattr(resource.instance.spec, "containers")
                    else []
                )

                # Get container statuses
                if hasattr(resource.instance.status, "containerStatuses"):
                    info["container_statuses"] = []
                    for cs in resource.instance.status.containerStatuses:
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
                if hasattr(resource.instance.status, "replicas"):
                    info["replicas"] = resource.instance.status.replicas
                    info["readyReplicas"] = getattr(resource.instance.status, "readyReplicas", 0)
                    info["availableReplicas"] = getattr(resource.instance.status, "availableReplicas", 0)

            elif resource_type.lower() == "service":
                if hasattr(resource.instance.spec, "type"):
                    info["type"] = resource.instance.spec.type
                    info["clusterIP"] = resource.instance.spec.clusterIP
                    info["ports"] = (
                        [
                            {"port": p.port, "targetPort": str(p.targetPort), "protocol": p.protocol}
                            for p in resource.instance.spec.ports
                        ]
                        if hasattr(resource.instance.spec, "ports")
                        else []
                    )

            return info
    except Exception as e:
        return {"error": f"Failed to get {resource_type} '{name}': {str(e)}", "type": type(e).__name__}


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

            resource_class = get_resource_class(resource_type=resource_type)
            if not resource_class:
                return {
                    "error": f"Unknown resource type: {resource_type}",
                    "available_types": RESOURCE_TYPES,
                }

            # Create resource from parsed YAML using kind_dict
            kwargs = {"client": client, "kind_dict": yaml_data}
            resource = resource_class(**kwargs)
        else:
            # Create resource from spec
            resource_class = get_resource_class(resource_type=resource_type)
            if not resource_class:
                return {
                    "error": f"Unknown resource type: {resource_type}",
                    "available_types": RESOURCE_TYPES,
                }

            # Check if resource is namespaced
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

            resource = resource_class(**kwargs)

        # Deploy the resource
        resource.deploy(wait=wait)

        return {
            "success": True,
            "resource_type": resource_type,
            "name": resource.name,
            "namespace": getattr(resource, "namespace", None),
            "message": f"{resource_type} '{resource.name}' created successfully",
        }
    except Exception as e:
        return {"error": f"Failed to create {resource_type}: {str(e)}", "type": type(e).__name__}


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
        resource_class = get_resource_class(resource_type=resource_type)
        if not resource_class:
            return {"error": f"Unknown resource type: {resource_type}", "available_types": RESOURCE_TYPES}

        client = get_dynamic_client()

        # Check if resource is namespaced
        is_namespaced = issubclass(resource_class, NamespacedResource)
        if is_namespaced and not namespace:
            return {"error": f"Namespace is required for {resource_type} resources"}

        # Create resource instance
        kwargs = {"name": name, "client": client}
        if is_namespaced:
            kwargs["namespace"] = namespace

        resource = resource_class(**kwargs)

        if not resource.exists:
            return {
                "error": f"{resource_type} '{name}' not found" + (f" in namespace '{namespace}'" if namespace else "")
            }

        # Apply the patch
        content_type = (
            "application/merge-patch+json" if patch_type == "merge" else "application/strategic-merge-patch+json"
        )
        resource.api.patch(body=patch, namespace=namespace, content_type=content_type)

        return {
            "success": True,
            "resource_type": resource_type,
            "name": name,
            "namespace": namespace,
            "message": f"{resource_type} '{name}' updated successfully",
        }
    except Exception as e:
        return {"error": f"Failed to update {resource_type} '{name}': {str(e)}", "type": type(e).__name__}


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
        resource_class = get_resource_class(resource_type=resource_type)
        if not resource_class:
            return {"error": f"Unknown resource type: {resource_type}", "available_types": RESOURCE_TYPES}

        client = get_dynamic_client()

        # Check if resource is namespaced
        is_namespaced = issubclass(resource_class, NamespacedResource)
        if is_namespaced and not namespace:
            return {"error": f"Namespace is required for {resource_type} resources"}

        # Create resource instance
        kwargs = {"name": name, "client": client}
        if is_namespaced:
            kwargs["namespace"] = namespace

        resource = resource_class(**kwargs)

        if not resource.exists:
            return {
                "warning": f"{resource_type} '{name}' not found"
                + (f" in namespace '{namespace}'" if namespace else ""),
                "success": True,
            }

        # Delete the resource
        success = resource.delete(wait=wait, timeout=timeout)

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
        return {"error": f"Failed to delete {resource_type} '{name}': {str(e)}", "type": type(e).__name__}


@mcp.tool
def get_pod_logs(
    name: str,
    namespace: str,
    container: str | None = None,
    previous: bool = False,
    tail_lines: int | None = None,
    since_seconds: int | None = None,
) -> dict[str, Any]:
    """
    Get logs from a pod container.
    """
    try:
        client = get_dynamic_client()
        pod = Pod(name=name, namespace=namespace, client=client)

        if not pod.exists:
            return {"error": f"Pod '{name}' not found in namespace '{namespace}'"}

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
        return {"error": f"Failed to get logs for pod '{name}': {str(e)}", "type": type(e).__name__}


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
        pod = Pod(name=name, namespace=namespace, client=client)

        if not pod.exists:
            return {"error": f"Pod '{name}' not found in namespace '{namespace}'"}

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
        return {"error": f"Failed to execute command in pod '{name}': {str(e)}", "type": type(e).__name__}


@mcp.tool
def get_resource_events(
    resource_type: str,
    name: str,
    namespace: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """
    Get events related to a specific resource.
    """
    try:
        LOGGER.info(f"Getting events for {resource_type}/{name} in namespace {namespace}")
        client = get_dynamic_client()

        # Build field selector for events with correct format
        field_selectors = []
        if name:
            field_selectors.append(f"involvedObject.name=={name}")
        if namespace:
            field_selectors.append(f"involvedObject.namespace=={namespace}")
        if resource_type:
            # Capitalize the resource type properly for the kind field
            kind = resource_type.title() if resource_type.lower() in ["pod", "service", "deployment"] else resource_type
            field_selectors.append(f"involvedObject.kind=={kind}")

        field_selector = ",".join(field_selectors) if field_selectors else None
        LOGGER.debug(f"Using field selector: {field_selector}")

        events = []
        # Event.get() returns a generator of watch events
        for watch_event in Event.get(
            client,  # Pass as positional argument, not keyword
            namespace=namespace,
            field_selector=field_selector,
            timeout=5,  # Add timeout to avoid hanging
        ):
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
                events.append(event_info)
                LOGGER.debug(f"Successfully extracted event: {event_info['reason']} - {event_info['message'][:50]}...")
            except Exception as e:
                LOGGER.error(f"Failed to extract event data: {e}")
                # Try to get whatever we can
                event_info = {
                    "type": "Unknown",
                    "reason": "ExtractionError",
                    "message": str(e),
                    "count": 0,
                    "firstTimestamp": "",
                    "lastTimestamp": "",
                    "source": {"component": None, "host": None},
                    "involvedObject": {"kind": None, "name": None, "namespace": None},
                }
                events.append(event_info)

            if len(events) >= limit:
                break

        return {
            "resource_type": resource_type,
            "name": name,
            "namespace": namespace,
            "event_count": len(events),
            "events": events,
        }
    except Exception as e:
        return {
            "error": f"Failed to get events: {str(e)}",
            "type": type(e).__name__,
            "traceback": traceback.format_exc(),
        }


@mcp.tool
def apply_yaml(
    yaml_content: str,
    namespace: str | None = None,
) -> dict[str, Any]:
    """
    Apply YAML content containing one or more Kubernetes/OpenShift resources.
    """
    try:
        client = get_dynamic_client()
        results = []

        # Parse YAML content (may contain multiple documents)
        yaml_docs = yaml.safe_load_all(io.StringIO(yaml_content))

        for doc in yaml_docs:
            if not doc:
                continue

            # Extract resource info
            kind = doc.get("kind", "").lower()
            name = doc.get("metadata", {}).get("name", "unknown")

            # If namespace is provided as parameter and not in the doc, add it
            if namespace and "namespace" not in doc.get("metadata", {}):
                if "metadata" not in doc:
                    doc["metadata"] = {}
                doc["metadata"]["namespace"] = namespace

            resource_class = get_resource_class(resource_type=kind)
            if not resource_class:
                results.append({"kind": kind, "name": name, "error": f"Unknown resource type: {kind}"})
                continue

            try:
                # Create resource using kind_dict which is more efficient than YAML string
                kwargs = {"client": client, "kind_dict": doc}
                resource = resource_class(**kwargs)
                resource.deploy()

                results.append({
                    "kind": kind,
                    "name": resource.name,
                    "namespace": getattr(resource, "namespace", None),
                    "success": True,
                    "message": f"Created {kind} '{resource.name}'",
                })
            except Exception as e:
                results.append({"kind": kind, "name": name, "error": str(e)})

        # Summary
        success_count = sum(1 for r in results if r.get("success"))
        error_count = len(results) - success_count

        return {"total_resources": len(results), "successful": success_count, "failed": error_count, "results": results}
    except Exception as e:
        return {"error": f"Failed to apply YAML: {str(e)}", "type": type(e).__name__}


@mcp.tool
def get_resource_types(random_string: str) -> dict[str, Any]:
    """
    Get a list of all available resource types that can be managed.
    """
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
