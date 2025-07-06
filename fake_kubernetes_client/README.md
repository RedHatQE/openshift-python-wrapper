# Fake Kubernetes Client

A comprehensive fake implementation of `kubernetes.dynamic.DynamicClient` for unit testing. This package provides a complete in-memory simulation of the Kubernetes API that works as a drop-in replacement for the real client in testing environments.

## 🎯 Overview

The Fake Kubernetes Client eliminates the need for:

- Real Kubernetes clusters in unit tests
- Complex mocking setups
- External dependencies during testing
- Network calls in test environments

It provides a fully functional, in-memory Kubernetes API simulation that supports all major operations including CRUD, resource discovery, label/field selectors, watch functionality, and automatic event generation.

## 📦 Installation

The fake client is included as part of this project. Simply import it:

```python
from fake_kubernetes_client import FakeDynamicClient
```

## 🚀 Quick Start

### Basic Usage

```python
from fake_kubernetes_client import FakeDynamicClient

# Create a fake client (no cluster connection needed)
client = FakeDynamicClient()

# Use exactly like the real DynamicClient
pod_api = client.resources.get(kind="Pod", api_version="v1")

# Create a pod
pod_manifest = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": "test-pod", "namespace": "default"},
    "spec": {"containers": [{"name": "test", "image": "nginx"}]}
}

created_pod = pod_api.create(body=pod_manifest, namespace="default")
print(f"Created: {created_pod.metadata.name}")

# Retrieve the pod
pod = pod_api.get(name="test-pod", namespace="default")
print(f"Retrieved: {pod.metadata.name}")

# List pods
pods = pod_api.get(namespace="default")
print(f"Found {len(pods.items)} pods")

# Delete the pod
deleted_pod = pod_api.delete(name="test-pod", namespace="default")
print(f"Deleted: {deleted_pod.metadata.name}")
```

### Test Integration

Perfect for pytest fixtures:

```python
import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.pod import Pod

class TestPodOperations:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def pod(self, client):
        return Pod(
            client=client,
            name="test-pod",
            namespace="default",
            image="nginx"
        )

    def test_pod_creation(self, pod):
        deployed_pod = pod.deploy()
        assert deployed_pod
        assert pod.exists
        assert pod.status
```

## 🔧 Advanced Features

### Resource Discovery & Auto-Generation

The client automatically discovers and generates resource definitions for any Kubernetes resource:

```python
# Works with any resource kind - no pre-configuration needed
vm_api = client.resources.get(kind="VirtualMachine", api_version="kubevirt.io/v1")
crd_api = client.resources.get(kind="MyCustomResource", api_version="example.com/v1")
```

### Label and Field Selectors

Full support for Kubernetes selectors:

```python
# Label selectors
pods = pod_api.get(namespace="default", label_selector="app=nginx,env=prod")

# Field selectors
pods = pod_api.get(namespace="default", field_selector="metadata.name=test-pod")
```

### Automatic Status Generation

Resources get realistic status based on their type:

```python
pod = pod_api.create(body=pod_manifest, namespace="default")

# Automatic Pod status with conditions
print(pod.status.phase)  # "Running"
print(pod.status.conditions)  # Ready, Initialized, PodScheduled, etc.
print(pod.status.containerStatuses)  # Container state info
```

### Event Generation

Automatic Kubernetes events for all operations:

```python
# Events are automatically created for resource operations
pod_api.create(body=pod_manifest, namespace="default")
# → Generates "Created" event

pod_api.delete(name="test-pod", namespace="default")
# → Generates "Deleted" event
```

### Pre-loading Test Data

Load multiple resources at once:

```python
test_resources = [
    {"apiVersion": "v1", "kind": "Pod", "metadata": {"name": "pod1"}},
    {"apiVersion": "v1", "kind": "Service", "metadata": {"name": "svc1"}},
    {"apiVersion": "apps/v1", "kind": "Deployment", "metadata": {"name": "deploy1"}}
]

client = FakeDynamicClient()
client.preload_resources(test_resources)
```

### Custom Resource Definitions

Add custom resources dynamically:

```python
client.add_custom_resource({
    "kind": "MyResource",
    "group": "example.com",
    "version": "v1",
    "namespaced": True,
    "plural": "myresources"
})

# Now use like any other resource
my_api = client.resources.get(kind="MyResource", api_version="example.com/v1")
```

## 🏗️ Architecture

### Single Source of Truth

The fake client uses **only** the `class_generator/schema/__resources-mappings.json` file as its source of truth for resource definitions. This ensures:

- ✅ Accurate API group/version/kind mappings
- ✅ Correct namespace scoping (cluster vs namespaced)
- ✅ Real cluster resource compatibility
- ✅ No hardcoded assumptions

### Resource-Agnostic Design

The storage backend is completely generic and works with any resource type:

```python
# Supports any resource automatically
storage.store_resource("CustomKind", "example.com/v1", "name", "namespace", data)
storage.get_resource("CustomKind", "example.com/v1", "name", "namespace")
```

### Realistic Simulation

- **Metadata Generation**: UIDs, resource versions, timestamps
- **Status Templates**: Pod conditions, Deployment replicas, Service endpoints
- **Event Creation**: Automatic events for all operations
- **Namespace Isolation**: Proper separation between namespaces
- **API Version Handling**: Correct group/version parsing and storage

## 🔍 Supported Operations

### CRUD Operations

- ✅ `create()` - Create resources with automatic metadata
- ✅ `get()` - Retrieve individual resources or lists
- ✅ `patch()` - Merge patch updates
- ✅ `replace()` - Full resource replacement
- ✅ `delete()` - Resource deletion with events

### Advanced Operations

- ✅ `watch()` - Resource change notifications
- ✅ Label/field selectors with filtering
- ✅ Namespace isolation and cross-namespace queries
- ✅ Resource discovery and dynamic registration
- ✅ Custom resource support

### Metadata Features

- ✅ Automatic UID generation
- ✅ Resource version tracking
- ✅ Creation timestamps
- ✅ Generation counters
- ✅ Label and annotation support

## 🧪 Testing Utilities

### Resource Counting

```python
count = client.get_resource_count()
pod_count = client.get_resource_count(kind="Pod", api_version="v1", namespace="default")
```

### Storage Inspection

```python
all_resources = client.list_all_resources()
client.clear_all_resources()  # Clean slate for tests
```

### Error Simulation

```python
# Simulate errors for testing error handling
client.simulate_error("Pod", "create", ConflictError("Already exists"))
```

## ⚠️ Known Limitations

### Missing Resources

When a resource is missing, you'll get:

```
NotImplementedError: Couldn't find ResourceKind in api.group api group
```

### Workarounds

For missing resources, you can manually add them:

```python
client.add_custom_resource({
    "kind": "MTQ",
    "group": "mtq.kubevirt.io",
    "version": "v1",
    "namespaced": False  # cluster-scoped
})
```

## 🔧 API Compatibility

### Drop-in Replacement

The fake client implements the same interface as `kubernetes.dynamic.DynamicClient`:

```python
# Real client
from kubernetes import dynamic, config
real_client = dynamic.DynamicClient(config.new_client_from_config())

# Fake client - same interface
from fake_kubernetes_client import FakeDynamicClient
fake_client = FakeDynamicClient()

# Use identically
pod_api = real_client.resources.get(kind="Pod", api_version="v1")
pod_api = fake_client.resources.get(kind="Pod", api_version="v1")
```

### Exception Compatibility

Uses real Kubernetes exceptions when available:

```python
try:
    pod_api.get(name="nonexistent", namespace="default")
except kubernetes.dynamic.exceptions.NotFoundError:
    print("Resource not found")
```

## 🎭 Usage Patterns

### Unit Test Pattern

```python
def test_my_kubernetes_function():
    client = FakeDynamicClient()

    # Setup test data
    client.preload_resources([test_pod, test_service])

    # Run your function that uses the client
    result = my_function(client)

    # Verify results
    assert result.success
    assert client.get_resource_count(kind="Pod") == 2
```

### Mock Replacement Pattern

```python
@patch('my_module.get_kubernetes_client')
def test_with_fake_client(mock_get_client):
    mock_get_client.return_value = FakeDynamicClient()

    # Your test code here
    my_kubernetes_function()
```

### Class-based Test Pattern

```python
class TestKubernetesIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = FakeDynamicClient()
        self.pod_api = self.client.resources.get(kind="Pod", api_version="v1")

    def test_pod_lifecycle(self):
        # Create, update, delete lifecycle test
        pass
```

## 🔍 Debugging

### Storage Inspection

```python
# See all stored resources
resources = client.list_all_resources()
for resource in resources:
    print(f"{resource['kind']}: {resource['metadata']['name']}")

# Check specific resource counts
print(f"Pods: {client.get_resource_count(kind='Pod', api_version='v1')}")
print(f"Total: {client.get_resource_count()}")
```

### Resource Definition Debugging

```python
pod_api = client.resources.get(kind="Pod", api_version="v1")
print(f"Resource def: {pod_api.resource_def}")
print(f"Namespaced: {pod_api.resource_def['namespaced']}")
print(f"Plural: {pod_api.resource_def['plural']}")
```

## 📄 License

This fake client is part of the openshift-python-wrapper project and follows the same license terms.
