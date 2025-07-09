"""Status template methods for fake Kubernetes resources"""

from datetime import datetime, timezone
from typing import Any


def add_realistic_status(body: dict[str, Any]) -> None:
    """Add realistic status to resources that need it"""
    kind = body.get("kind", "")

    if kind == "Pod":
        status = get_pod_status_template(body=body)
    elif kind == "Deployment":
        status = get_deployment_status_template(body=body)
    elif kind == "Service":
        status = get_service_status_template(body=body)
    elif kind == "Namespace":
        status = get_namespace_status_template(body=body)
    else:
        # Generic status for other resources
        status = get_generic_status_template(body=body)

    if status:
        body["status"] = status


def get_pod_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get realistic Pod status"""
    container_name = "test-container"
    if "spec" in body and "containers" in body["spec"] and body["spec"]["containers"]:
        container_name = body["spec"]["containers"][0].get("name", "test-container")

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
                "status": "False",  # Default to False to match test expectation
                "lastProbeTime": None,
                "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                "reason": "ContainersNotReady",
                "message": f"containers with unready status: [{container_name}]",
            },
            {
                "type": "ContainersReady",
                "status": "False",
                "lastProbeTime": None,
                "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                "reason": "ContainersNotReady",
                "message": f"containers with unready status: [{container_name}]",
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
                "state": {"waiting": {"reason": "ContainerCreating"}},
                "lastState": {},
                "ready": False,
                "restartCount": 0,
                "image": "nginx:latest",
                "imageID": "",
                "containerID": "",
                "started": False,
            }
        ],
    }


def get_deployment_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get realistic Deployment status"""
    return {
        "replicas": 1,
        "updatedReplicas": 1,
        "readyReplicas": 1,
        "availableReplicas": 1,
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


def get_service_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get realistic Service status"""
    # Services don't typically have complex status
    return {"loadBalancer": {}}


def get_namespace_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get realistic Namespace status"""
    return {
        "phase": "Active",  # This is what the test checks for
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


def get_generic_status_template(body: dict[str, Any]) -> dict[str, Any]:
    """Get generic status for unknown resource types"""
    # Most resources have conditions, so provide a generic "Ready" condition
    return {
        "conditions": [
            {
                "type": "Ready",
                "status": "True",
                "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                "reason": "ResourceReady",
                "message": "Resource is ready",
            }
        ]
    }
