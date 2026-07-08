Let me start by exploring the repository structure and the knowledge graph.

Now let me look at the YAML-related functions and some example resource files:

Now let me look at some concrete resource examples and tests:

Now let me look at tests for create, update, delete operations and the exceptions:

Now let me look at the exceptions module and the project resource:

Now let me look at how `to_yaml`, `yaml_file`, and `kind_dict` usage works, and the `dry_run` option:

Now let me check how `ensure_exists` and `wait_for_resource` work:

Now let me look at how the `service.py` and `route.py` look to understand namespaced resources better:

Let me also look at the `node_network_configuration_policy.py` for a more complex `deploy/clean_up` example:

Now let me look at the `to_yaml` method and some environment variable usage:

Let me also check the `dry_run` behavior and check for how `label` and `annotations` work:

Now I have a thorough understanding of the codebase. Let me write the documentation.

# Creating and Managing Resources

Deploy Kubernetes and OpenShift resources to your cluster, update them in place, and clean them up reliably using the openshift-python-wrapper's resource lifecycle methods.

## Prerequisites

- `openshift-python-wrapper` installed (see [Installing and Creating Your First Resource](quickstart.html))
- A connected client — either a real cluster connection or a fake client for testing (see [Connecting to Clusters](connecting-to-clusters.html))

## Quick Example

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()

# Create, use, and automatically delete a Namespace
with Namespace(client=client, name="my-app") as ns:
    print(f"{ns.name} is ready")
# Namespace is deleted when the block exits
```

## Creating Resources

Every resource provides three ways to create it: calling `deploy()` directly, using a context manager, or loading from a YAML file.

### Using `deploy()` and `clean_up()`

```python
from ocp_resources.namespace import Namespace

ns = Namespace(client=client, name="my-namespace")
ns.deploy()

# ... do work ...

ns.clean_up()  # Deletes the resource and waits for deletion
```

`deploy()` returns the resource instance, so you can chain:

```python
ns = Namespace(client=client, name="my-namespace").deploy()
```

Pass `wait=True` to `deploy()` to block until the resource reaches its ready state:

```python
ns = Namespace(client=client, name="my-namespace")
ns.deploy(wait=True)
```

### Using a Context Manager

The context manager calls `deploy()` on entry and `clean_up()` on exit, guaranteeing cleanup even if an exception occurs:

```python
from ocp_resources.config_map import ConfigMap

with ConfigMap(
    client=client,
    name="app-config",
    namespace="my-namespace",
    data={"database_url": "postgres://db:5432/myapp"},
) as cm:
    print(cm.instance.data)
# ConfigMap is automatically deleted here
```

> **Note:** If cleanup fails during context manager exit, a `ResourceTeardownError` is raised so failures are never silently ignored.

### Namespaced vs. Cluster-Scoped Resources

Resources that live within a namespace inherit from `NamespacedResource` and require both `name` and `namespace`:

```python
from ocp_resources.pod import Pod

pod = Pod(
    client=client,
    name="nginx",
    namespace="my-namespace",
    containers=[{"name": "nginx", "image": "nginx:latest"}],
)
pod.deploy()
```

Cluster-scoped resources (like `Namespace`) inherit from `Resource` and need only `name`:

```python
from ocp_resources.namespace import Namespace

ns = Namespace(client=client, name="my-namespace")
ns.deploy()
```

### Creating Resources from a YAML File

Pass `yaml_file` to create any resource directly from a YAML manifest. The resource name and namespace are read from the file:

```python
from ocp_resources.config_map import ConfigMap

cm = ConfigMap(client=client, yaml_file="manifests/configmap.yaml")
cm.deploy()
```

`yaml_file` also accepts a `StringIO` object for in-memory YAML:

```python
from io import StringIO
from ocp_resources.config_map import ConfigMap

yaml_content = StringIO("""
apiVersion: v1
kind: ConfigMap
metadata:
  name: dynamic-config
  namespace: my-namespace
data:
  setting: "enabled"
""")

cm = ConfigMap(client=client, yaml_file=yaml_content)
cm.deploy()
```

### Creating Resources from a Dictionary

Use `kind_dict` to pass a pre-built dictionary. When `kind_dict` is provided, the resource class's `to_dict()` logic is bypassed entirely:

```python
from ocp_resources.config_map import ConfigMap

resource_dict = {
    "apiVersion": "v1",
    "kind": "ConfigMap",
    "metadata": {
        "name": "from-dict",
        "namespace": "my-namespace",
    },
    "data": {"key": "value"},
}

cm = ConfigMap(client=client, kind_dict=resource_dict)
cm.deploy()
```

> **Warning:** `yaml_file` and `kind_dict` are mutually exclusive. Passing both raises a `ValueError`.

### Adding Labels and Annotations

Pass `label` and `annotations` at construction time:

```python
from ocp_resources.namespace import Namespace

ns = Namespace(
    client=client,
    name="labeled-ns",
    label={"team": "platform", "env": "staging"},
    annotations={"description": "Staging environment namespace"},
)
ns.deploy()
```

## Updating Resources

### Patching with `update()`

`update()` sends a merge patch — it adds or modifies fields without removing existing ones:

```python
cm = ConfigMap(
    client=client,
    name="app-config",
    namespace="my-namespace",
    ensure_exists=True,
)

cm.update(resource_dict={
    "data": {"new_key": "new_value"},
})
```

### Replacing with `update_replace()`

`update_replace()` performs a full replacement of the resource. Use this when you need to **remove** fields that `update()` would leave untouched:

```python
# Get the current state
current = cm.instance.to_dict()

# Remove a key
current["data"].pop("old_key", None)

# Replace the entire resource
cm.update_replace(resource_dict=current)
```

| Method | HTTP Verb | Behavior | Use When |
|--------|-----------|----------|----------|
| `update()` | PATCH | Merges fields into existing resource | Adding or changing fields |
| `update_replace()` | PUT | Replaces entire resource | Removing fields or doing full replacements |

## Deleting Resources

### Using `clean_up()`

```python
ns.clean_up()  # Deletes and waits for removal (default: wait=True)
```

Control the deletion behavior:

```python
# Delete without waiting
ns.clean_up(wait=False)

# Delete with a custom timeout (in seconds)
ns.clean_up(timeout=120)
```

`clean_up()` returns `True` if the resource was successfully deleted, `False` otherwise.

### Using `delete()`

`delete()` is the lower-level method called by `clean_up()`:

```python
ns.delete(wait=True, timeout=240)
```

You can also pass a custom body for delete options:

```python
ns.delete(body={"propagationPolicy": "Background"})
```

> **Tip:** If you delete a resource that doesn't exist, `delete()` logs a warning and returns `True` instead of raising an error.

### Controlling Teardown

Set `teardown=False` at construction to prevent automatic deletion in context managers:

```python
with Namespace(client=client, name="persistent-ns", teardown=False) as ns:
    print("This namespace will NOT be deleted on exit")
```

## Checking Resource State

### Check If a Resource Exists

```python
ns = Namespace(client=client, name="my-namespace")
if ns.exists:
    print("Namespace exists")
```

### Ensure a Resource Already Exists

Use `ensure_exists=True` to raise `ResourceNotFoundError` if the resource is not present on the cluster:

```python
from ocp_resources.config_map import ConfigMap

# Raises ResourceNotFoundError if the ConfigMap doesn't exist
cm = ConfigMap(
    client=client,
    name="must-exist",
    namespace="default",
    ensure_exists=True,
)
```

### Get the Live Instance

The `instance` property fetches the current state from the API server:

```python
ns = Namespace(client=client, name="my-namespace", ensure_exists=True)
print(ns.instance.metadata.labels)
print(ns.status)
```

### Export as YAML

```python
ns = Namespace(client=client, name="my-namespace")
print(ns.to_yaml())
```

For more on querying, watching, and status checks, see [Querying and Watching Resources](querying-resources.html).

## Dry Run Mode

Validate a resource against the API server without actually creating it:

```python
from ocp_resources.namespace import Namespace

ns = Namespace(client=client, name="dry-run-ns", dry_run=True)
ns.deploy()  # Sends the request with ?dryRun=All — no resource is created
```

## Advanced Usage

### Constructor Parameters Reference

All resource classes accept these common parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `client` | `DynamicClient` | `None` | Cluster client connection (will be required in next major release) |
| `name` | `str` | `None` | Resource name |
| `namespace` | `str` | `None` | Namespace (namespaced resources only) |
| `teardown` | `bool` | `True` | Whether `clean_up()` deletes the resource |
| `yaml_file` | `str` | `None` | Path to a YAML manifest file |
| `kind_dict` | `dict` | `None` | Dictionary representation of the resource |
| `delete_timeout` | `int` | `240` | Timeout in seconds for delete operations |
| `dry_run` | `bool` | `False` | Server-side dry run without persisting |
| `label` | `dict` | `None` | Labels to set on the resource |
| `annotations` | `dict` | `None` | Annotations to set on the resource |
| `ensure_exists` | `bool` | `False` | Raise if resource doesn't already exist |
| `wait_for_resource` | `bool` | `False` | Wait for resource creation in context manager |
| `schema_validation_enabled` | `bool` | `False` | Validate against OpenAPI schema on create/replace |
| `hash_log_data` | `bool` | `True` | Mask sensitive data in logs |

For the full API reference, see [Resource and NamespacedResource API](resource-api.html).

### Schema Validation on Create and Replace

Enable automatic schema validation so `create()` and `update_replace()` check your resource against its OpenAPI schema before sending it to the API server:

```python
from ocp_resources.config_map import ConfigMap

cm = ConfigMap(
    client=client,
    name="validated-cm",
    namespace="default",
    data={"key": "value"},
    schema_validation_enabled=True,  # Validates before create()
)
cm.deploy()
```

You can also validate on demand or validate a dictionary directly:

```python
# Validate an existing resource instance
cm.validate()

# Validate a dictionary without creating a resource
ConfigMap.validate_dict({
    "apiVersion": "v1",
    "kind": "ConfigMap",
    "metadata": {"name": "test"},
    "data": {"key": "value"},
})
```

Both methods raise `ValidationError` if validation fails. For more details, see [Validating Resources Against OpenAPI Schemas](validating-resources.html).

### Temporary Edits with ResourceEditor

`ResourceEditor` applies patches to existing resources and automatically restores original values when used as a context manager:

```python
from ocp_resources.resource import ResourceEditor

ns = Namespace(client=client, name="my-namespace", ensure_exists=True)

with ResourceEditor(
    patches={ns: {"metadata": {"labels": {"temporary-label": "true"}}}}
):
    # Label is applied
    assert ns.labels["temporary-label"] == "true"
# Label is automatically removed
```

`ResourceEditor` supports both `update` (merge patch) and `replace` actions:

```python
with ResourceEditor(
    patches={ns: {"metadata": {"labels": {"keep-only-this": "true"}}}},
    action="replace",
):
    pass  # Full replacement applied, then restored on exit
```

For complete coverage, see [Editing Resources Temporarily with ResourceEditor](editing-resources-temporarily.html).

### Managing Multiple Resources

#### ResourceList — Create N Copies

Create multiple instances of the same resource type with indexed names:

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import ResourceList

with ResourceList(
    client=client,
    resource_class=Namespace,
    name="test-ns",
    num_resources=3,
) as namespaces:
    # Creates test-ns-1, test-ns-2, test-ns-3
    for ns in namespaces:
        print(ns.name)
# All three namespaces are deleted on exit
```

#### NamespacedResourceList — One Per Namespace

Create one resource in each namespace from a `ResourceList`:

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import NamespacedResourceList, ResourceList

namespaces = ResourceList(
    client=client,
    resource_class=Namespace,
    name="env",
    num_resources=3,
)

with NamespacedResourceList(
    client=client,
    resource_class=Pod,
    namespaces=namespaces,
    name="worker",
    containers=[{"name": "app", "image": "myapp:latest"}],
) as pods:
    for pod in pods:
        print(f"{pod.name} in {pod.namespace}")
```

For detailed patterns, see [Managing Bulk Resources with ResourceList](managing-resource-lists.html).

### Debugging with Environment Variables

These environment variables control resource lifecycle behavior at runtime without code changes:

| Variable | Effect |
|----------|--------|
| `REUSE_IF_RESOURCE_EXISTS` | Skip `deploy()` if the resource already exists |
| `SKIP_RESOURCE_TEARDOWN` | Skip `clean_up()` to keep resources for debugging |

Both accept a YAML-formatted dictionary. Spaces are significant:

```bash
# Skip creation of all Pods
export REUSE_IF_RESOURCE_EXISTS="{Pod: {}}"

# Skip creation of a specific Pod in a specific namespace
export REUSE_IF_RESOURCE_EXISTS="{Pod: {my-pod: my-namespace}}"

# Skip teardown for a Namespace and a Pod
export SKIP_RESOURCE_TEARDOWN="{Namespace: {my-ns:}, Pod: {my-pod: my-namespace}}"
```

For the full list of environment variables, see [Environment Variables and Configuration](environment-variables.html).

## Troubleshooting

**`MissingRequiredArgumentError` on construction**
You must provide either `name`, `yaml_file`, or `kind_dict`. For namespaced resources, both `name` and `namespace` are required unless using `yaml_file` or `kind_dict`.

**`ResourceTeardownError` in context manager**
The resource's `clean_up()` returned `False`, meaning deletion failed. Check cluster permissions and resource finalizers.

**`ValueError: yaml_file and resource_dict are mutually exclusive`**
You passed both `yaml_file` and `kind_dict` to a constructor. Use only one.

**`ResourceNotFoundError` with `ensure_exists=True`**
The resource doesn't exist on the cluster. Verify the name (and namespace for namespaced resources) are correct.

**Resource not deleted after context manager exits**
Check if `teardown=False` was passed. Also verify the `SKIP_RESOURCE_TEARDOWN` environment variable is not set.

## Related Pages

- [Installing and Creating Your First Resource](quickstart.html)
- [Querying and Watching Resources](querying-resources.html)
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html)
- [Editing Resources Temporarily with ResourceEditor](editing-resources-temporarily.html)
- [Resource and NamespacedResource API](resource-api.html)
