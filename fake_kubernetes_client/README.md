# Fake Kubernetes Client

A comprehensive fake implementation of `kubernetes.dynamic.DynamicClient` for unit testing. This package provides a complete in-memory simulation of the Kubernetes API that works as a drop-in replacement for the real client in testing environments.

## 🎯 Overview

The Fake Kubernetes Client eliminates the need for:

- Real Kubernetes clusters in unit tests
- Complex mocking setups
- External dependencies during testing
- Network calls in test environments

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
            containers=[{"name": "nginx", "image": "nginx"}]
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
deployment_api = client.resources.get(kind="Deployment", api_version="apps/v1")
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

### Custom Resource Definitions

Add custom resources dynamically using the `register_resources()` method:

```python
# Register a single custom resource
client.register_resources({
    "kind": "MyCustomResource",
    "api_version": "v1alpha1",
    "group": "example.com",
    "namespaced": True
})

# Register multiple resources at once
client.register_resources([
    {
        "kind": "MyApp",
        "api_version": "v1",
        "group": "apps.example.com",
        "namespaced": True,
        "plural": "myapps"
    },
    {
        "kind": "MyConfig",
        "api_version": "v1beta1",
        "group": "config.example.com",
        "namespaced": False,  # cluster-scoped
        "shortNames": ["mc"]
    }
])

# After registration, use the resources normally
myapp_api = client.resources.get(
    api_version="apps.example.com/v1",
    kind="MyApp"
)

created = myapp_api.create(
    body={
        "metadata": {"name": "my-app", "namespace": "default"},
        "spec": {"replicas": 3}
    },
    namespace="default"
)
```

#### Resource Definition Parameters

When registering resources, you can specify:

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `kind` | Yes | Resource kind (e.g., "MyResource") | - |
| `api_version` | Yes | API version without group (e.g., "v1", "v1beta1") | - |
| `group` | No | API group (e.g., "example.com") | "" (core group) |
| `namespaced` | No | Whether resource is namespaced | `True` |
| `plural` | No | Plural name | Auto-generated |
| `singular` | No | Singular name | Lowercase kind |
| `shortNames` | No | List of short names | `[]` |
| `categories` | No | List of categories | `["all"]` |

#### Common Use Cases

**1. Testing CRDs (Custom Resource Definitions)**
```python
# Register your CRD
client.register_resources({
    "kind": "Database",
    "api_version": "v1",
    "group": "db.example.com",
    "namespaced": True,
    "plural": "databases",
    "shortNames": ["db"]
})

# Test your operator/controller logic
db_api = client.resources.get(api_version="db.example.com/v1", kind="Database")
db = db_api.create(body={...}, namespace="default")
```

**2. Multi-Version Resources**
```python
# Register same kind with different versions
client.register_resources([
    {
        "kind": "MyAPI",
        "api_version": "v1alpha1",
        "group": "api.example.com"
    },
    {
        "kind": "MyAPI",
        "api_version": "v1beta1",
        "group": "api.example.com"
    },
    {
        "kind": "MyAPI",
        "api_version": "v1",
        "group": "api.example.com"
    }
])
```

## ��️ Architecture

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

## ⚠️ Known Limitations

When a resource is missing, you'll get:

```
NotImplementedError: Couldn't find ResourceKind in api.group api group
```

**Solution:** Use the `register_resources()` method to add the missing resource:

```python
client.register_resources({
    "kind": "MTQ",
    "api_version": "v1alpha1",
    "group": "mtq.kubevirt.io",
    "namespaced": False  # cluster-scoped
})
```

See the [Custom Resource Definitions](#custom-resource-definitions) section for more details.

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

    # Create test resources
    pod_api = client.resources.get(kind="Pod", api_version="v1")
    pod_api.create(body=test_pod, namespace="default")

    service_api = client.resources.get(kind="Service", api_version="v1")
    service_api.create(body=test_service, namespace="default")

    # Run your function that uses the client
    result = my_function(client)

    # Verify results
    assert result.success
    # Check resources exist
    assert pod_api.get(name="test-pod", namespace="default")
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

## 📄 License

This fake client is part of the openshift-python-wrapper project and follows the same license terms.
