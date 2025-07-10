#!/usr/bin/env python
"""
MCP Server for OpenShift Python Wrapper (ocp_resources)

This MCP server provides tools to interact with OpenShift/Kubernetes resources
using the ocp_resources library through the Model Context Protocol.
"""

from typing import Any

import yaml
from fastmcp import FastMCP

# Import ocp_resources modules
from ocp_resources.resource import NamespacedResource, get_client
from ocp_resources.namespace import Namespace
from ocp_resources.pod import Pod
from ocp_resources.deployment import Deployment
from ocp_resources.service import Service
from ocp_resources.config_map import ConfigMap
from ocp_resources.secret import Secret
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.job import Job
from ocp_resources.cron_job import CronJob
from ocp_resources.daemonset import DaemonSet
from ocp_resources.replica_set import ReplicaSet
from ocp_resources.service_account import ServiceAccount
from ocp_resources.role import Role
from ocp_resources.role_binding import RoleBinding
from ocp_resources.cluster_role import ClusterRole
from ocp_resources.cluster_role_binding import ClusterRoleBinding
from ocp_resources.network_policy import NetworkPolicy
from ocp_resources.storage_class import StorageClass
from ocp_resources.persistent_volume import PersistentVolume
from ocp_resources.node import Node
from ocp_resources.event import Event
from ocp_resources.limit_range import LimitRange
from ocp_resources.resource_quota import ResourceQuota
from ocp_resources.pod_disruption_budget import PodDisruptionBudget
from ocp_resources.priority_class import PriorityClass
from ocp_resources.custom_resource_definition import CustomResourceDefinition

# OpenShift specific resources
from ocp_resources.project_project_openshift_io import Project
from ocp_resources.route import Route
from ocp_resources.image_stream import ImageStream
from ocp_resources.template import Template

# Initialize the MCP server
mcp = FastMCP(name="openshift-python-wrapper")

# Global client variable
_client = None


def get_dynamic_client(config_file: str | None = None, context: str | None = None):
    """Get or create a dynamic client for Kubernetes/OpenShift"""
    global _client
    if _client is None:
        _client = get_client(config_file=config_file, context=context)
    return _client


# Resource type mapping
RESOURCE_TYPES = {
    "namespace": Namespace,
    "pod": Pod,
    "deployment": Deployment,
    "service": Service,
    "configmap": ConfigMap,
    "secret": Secret,
    "persistentvolumeclaim": PersistentVolumeClaim,
    "pvc": PersistentVolumeClaim,
    "job": Job,
    "cronjob": CronJob,
    "daemonset": DaemonSet,
    "replicaset": ReplicaSet,
    "serviceaccount": ServiceAccount,
    "role": Role,
    "rolebinding": RoleBinding,
    "clusterrole": ClusterRole,
    "clusterrolebinding": ClusterRoleBinding,
    "networkpolicy": NetworkPolicy,
    "storageclass": StorageClass,
    "persistentvolume": PersistentVolume,
    "pv": PersistentVolume,
    "node": Node,
    "event": Event,
    "limitrange": LimitRange,
    "resourcequota": ResourceQuota,
    "poddisruptionbudget": PodDisruptionBudget,
    "pdb": PodDisruptionBudget,
    "priorityclass": PriorityClass,
    "customresourcedefinition": CustomResourceDefinition,
    "crd": CustomResourceDefinition,
    # OpenShift specific
    "project": Project,
    "route": Route,
    "imagestream": ImageStream,
    "template": Template,
}


def get_resource_class(resource_type: str):
    """Get the resource class for a given resource type"""
    return RESOURCE_TYPES.get(resource_type.lower())


def format_resource_info(resource) -> dict[str, Any]:
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


@mcp.tool()
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
        resource_class = get_resource_class(resource_type)
        if not resource_class:
            return {"error": f"Unknown resource type: {resource_type}", "available_types": list(RESOURCE_TYPES.keys())}

        client = get_dynamic_client()

        # Build kwargs for the get method
        kwargs = {}
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
        return {"error": f"Failed to list {resource_type} resources: {str(e)}", "type": type(e).__name__}


@mcp.tool()
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
        resource_class = get_resource_class(resource_type)
        if not resource_class:
            return {"error": f"Unknown resource type: {resource_type}", "available_types": list(RESOURCE_TYPES.keys())}

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


@mcp.tool()
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
            import io

            yaml_data = yaml.safe_load(io.StringIO(yaml_content))

            # Extract resource info from YAML
            resource_type = yaml_data.get("kind", resource_type).lower()
            name = yaml_data.get("metadata", {}).get("name", name)
            namespace = yaml_data.get("metadata", {}).get("namespace", namespace)

            resource_class = get_resource_class(resource_type)
            if not resource_class:
                return {
                    "error": f"Unknown resource type: {resource_type}",
                    "available_types": list(RESOURCE_TYPES.keys()),
                }

            # Create resource from YAML
            kwargs = {"client": client, "yaml_file": io.StringIO(yaml_content)}
            resource = resource_class(**kwargs)
        else:
            # Create resource from spec
            resource_class = get_resource_class(resource_type)
            if not resource_class:
                return {
                    "error": f"Unknown resource type: {resource_type}",
                    "available_types": list(RESOURCE_TYPES.keys()),
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


@mcp.tool()
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
        resource_class = get_resource_class(resource_type)
        if not resource_class:
            return {"error": f"Unknown resource type: {resource_type}", "available_types": list(RESOURCE_TYPES.keys())}

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


@mcp.tool()
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
        resource_class = get_resource_class(resource_type)
        if not resource_class:
            return {"error": f"Unknown resource type: {resource_type}", "available_types": list(RESOURCE_TYPES.keys())}

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


@mcp.tool()
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
        kwargs = {}
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


@mcp.tool()
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
        result = pod.execute(command=command, container=container)

        return {
            "pod": name,
            "namespace": namespace,
            "container": container,
            "command": command,
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "returncode": result.get("returncode", 0),
        }
    except Exception as e:
        return {"error": f"Failed to execute command in pod '{name}': {str(e)}", "type": type(e).__name__}


@mcp.tool()
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
        client = get_dynamic_client()

        # Build field selector for events
        field_selectors = []
        if name:
            field_selectors.append(f"involvedObject.name={name}")
        if namespace:
            field_selectors.append(f"involvedObject.namespace={namespace}")
        if resource_type:
            field_selectors.append(f"involvedObject.kind={resource_type.title()}")

        field_selector = ",".join(field_selectors) if field_selectors else None

        events = []
        for event in Event.get(dyn_client=client, namespace=namespace, field_selector=field_selector, limit=limit):
            event_info = {
                "type": event.instance.type,
                "reason": event.instance.reason,
                "message": event.instance.message,
                "count": event.instance.count,
                "firstTimestamp": event.instance.firstTimestamp,
                "lastTimestamp": event.instance.lastTimestamp,
                "source": {
                    "component": getattr(event.instance.source, "component", None),
                    "host": getattr(event.instance.source, "host", None),
                },
            }
            events.append(event_info)

        return {
            "resource_type": resource_type,
            "name": name,
            "namespace": namespace,
            "event_count": len(events),
            "events": events,
        }
    except Exception as e:
        return {"error": f"Failed to get events: {str(e)}", "type": type(e).__name__}


@mcp.tool()
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
        import io

        yaml_docs = yaml.safe_load_all(io.StringIO(yaml_content))

        for doc in yaml_docs:
            if not doc:
                continue

            # Extract resource info
            kind = doc.get("kind", "").lower()
            name = doc.get("metadata", {}).get("name", "unknown")
            ns = doc.get("metadata", {}).get("namespace", namespace)

            resource_class = get_resource_class(kind)
            if not resource_class:
                results.append({"kind": kind, "name": name, "error": f"Unknown resource type: {kind}"})
                continue

            try:
                # Create resource from YAML
                yaml_str = yaml.dump(doc)
                kwargs = {"client": client, "yaml_file": io.StringIO(yaml_str)}
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


@mcp.tool()
def get_resource_types() -> dict[str, list[str]]:
    """
    Get a list of all available resource types that can be managed.
    """
    return {
        "resource_types": sorted(list(RESOURCE_TYPES.keys())),
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


# Add main entry point
if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
