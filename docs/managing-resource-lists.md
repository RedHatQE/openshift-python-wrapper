Let me explore the codebase to understand ResourceList and NamespacedResourceList.

Now let me check the example file more carefully and also look at how the `NamespacedResourceList` actually works in the example vs the source code — I noticed the example passes `namespaces=[ns.name for ns in namespaces]` (a list of strings) but the source code expects a `ResourceList` object. Let me verify.

The example file seems to have an outdated API for `NamespacedResourceList` (passing a list of strings), but the actual source code expects a `ResourceList` object. The tests confirm it passes a `ResourceList`. Let me check if the example is outdated:

The example file is inconsistent with the actual source code. The source code validates that each element in `namespaces` has `ns.kind == "Namespace"`, meaning it expects actual Namespace resource objects (from a ResourceList), not strings. The test confirms this by passing a `ResourceList` fixture. I'll document based on the actual source code, not the potentially outdated example.

Let me also check what methods and properties are available:

Now I have all the information I need. Let me write the documentation.

# Managing Bulk Resources with ResourceList

When you need to create several copies of the same resource or deploy a resource across multiple namespaces, doing it one at a time is tedious and error-prone. `ResourceList` and `NamespacedResourceList` let you create, deploy, and clean up groups of resources in a single operation.

## Prerequisites

- A working cluster connection (see [Connecting to Clusters](connecting-to-clusters.html))
- Familiarity with creating individual resources (see [Creating and Managing Resources](creating-and-managing-resources.html))

## Quick Example

Create three namespaces and deploy them in two lines:

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import ResourceList, get_client

client = get_client()

namespaces = ResourceList(resource_class=Namespace, num_resources=3, client=client, name="my-ns")
namespaces.deploy()
# Creates: my-ns-1, my-ns-2, my-ns-3
```

Or use a context manager for automatic cleanup:

```python
with ResourceList(client=client, resource_class=Namespace, name="my-ns", num_resources=3) as namespaces:
    print(namespaces[0].name)  # "my-ns-1"
# All three namespaces are deleted when the block exits
```

## Creating Multiple Copies of a Resource

`ResourceList` creates N copies of a resource type, each with an auto-generated name based on a base name you provide.

**Step 1:** Choose a resource class and specify how many copies you want:

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import ResourceList, get_client

client = get_client()
namespaces = ResourceList(
    resource_class=Namespace,
    num_resources=3,
    client=client,
    name="test-ns",
)
```

This creates three `Namespace` objects named `test-ns-1`, `test-ns-2`, and `test-ns-3`. They are not yet deployed to the cluster.

**Step 2:** Deploy all resources:

```python
namespaces.deploy()
```

**Step 3:** Work with individual resources by index or iteration:

```python
# Access by index
first_ns = namespaces[0]
print(first_ns.name)  # "test-ns-1"

# Iterate over all resources
for ns in namespaces:
    print(ns.name)

# Check how many resources are in the list
print(len(namespaces))  # 3
```

**Step 4:** Clean up all resources when done:

```python
namespaces.clean_up()
```

> **Note:** `clean_up()` deletes resources in reverse order. This ensures dependent resources are removed before the resources they depend on.

## Deploying One Resource Per Namespace

`NamespacedResourceList` creates one instance of a namespaced resource in each namespace from a `ResourceList`.

```python
from ocp_resources.namespace import Namespace
from ocp_resources.pod import Pod
from ocp_resources.resource import NamespacedResourceList, ResourceList, get_client

client = get_client()

# First, create the namespaces
namespaces = ResourceList(resource_class=Namespace, num_resources=3, client=client, name="app-ns")
namespaces.deploy()

# Then create one pod in each namespace
pods = NamespacedResourceList(
    client=client,
    resource_class=Pod,
    namespaces=namespaces,
    name="web-server",
    containers=[{"name": "nginx", "image": "nginx:latest"}],
)
pods.deploy()
```

This creates three pods, all named `web-server`, one in each namespace (`app-ns-1`, `app-ns-2`, `app-ns-3`).

```python
for pod in pods:
    print(f"{pod.name} in {pod.namespace}")
# web-server in app-ns-1
# web-server in app-ns-2
# web-server in app-ns-3
```

> **Warning:** The `namespaces` parameter must be a `ResourceList` containing only Namespace resources. Passing any other resource type raises a `TypeError`.

## Passing Extra Resource Parameters

Any additional keyword arguments you pass are forwarded to each resource's constructor. This lets you configure resources beyond just the name:

```python
from ocp_resources.role import Role
from ocp_resources.resource import NamespacedResourceList

roles = NamespacedResourceList(
    client=client,
    resource_class=Role,
    namespaces=namespaces,
    name="viewer-role",
    rules=[
        {
            "apiGroups": [""],
            "resources": ["pods"],
            "verbs": ["get", "list", "watch"],
        }
    ],
)
roles.deploy()
```

## Advanced Usage

### Context Managers for Automatic Lifecycle

Both `ResourceList` and `NamespacedResourceList` support context managers. Resources are deployed on entry and cleaned up on exit — ideal for tests:

```python
with ResourceList(client=client, resource_class=Namespace, name="test-ns", num_resources=3) as namespaces:
    with NamespacedResourceList(
        client=client,
        resource_class=Pod,
        namespaces=namespaces,
        name="test-pod",
        containers=[{"name": "app", "image": "busybox"}],
    ) as pods:
        # All namespaces and pods are deployed
        assert len(pods) == 3
    # Pods are cleaned up here
# Namespaces are cleaned up here
```

> **Tip:** Nest the context managers so that namespaced resources are cleaned up before their namespaces are deleted.

### Waiting During Deploy and Cleanup

Pass `wait=True` to `deploy()` to wait for each resource to reach a ready state. By default, `clean_up()` already waits for deletion to complete.

```python
namespaces = ResourceList(resource_class=Namespace, num_resources=2, client=client, name="ns")
namespaces.deploy(wait=True)

# Later...
namespaces.clean_up(wait=True)   # wait=True is the default
namespaces.clean_up(wait=False)  # Skip waiting for deletion
```

For more on waiting for specific conditions, see [Waiting for Resource Conditions and Status](waiting-for-conditions.html).

### Comparison: ResourceList vs NamespacedResourceList

| Feature | `ResourceList` | `NamespacedResourceList` |
|---|---|---|
| **Purpose** | Create N copies of any resource | Create one resource per namespace |
| **Naming** | Auto-generates `{name}-1`, `{name}-2`, … | Same name in each namespace |
| **Required params** | `resource_class`, `num_resources`, `name` | `resource_class`, `namespaces`, `name` |
| **Use case** | Multiple namespaces, nodes, cluster-scoped resources | Pods, services, roles — anything namespace-scoped |
| **Context manager** | ✅ | ✅ |

## Troubleshooting

**TypeError: "All the resources in namespaces should be namespaces"**

You passed a `ResourceList` that contains non-Namespace resources to `NamespacedResourceList`. Make sure the `namespaces` parameter is a `ResourceList` created with `resource_class=Namespace`.

**Resources not appearing on the cluster**

Creating a `ResourceList` or `NamespacedResourceList` only instantiates the Python objects — it does not deploy them. Call `.deploy()` or use a context manager (`with ... as`) to actually create the resources on the cluster.

**Cleanup order issues**

Always clean up namespaced resources before their namespaces. When using context managers, nest them so the inner block (namespaced resources) exits first. When calling `clean_up()` manually, clean up dependent resources before their parents.

## Related Pages

- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html)
- [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html)
- [Common Resource Patterns](common-patterns.html)
- [Resource and NamespacedResource API](resource-api.html)
