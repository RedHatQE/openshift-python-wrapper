Let me start by exploring the repository structure and the knowledge graph.

Now let me look at the test files for the fake client:

Let me look at a few more test files to understand patterns used:

Now let me look at how `get_client` works with `fake=True` and how resource classes use the client:

Now let me look at a few more test examples to understand patterns:

Now let me check how resources use the fake client and how `deploy`, `clean_up`, `update` work:

Let me look at additional test files for more patterns - ConfigMap, events, and the configmap resource:

Now let me check how watch and events are used, and how to use the lower-level API:

Now let me check the `events` and `watch` implementation in the Resource class:

Now let me look at a few more resource test files and the low-level API usage:

Let me check for import paths and the `ocp_resources.resource` module to understand the public API:

Let me check how the `wait_for_condition` and other resource methods work with the fake client:

Now I have enough information to write the documentation page. Let me check a couple more things:

Now I have all the information I need. Let me write the documentation page.

# Testing Without a Cluster Using the Fake Client

Write unit tests that create, read, update, and delete Kubernetes resources — including status checks, watch events, and custom CRDs — without connecting to a real cluster.

## Prerequisites

- `openshift-python-wrapper` installed (see [Installing and Creating Your First Resource](quickstart.html))
- `pytest` installed for running tests

## Quick Example

```python
import pytest
from ocp_resources.resource import get_client
from ocp_resources.namespace import Namespace

@pytest.fixture(scope="class")
def fake_client():
    return get_client(fake=True)

class TestMyFeature:
    def test_create_namespace(self, fake_client):
        ns = Namespace(client=fake_client, name="my-namespace")
        ns.deploy()

        assert ns.exists
        assert ns.kind == "Namespace"
        assert ns.status == Namespace.Status.ACTIVE

        ns.clean_up(wait=False)
        assert not ns.exists
```

Run it with `pytest` — no cluster, no kubeconfig, no network calls.

## How It Works

Calling `get_client(fake=True)` returns an in-memory client that simulates the Kubernetes API. It supports all standard resources (Pods, Deployments, Services, Namespaces, etc.) and OpenShift resources (Routes, Projects, etc.) out of the box.

All resource classes (`Pod`, `Deployment`, `Namespace`, etc.) accept this fake client through their `client` parameter, and all CRUD methods work identically to a real cluster.

## Step-by-Step: CRUD Operations

### 1. Set up a shared fixture

Create a `conftest.py` in your test directory:

```python
import pytest
from ocp_resources.resource import get_client

@pytest.fixture(scope="class")
def fake_client():
    """Provides a fake Kubernetes client for all tests."""
    return get_client(fake=True)
```

> **Tip:** Use `scope="class"` so resources created in one test method persist for subsequent methods in the same class.

### 2. Create a resource

```python
from ocp_resources.pod import Pod

def test_create_pod(fake_client):
    pod = Pod(
        client=fake_client,
        name="my-pod",
        namespace="default",
        containers=[{"name": "nginx", "image": "nginx:latest"}],
    )
    result = pod.deploy()

    assert result.name == "my-pod"
    assert pod.exists
```

The fake client automatically generates metadata (`uid`, `resourceVersion`, `creationTimestamp`) and a realistic `status` section for the resource.

### 3. Read and query resources

```python
from ocp_resources.namespace import Namespace

def test_list_resources(fake_client):
    # Create some namespaces first
    Namespace(client=fake_client, name="ns-a").deploy()
    Namespace(client=fake_client, name="ns-b").deploy()

    # Iterate over all Namespace resources
    for ns in Namespace.get(client=fake_client):
        assert ns.name
```

Access individual resource data via the `instance` property:

```python
def test_get_instance(fake_client):
    ns = Namespace(client=fake_client, name="test-ns")
    ns.deploy()

    assert ns.instance
    assert ns.kind == "Namespace"
```

### 4. Update a resource

Use `update()` to patch a resource or `update_replace()` to replace it entirely:

```python
def test_update_labels(fake_client):
    ns = Namespace(client=fake_client, name="labeled-ns")
    ns.deploy()

    # Patch: add a label
    resource_dict = ns.instance.to_dict()
    resource_dict["metadata"]["labels"]["env"] = "staging"
    ns.update(resource_dict=resource_dict)

    assert ns.labels["env"] == "staging"
```

```python
def test_replace_labels(fake_client):
    ns = Namespace(client=fake_client, name="replace-ns")
    ns.deploy()

    resource_dict = ns.instance.to_dict()
    resource_dict["metadata"]["labels"] = {"new-label": "value"}
    ns.update_replace(resource_dict=resource_dict)

    assert "new-label" in ns.labels.keys()
```

### 5. Delete a resource

```python
def test_delete_resource(fake_client):
    ns = Namespace(client=fake_client, name="temp-ns")
    ns.deploy()
    assert ns.exists

    ns.clean_up(wait=False)
    assert not ns.exists
```

### 6. Use context managers for automatic cleanup

Resources support Python's `with` statement. The resource deploys on entry and is cleaned up on exit:

```python
from ocp_resources.secret import Secret

def test_context_manager(fake_client):
    with Secret(name="my-secret", namespace="default", client=fake_client) as sec:
        assert sec.exists

    # Automatically cleaned up
    assert not sec.exists
```

## Testing Status and Conditions

The fake client generates realistic status objects so you can test code that reads resource status.

### Checking resource status

```python
def test_namespace_status(fake_client):
    ns = Namespace(client=fake_client, name="status-ns")
    ns.deploy()

    assert ns.status == Namespace.Status.ACTIVE
```

### Waiting for conditions

```python
from ocp_resources.pod import Pod

def test_wait_for_condition(fake_client):
    pod = Pod(
        client=fake_client,
        name="ready-pod",
        namespace="default",
        containers=[{"name": "app", "image": "nginx:latest"}],
    )
    pod.deploy()

    pod.wait_for_status(status=Pod.Status.RUNNING, timeout=5)
```

### Simulating "not ready" resources

Control a resource's readiness state with the `fake-client.io/ready` annotation:

```python
def test_not_ready_pod(fake_client):
    pod = Pod(
        client=fake_client,
        name="failing-pod",
        namespace="default",
        containers=[{"name": "app", "image": "nginx:latest"}],
        annotations={"fake-client.io/ready": "false"},
    )
    pod.deploy()

    # The pod will have Ready condition set to False
    pod.wait_for_condition(
        condition=pod.Condition.READY,
        status=pod.Condition.Status.FALSE,
        timeout=5,
    )

    message = pod.get_condition_message(
        condition_type=pod.Condition.READY,
        condition_status=pod.Condition.Status.FALSE,
    )
    assert message
```

Resource-specific status behavior when marked "not ready":

| Resource | Ready behavior | Not-ready behavior |
|---|---|---|
| Pod | `phase: Running`, containers ready | Containers in `waiting` state |
| Deployment | `readyReplicas` matches `spec.replicas` | `readyReplicas: 0`, `unavailableReplicas` set |
| Namespace | `phase: Active` | `phase: Terminating` |
| All others | `Ready` condition `True` | `Ready` condition `False` |

## Testing with Events

The fake client automatically generates Kubernetes events for create, update, and delete operations. You can query them through the resource's `events()` method:

```python
def test_resource_events(fake_client):
    pod = Pod(
        client=fake_client,
        name="event-pod",
        namespace="default",
        containers=[{"name": "nginx", "image": "nginx:latest"}],
    )
    pod.deploy()

    events = list(pod.events(timeout=1))
    assert events
```

## Testing with Deployments

Deployments get a full status template including replica counts, conditions, and observed generation:

```python
from ocp_resources.deployment import Deployment

def test_deployment(fake_client):
    dep = Deployment(
        client=fake_client,
        name="my-deploy",
        namespace="default",
        replicas=3,
        selector={"matchLabels": {"app": "web"}},
        template={
            "metadata": {"labels": {"app": "web"}},
            "spec": {"containers": [{"name": "web", "image": "nginx:latest"}]},
        },
    )
    dep.deploy()

    assert dep.exists
    assert dep.kind == "Deployment"

    dep.clean_up(wait=False)
    assert not dep.exists
```

## Testing with ResourceList

Test bulk resource creation with `ResourceList` and `NamespacedResourceList`:

```python
from ocp_resources.resource import ResourceList, NamespacedResourceList

def test_resource_list(fake_client):
    with ResourceList(
        client=fake_client,
        resource_class=Namespace,
        name="batch-ns",
        num_resources=3,
    ) as namespaces:
        assert len(namespaces) == 3
    # All three namespaces are automatically cleaned up
```

See [Managing Bulk Resources with ResourceList](managing-resource-lists.html) for more details.

## Advanced Usage

### Using the low-level API directly

You can bypass resource classes and work with the fake client's API directly — useful for testing custom logic:

```python
def test_low_level_api(fake_client):
    api = fake_client.resources.get(api_version="v1", kind="Pod")

    # Create
    pod = api.create(
        body={
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": "raw-pod", "namespace": "default"},
            "spec": {"containers": [{"name": "app", "image": "nginx:latest"}]},
        },
        namespace="default",
    )
    assert pod.metadata.name == "raw-pod"
    assert pod.status.phase == "Running"

    # List
    pods = api.get(namespace="default")
    assert len(pods.items) >= 1

    # Patch
    updated = api.patch(
        name="raw-pod",
        namespace="default",
        body={"metadata": {"labels": {"env": "test"}}},
    )
    assert updated.metadata.labels["env"] == "test"

    # Delete
    api.delete(name="raw-pod", namespace="default")
```

### Label and field selectors

The fake client supports filtering resources by labels and fields:

```python
def test_label_selector(fake_client):
    api = fake_client.resources.get(api_version="v1", kind="Pod")

    api.create(body={
        "apiVersion": "v1", "kind": "Pod",
        "metadata": {"name": "pod-a", "namespace": "default", "labels": {"app": "web"}},
        "spec": {"containers": [{"name": "c", "image": "nginx"}]},
    }, namespace="default")

    api.create(body={
        "apiVersion": "v1", "kind": "Pod",
        "metadata": {"name": "pod-b", "namespace": "default", "labels": {"app": "api"}},
        "spec": {"containers": [{"name": "c", "image": "nginx"}]},
    }, namespace="default")

    # Filter by label
    web_pods = api.get(namespace="default", label_selector="app=web")
    assert len(web_pods.items) == 1
    assert web_pods.items[0].metadata.name == "pod-a"
```

Field selectors support `metadata.name` and `metadata.namespace`:

```python
def test_field_selector(fake_client):
    api = fake_client.resources.get(api_version="v1", kind="Pod")
    result = api.get(namespace="default", field_selector="metadata.name=my-pod")
```

### Watch for resource changes

The `watch()` method yields existing resources as `ADDED` events:

```python
def test_watch(fake_client):
    api = fake_client.resources.get(api_version="v1", kind="Pod")

    api.create(body={
        "apiVersion": "v1", "kind": "Pod",
        "metadata": {"name": "watch-pod", "namespace": "default"},
        "spec": {"containers": [{"name": "c", "image": "nginx"}]},
    }, namespace="default")

    for event in api.watch(namespace="default"):
        assert event["type"] == "ADDED"
        assert event["object"].metadata.name
        break  # Stop after first event
```

### Registering Custom Resource Definitions

To test with CRDs not bundled in the default schema, register them on the client:

```python
def test_custom_resource(fake_client):
    # Register the CRD
    fake_client.register_resources({
        "kind": "MyApp",
        "api_version": "v1alpha1",
        "group": "apps.example.com",
        "namespaced": True,
    })

    # Use it through the low-level API
    api = fake_client.resources.get(
        api_version="apps.example.com/v1alpha1",
        kind="MyApp",
    )

    created = api.create(
        body={
            "apiVersion": "apps.example.com/v1alpha1",
            "kind": "MyApp",
            "metadata": {"name": "my-app", "namespace": "default"},
            "spec": {"replicas": 2},
        },
        namespace="default",
    )
    assert created.metadata.name == "my-app"
```

You can also register multiple CRDs at once:

```python
fake_client.register_resources([
    {"kind": "MyApp", "api_version": "v1", "group": "apps.example.com"},
    {"kind": "MyConfig", "api_version": "v1beta1", "group": "config.example.com", "namespaced": False},
])
```

### Testing incremental workflows

Use `@pytest.mark.incremental` to test a resource through its full lifecycle. Each test depends on the previous one succeeding:

```python
import pytest
from ocp_resources.pod import Pod

@pytest.mark.incremental
class TestPodLifecycle:
    @pytest.fixture(scope="class")
    def pod(self, fake_client):
        return Pod(
            client=fake_client,
            name="lifecycle-pod",
            namespace="default",
            containers=[{"name": "nginx", "image": "nginx:latest"}],
        )

    def test_01_create(self, pod):
        deployed = pod.deploy()
        assert deployed.name == "lifecycle-pod"
        assert pod.exists

    def test_02_read(self, pod):
        assert pod.instance
        assert pod.kind == "Pod"

    def test_03_update(self, pod):
        resource_dict = pod.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        pod.update(resource_dict=resource_dict)
        assert pod.labels["updated"] == "true"

    def test_04_delete(self, pod):
        pod.clean_up(wait=False)
        assert not pod.exists
```

> **Note:** The `@pytest.mark.incremental` marker requires custom `conftest.py` hooks. Add the following to your `conftest.py`:
> ```python
> def pytest_runtest_makereport(item, call):
>     if call.excinfo is not None and "incremental" in item.keywords:
>         parent = item.parent
>         parent._previousfailed = item
>
> def pytest_runtest_setup(item):
>     if "incremental" in item.keywords:
>         previousfailed = getattr(item.parent, "_previousfailed", None)
>         if previousfailed is not None:
>             pytest.xfail(f"previous test failed ({previousfailed.name})")
> ```

### Conflict detection

The fake client raises errors for duplicate creates and missing resources, just like a real cluster:

```python
from fake_kubernetes_client import NotFoundError, ConflictError

def test_conflict_on_duplicate_create(fake_client):
    api = fake_client.resources.get(api_version="v1", kind="Namespace")

    api.create(body={"metadata": {"name": "unique-ns"}})

    with pytest.raises(ConflictError):
        api.create(body={"metadata": {"name": "unique-ns"}})

def test_not_found_on_missing(fake_client):
    api = fake_client.resources.get(api_version="v1", kind="Pod")

    with pytest.raises(NotFoundError):
        api.get(name="does-not-exist", namespace="default")
```

### Accessing response data

The fake client returns response objects that support both attribute access and dictionary access:

```python
def test_response_access(fake_client):
    api = fake_client.resources.get(api_version="v1", kind="Pod")

    created = api.create(
        body={
            "apiVersion": "v1", "kind": "Pod",
            "metadata": {"name": "access-pod", "namespace": "default"},
            "spec": {"containers": [{"name": "c", "image": "nginx"}]},
        },
        namespace="default",
    )

    # Attribute access
    assert created.metadata.name == "access-pod"
    assert created.status.phase == "Running"

    # Dictionary-style access
    assert created["metadata"]["name"] == "access-pod"

    # Convert to a plain dict
    data = created.to_dict()
    assert isinstance(data, dict)
    assert data["metadata"]["name"] == "access-pod"
```

## Troubleshooting

**`ResourceNotFoundError` when creating a resource**

The fake client must recognize the resource's API group and kind. Standard Kubernetes and OpenShift resources are pre-registered. For CRDs, call `fake_client.register_resources(...)` before using them.

**Status fields are missing or empty**

Pods, Deployments, Services, and Namespaces have hardcoded status templates. Other resources get a generic status with a `Ready` condition. If the resource has a schema in the bundled OpenAPI definitions, a richer status is generated automatically.

**Tests interfere with each other**

Each call to `get_client(fake=True)` creates an independent in-memory store. Use separate fixtures or narrower fixture scopes to isolate tests that share a client.

## Related Pages

- [Connecting to Clusters](connecting-to-clusters.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Querying and Watching Resources](querying-resources.html)
- [Managing Bulk Resources with ResourceList](managing-resource-lists.html)
- [Common Resource Patterns](common-patterns.html)
