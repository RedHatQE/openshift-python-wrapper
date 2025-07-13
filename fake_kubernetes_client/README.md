# Fake Kubernetes Client

A fake/mock implementation of the Kubernetes dynamic client for testing purposes. This allows you to test Kubernetes-related code without needing an actual cluster.

## Features

- Full CRUD operations (Create, Read, Update, Delete) for Kubernetes resources
- Support for all standard Kubernetes resources and Custom Resources
- Proper API group/version/kind handling
- Namespace support
- Label selector support
- Field selector support (limited)
- Watch functionality with event generation
- Realistic status generation for resources
- Configurable resource ready/not-ready states

## Installation

```python
from ocp_resources.resource import get_client

# Create a fake client
fake_client = get_client(fake=True)

# Use it like a real Kubernetes dynamic client
api = fake_client.resources.get(api_version="v1", kind="Pod")
```

## Basic Usage

### Creating Resources

```python
# Create a Pod
pod = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "test-pod",
        "namespace": "default"
    },
    "spec": {
        "containers": [{
            "name": "nginx",
            "image": "nginx:latest"
        }]
    }
}

created_pod = api.create(body=pod, namespace="default")
print(created_pod.metadata.name)  # test-pod
print(created_pod.status.phase)  # Running
```

### Listing Resources

```python
# List all pods
pods = api.get(namespace="default")
for pod in pods.items:
    print(pod.metadata.name)

# List with label selector
pods = api.get(namespace="default", label_selector="app=nginx")
```

### Updating Resources

```python
# Update a pod
pod = api.get(name="test-pod", namespace="default")
pod.metadata.labels = {"app": "nginx"}
updated = api.patch(
    name="test-pod",
    namespace="default",
    body=pod
)
```

### Deleting Resources

```python
# Delete a pod
api.delete(name="test-pod", namespace="default")
```

### Watch Operations

```python
# Watch for changes
count = 0
for event in api.watch(namespace="default", timeout=5):
    print(f"{event['type']}: {event['object'].metadata.name}")
    count += 1
    if count >= 3:
        break
```

## Configuring Resource Ready Status

You can configure resources to be in a "not ready" state for testing scenarios where resources are not fully available. This works for all resource types.

### Using Annotations

Add the `fake-client.io/ready` annotation to any resource:

```python
# Create a Pod that's not ready
pod = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "not-ready-pod",
        "namespace": "default",
        "annotations": {
            "fake-client.io/ready": "false"  # This makes the pod not ready
        }
    },
    "spec": {
        "containers": [{
            "name": "nginx",
            "image": "nginx:latest"
        }]
    }
}

created_pod = api.create(body=pod, namespace="default")
print(created_pod.status.conditions)  # Ready condition will be False
```

### Using Spec Field

Alternatively, you can use `readyStatus` in the spec:

```python
deployment = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "not-ready-deployment",
        "namespace": "default"
    },
    "spec": {
        "readyStatus": False,  # This makes the deployment not ready
        "replicas": 3,
        "selector": {"matchLabels": {"app": "nginx"}},
        "template": {
            "metadata": {"labels": {"app": "nginx"}},
            "spec": {
                "containers": [{
                    "name": "nginx",
                    "image": "nginx:latest"
                }]
            }
        }
    }
}

created = api.create(body=deployment, namespace="default")
print(created.status.readyReplicas)  # 0
print(created.status.conditions)  # Available condition will be False
```

### Resource-Specific Behavior

Different resources behave differently when not ready:

- **Pods**: Show as not ready with containers in waiting state
- **Deployments**: Show 0 ready replicas and unavailable condition
- **Namespaces**: Show as Terminating phase
- **Other resources**: Show Ready condition as False

For Pods specifically, you can also use the `fake-client.io/pod-ready` annotation for backward compatibility.

## Custom Resources

The fake client automatically supports any Custom Resource:

```python
# Access a custom resource
crd_api = fake_client.resources.get(
    api_version="example.com/v1",
    kind="MyCustomResource"
)

# Create custom resource
custom_resource = {
    "apiVersion": "example.com/v1",
    "kind": "MyCustomResource",
    "metadata": {"name": "my-resource"},
    "spec": {"foo": "bar"}
}

created = crd_api.create(body=custom_resource)
```

## Advanced Features

### Namespace Creation

Namespaces are automatically created when you create resources in non-existent namespaces:

```python
# This will auto-create the "new-namespace" namespace
pod = api.create(body=pod_manifest, namespace="new-namespace")
```

### Resource Status

Resources automatically get realistic status fields:

```python
pod = api.get(name="test-pod", namespace="default")
print(pod.status.phase)  # "Running"
print(pod.status.containerStatuses[0].ready)  # True

deployment = deployment_api.get(name="test-deployment", namespace="default")
print(deployment.status.readyReplicas)  # Matches spec.replicas
print(deployment.status.conditions[0].type)  # "Available"
```

### OpenShift Resources

The client includes OpenShift-specific resources:

```python
# Work with OpenShift routes
route_api = fake_client.resources.get(
    api_version="route.openshift.io/v1",
    kind="Route"
)

# Create a route
route = route_api.create(body=route_manifest, namespace="default")
```

## Limitations

- No real networking or pod execution
- Simplified watch implementation (immediate events only)
- Limited field selector support (only metadata.name and metadata.namespace)
- No admission webhooks or validation beyond basic structure
- Status updates are simplified

## Testing Example

```python
import pytest
from ocp_resources.resource import get_client

@pytest.fixture
def k8s_client():
    return get_client(fake=True)

def test_pod_creation(k8s_client):
    api = k8s_client.resources.get(api_version="v1", kind="Pod")

    pod = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": "test-pod", "namespace": "default"},
        "spec": {
            "containers": [{
                "name": "nginx",
                "image": "nginx:latest"
            }]
        }
    }

    created = api.create(body=pod, namespace="default")
    assert created.metadata.name == "test-pod"
    assert created.status.phase == "Running"

    # List pods
    pods = api.get(namespace="default")
    assert len(pods.items) == 1
    assert pods.items[0].metadata.name == "test-pod"
```
