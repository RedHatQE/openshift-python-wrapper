Let me explore the repository structure and key files to understand the codebase before writing the documentation.

Now let me look at the `NamespacedResource` class and the `get` classmethod for listing resources:

Now let me check the `get_client` with the `utils/client_config.py` for understanding connection options:

Now I have a thorough understanding of the codebase. Let me write the documentation:

Now I have a comprehensive understanding of the codebase. Let me write the guide:

# Installing and Creating Your First Resource

Get up and running with openshift-python-wrapper so you can programmatically create, query, and delete Kubernetes and OpenShift resources from Python. This guide takes you from installation to your first working resource in under 5 minutes.

## Prerequisites

- Python 3.10 or later
- Access to a Kubernetes or OpenShift cluster (with a valid kubeconfig)
- `pip` or another Python package manager

## Quick Example

```bash
pip install openshift-python-wrapper
```

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()

with Namespace(client=client, name="my-first-namespace") as ns:
    ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=120)
    print(f"Namespace {ns.name} is active: {ns.exists}")
# Namespace is automatically deleted when the block exits
```

That's it — the namespace is created when entering the `with` block and cleaned up when leaving it.

## Step 1: Install the Package

```bash
pip install openshift-python-wrapper
```

> **Tip:** For isolated environments, use a virtual environment:
> ```bash
> python -m venv .venv && source .venv/bin/activate
> pip install openshift-python-wrapper
> ```

## Step 2: Connect to Your Cluster

The `get_client()` function returns a dynamic client connected to your cluster. By default it reads your kubeconfig from the `KUBECONFIG` environment variable or `~/.kube/config`:

```python
from ocp_resources.resource import get_client

client = get_client()
```

You can also point to a specific kubeconfig file:

```python
client = get_client(config_file="/path/to/kubeconfig")
```

Or connect with a token and host directly:

```python
client = get_client(host="https://api.mycluster.example.com:6443", token="sha256~...")
```

> **Note:** For the full set of connection options — including basic auth, in-cluster config, and environment variables — see [Connecting to Clusters](connecting-to-clusters.html).

## Step 3: Create a Resource

There are two ways to create a resource: explicitly with `deploy()`/`clean_up()`, or automatically with a context manager (`with` statement).

### Option A: Context Manager (Recommended)

The context manager automatically deletes the resource when the block exits, which prevents leftover resources:

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()

with Namespace(client=client, name="namespace-example-2") as ns:
    ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=120)
    assert ns.exists
# Resource is automatically cleaned up here
```

### Option B: Explicit Deploy and Clean Up

Use `deploy()` and `clean_up()` when you need more control over the lifecycle:

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()

ns = Namespace(client=client, name="namespace-example-1")
ns.deploy()
assert ns.exists
ns.clean_up()
```

> **Tip:** Set `teardown=False` on the resource to prevent `clean_up()` from being called when using a context manager. This is useful when you want the resource to persist after the block exits.

## Step 4: Create a Namespaced Resource

Most Kubernetes resources (Pods, ConfigMaps, Deployments, etc.) live inside a namespace. These require both `name` and `namespace`:

```python
from ocp_resources.config_map import ConfigMap
from ocp_resources.resource import get_client

client = get_client()

with ConfigMap(
    client=client,
    name="app-config",
    namespace="default",
    data={"app.properties": "debug=true\nport=8080"},
) as cm:
    assert cm.exists
    print(f"ConfigMap {cm.name} created in namespace {cm.namespace}")
```

## Step 5: Query Resources

Use the `get()` class method to list resources from the cluster. It returns a generator you can iterate over:

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()

for pod in Pod.get(client=client, namespace="default"):
    print(pod.name)
```

Filter by labels using `label_selector`:

```python
for pod in Pod.get(client=client, label_selector="app=nginx"):
    node = pod.node
    print(f"Pod {pod.name} is running on node {node.name}")
```

Check if a specific resource exists:

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()

ns = Namespace(client=client, name="default")
if ns.exists:
    print("Namespace exists!")
```

> **Note:** For more on querying, filtering, and watching resources, see [Querying and Watching Resources](querying-resources.html).

## Step 6: Delete a Resource

If you didn't use a context manager, call `clean_up()` to delete the resource:

```python
ns = Namespace(client=client, name="my-temp-namespace")
ns.deploy()
# ... do work ...
ns.clean_up()
```

The `clean_up()` method waits for the resource to be fully deleted by default. Pass `wait=False` to return immediately:

```python
ns.clean_up(wait=False)
```

> **Note:** For full details on resource lifecycle management, see [Creating and Managing Resources](creating-and-managing-resources.html).

## Putting It All Together

Here's a complete script that creates a namespace, deploys a ConfigMap inside it, reads it back, and cleans everything up:

```python
from ocp_resources.config_map import ConfigMap
from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()

with Namespace(client=client, name="quickstart-demo") as ns:
    ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=120)

    with ConfigMap(
        client=client,
        name="demo-config",
        namespace="quickstart-demo",
        data={"greeting": "hello from openshift-python-wrapper"},
    ) as cm:
        assert cm.exists
        print(f"Created ConfigMap '{cm.name}' in namespace '{ns.name}'")

        # Query it back
        for config_map in ConfigMap.get(client=client, namespace="quickstart-demo"):
            print(f"  Found: {config_map.name}")
    # ConfigMap cleaned up here
# Namespace cleaned up here
```

## Advanced Usage

### Creating Resources from YAML

You can create any resource from an existing YAML file instead of specifying parameters in Python:

```python
from ocp_resources.config_map import ConfigMap
from ocp_resources.resource import get_client

client = get_client()

cm = ConfigMap(client=client, yaml_file="my-configmap.yaml")
cm.deploy()
```

### Using a Fake Client for Testing

You can run your code without a live cluster by using a fake client — useful for unit tests and local development:

```python
from ocp_resources.config_map import ConfigMap
from ocp_resources.resource import get_client

client = get_client(fake=True)

with ConfigMap(
    client=client,
    name="test-config",
    namespace="default",
    data={"key": "value"},
) as cm:
    cm.create()
    print(f"Created (fake): {cm.name}")
```

> **Note:** See [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html) for full details on the fake client.

### Schema Validation Before Creating

Enable schema validation to catch configuration errors before sending requests to the cluster:

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()

pod = Pod(
    client=client,
    name="validated-pod",
    namespace="default",
    containers=[{"name": "nginx", "image": "nginx:latest"}],
    schema_validation_enabled=True,  # Validates on create
)
pod.deploy()
```

You can also validate manually without creating:

```python
pod = Pod(
    name="check-me",
    namespace="default",
    containers=[{"name": "nginx", "image": "nginx:latest"}],
)
pod.validate()  # Raises ValidationError if invalid
```

> **Note:** See [Validating Resources Against OpenAPI Schemas](validating-resources.html) for more validation options.

### Waiting for Resource Conditions

After creating a resource, you can wait for it to reach a specific status or condition:

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()

with Namespace(client=client, name="wait-demo") as ns:
    ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=120)
```

> **Note:** See [Waiting for Resource Conditions and Status](waiting-for-conditions.html) for advanced waiting patterns.

## Troubleshooting

### "KUBECONFIG not found" or connection errors

Make sure your kubeconfig is in the expected location or explicitly set the path:

```bash
export KUBECONFIG=/path/to/kubeconfig
```

Or pass it directly:

```python
client = get_client(config_file="/path/to/kubeconfig")
```

### Resource not found after creation

Some resources take time to become available. Use `wait_for_status()` or `wait()` to confirm the resource is ready before interacting with it:

```python
ns.deploy()
ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=120)
```

### Missing `name` or `namespace` errors

- Cluster-scoped resources (like `Namespace`) require only `name`.
- Namespaced resources (like `Pod`, `ConfigMap`, `Deployment`) require both `name` and `namespace`.

```python
# Cluster-scoped — only name needed
Namespace(client=client, name="my-ns")

# Namespaced — both name and namespace required
ConfigMap(client=client, name="my-cm", namespace="my-ns")
```

## Related Pages

- [Connecting to Clusters](connecting-to-clusters.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Querying and Watching Resources](querying-resources.html)
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html)
- [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html)
