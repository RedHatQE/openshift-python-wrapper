"""Status template methods for fake Kubernetes resources"""

from datetime import datetime, timezone
from typing import Any

from fake_kubernetes_client.status_schema_parser import StatusSchemaParser


def _get_ready_status_config(body: dict[str, Any]) -> tuple[str, str, str]:
    """
    Get ready status configuration from resource annotations or spec.

    Returns:
        tuple: (status, reason, message) - status is "True" or "False"
    """
    # Default to ready
    status = "True"
    reason = "ResourceReady"
    message = "Resource is ready"

    # Check annotations for test configuration
    metadata = body.get("metadata", {})
    annotations = metadata.get("annotations", {})

    # Allow configuration via annotation "fake-client.io/ready"
    if annotations.get("fake-client.io/ready", "").lower() == "false":
        status = "False"
        reason = "ResourceNotReady"
        message = "Resource is not ready"

    # Also check for a more specific ready status in spec
    if "readyStatus" in body.get("spec", {}):
        if body["spec"]["readyStatus"]:
            status = "True"
            reason = "ResourceReady"
            message = "Resource is ready"
        else:
            status = "False"
            reason = "ResourceNotReady"
            message = "Resource is not ready"

    return status, reason, message


def add_realistic_status(body: dict[str, Any], resource_mappings: dict[str, Any] | None = None) -> None:
    """Add realistic status to resources that need it"""
    kind = body.get("kind", "")

    # First check if we have a hardcoded template
    if kind == "Pod":
        status = get_pod_status_template(body=body)
    elif kind == "Deployment":
        status = get_deployment_status_template(body=body)
    elif kind == "Service":
        status = get_service_status_template(_body=body)
    elif kind == "Namespace":
        status = get_namespace_status_template(body=body)
    else:
        # Try schema-based generation if mappings are available
        if resource_mappings:
            status = generate_dynamic_status(body=body, resource_mappings=resource_mappings)
        else:
            # Fallback to generic status
            status = get_generic_status_template(body=body)

    if status:
        body["status"] = status


def generate_dynamic_status(body: dict[str, Any], resource_mappings: dict[str, Any]) -> dict[str, Any]:
    """Generate status dynamically based on resource schema"""
    kind = body.get("kind", "")
    api_version = body.get("apiVersion", "v1")

    parser = StatusSchemaParser(resource_mappings=resource_mappings)
    status_schema = parser.get_status_schema_for_resource(kind=kind, _api_version=api_version)

    if status_schema:
        return parser.generate_status_from_schema(schema=status_schema, resource_body=body)
    else:
        # Fallback to generic status
        return get_generic_status_template(body=body)


def get_pod_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get realistic Pod status"""
    container_name = "test-container"
    if "spec" in body and "containers" in body["spec"] and body["spec"]["containers"]:
        container_name = body["spec"]["containers"][0].get("name", "test-container")

    # For Pods, we need more specific configuration
    # Check for pod-specific annotation first, fall back to general ready annotation
    metadata = body.get("metadata", {})
    annotations = metadata.get("annotations", {})

    # Default to ready
    ready_status = "True"
    ready_reason = "ContainersReady"
    ready_message = "All containers are ready"
    container_ready = True
    container_started = True
    container_state = {"running": {"startedAt": datetime.now(timezone.utc).isoformat()}}

    # Check pod-specific annotation first
    if "fake-client.io/pod-ready" in annotations:
        if annotations["fake-client.io/pod-ready"].lower() == "false":
            ready_status = "False"
            ready_reason = "ContainersNotReady"
            ready_message = f"containers with unready status: [{container_name}]"
            container_ready = False
            container_started = False
            container_state = {"waiting": {"reason": "ContainerCreating"}}
    # Fall back to general ready annotation
    elif annotations.get("fake-client.io/ready", "").lower() == "false":
        ready_status = "False"
        ready_reason = "ContainersNotReady"
        ready_message = f"containers with unready status: [{container_name}]"
        container_ready = False
        container_started = False
        container_state = {"waiting": {"reason": "ContainerCreating"}}

    # Check spec.readyStatus
    if "readyStatus" in body.get("spec", {}):
        ready_status = "True" if body["spec"]["readyStatus"] else "False"
        if ready_status == "False":
            ready_reason = "ContainersNotReady"
            ready_message = f"containers with unready status: [{container_name}]"
            container_ready = False
            container_started = False
            container_state = {"waiting": {"reason": "ContainerCreating"}}
        else:
            ready_reason = "ContainersReady"
            ready_message = "All containers are ready"
            container_ready = True
            container_started = True
            container_state = {"running": {"startedAt": datetime.now(timezone.utc).isoformat()}}

    return {
        "phase": "Running",
        "conditions": [
            {
                "type": "Initialized",
                "status": "True",
                "lastProbeTime": None,
                "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                "reason": "PodCompleted",
            },
            {
                "type": "Ready",
                "status": ready_status,  # Now configurable, defaults to True
                "lastProbeTime": None,
                "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                "reason": ready_reason,
                "message": ready_message,
            },
            {
                "type": "ContainersReady",
                "status": ready_status,  # Should match Ready status
                "lastProbeTime": None,
                "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                "reason": ready_reason,
                "message": ready_message,
            },
            {
                "type": "PodScheduled",
                "status": "True",
                "lastProbeTime": None,
                "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                "reason": "PodScheduled",
            },
        ],
        "hostIP": "10.0.0.1",
        "podIP": "10.244.0.2",
        "podIPs": [{"ip": "10.244.0.2"}],
        "startTime": datetime.now(timezone.utc).isoformat(),
        "containerStatuses": [
            {
                "name": container_name,
                "state": container_state,
                "lastState": {},
                "ready": container_ready,
                "restartCount": 0,
                "image": "nginx:latest",
                "imageID": "docker://sha256:nginx",
                "containerID": "docker://1234567890abcdef" if container_ready else "",
                "started": container_started,
            }
        ],
    }


def get_deployment_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get realistic Deployment status"""
    # Get ready status configuration
    ready_status, _ready_reason, _ready_message = _get_ready_status_config(body=body)

    # Adjust deployment-specific values based on ready status
    if ready_status == "True":
        replicas = body.get("spec", {}).get("replicas", 1)
        return {
            "replicas": replicas,
            "updatedReplicas": replicas,
            "readyReplicas": replicas,
            "availableReplicas": replicas,
            "observedGeneration": 1,
            "conditions": [
                {
                    "type": "Available",
                    "status": "True",
                    "lastUpdateTime": datetime.now(timezone.utc).isoformat(),
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "MinimumReplicasAvailable",
                    "message": "Deployment has minimum availability.",
                },
                {
                    "type": "Progressing",
                    "status": "True",
                    "lastUpdateTime": datetime.now(timezone.utc).isoformat(),
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "NewReplicaSetAvailable",
                    "message": "ReplicaSet has successfully progressed.",
                },
            ],
        }
    else:
        replicas = body.get("spec", {}).get("replicas", 1)
        return {
            "replicas": replicas,
            "updatedReplicas": 0,
            "readyReplicas": 0,
            "availableReplicas": 0,
            "unavailableReplicas": replicas,
            "observedGeneration": 1,
            "conditions": [
                {
                    "type": "Available",
                    "status": "False",
                    "lastUpdateTime": datetime.now(timezone.utc).isoformat(),
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "MinimumReplicasUnavailable",
                    "message": "Deployment does not have minimum availability.",
                },
                {
                    "type": "Progressing",
                    "status": "False",
                    "lastUpdateTime": datetime.now(timezone.utc).isoformat(),
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ProgressDeadlineExceeded",
                    "message": "ReplicaSet has timed out progressing.",
                },
            ],
        }


def get_service_status_template(_body: dict[str, Any]) -> dict[str, Any]:
    """Get realistic Service status"""
    # Services don't typically have complex status
    return {"loadBalancer": {}}


def get_namespace_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get realistic Namespace status"""
    # Check if namespace should be terminating based on ready status
    ready_status, _, _ = _get_ready_status_config(body=body)

    if ready_status == "True":
        return {
            "phase": "Active",
            "conditions": [
                {
                    "type": "NamespaceDeletionDiscoveryFailure",
                    "status": "False",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ResourcesDiscovered",
                    "message": "All resources successfully discovered",
                },
                {
                    "type": "NamespaceDeletionContentFailure",
                    "status": "False",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ContentDeleted",
                    "message": "All content successfully deleted",
                },
            ],
        }
    else:
        # Namespace not ready could mean it's terminating
        return {
            "phase": "Terminating",
            "conditions": [
                {
                    "type": "NamespaceDeletionDiscoveryFailure",
                    "status": "True",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "DiscoveryFailed",
                    "message": "Discovery failed for some resources",
                },
                {
                    "type": "NamespaceDeletionContentFailure",
                    "status": "True",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ContentDeletionFailed",
                    "message": "Failed to delete all content",
                },
            ],
        }


def get_generic_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get generic status for unknown resource types"""
    # Use the general ready status configuration
    ready_status, ready_reason, ready_message = _get_ready_status_config(body=body)

    return {
        "conditions": [
            {
                "type": "Ready",
                "status": ready_status,
                "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                "reason": ready_reason,
                "message": ready_message,
            }
        ]
    }
