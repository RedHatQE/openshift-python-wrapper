Let me start by reading the knowledge graph and understanding the repository structure.

Now let me find the ResourceEditor source code.

Now let me look at how ResourceEditor is used in the NNCP file and any tests:

Let me look at the import section and any related constants:

Now let me look at the `update` and `update_replace` methods on the Resource class to understand the two actions:

Now let me look at the imports to verify how ResourceEditor is exported:

Now let me check for any additional examples or documentation:

Let me look at the full ResourceEditor code once more to make sure I've captured everything, and also check the `_apply_patches` method details and what `action` values are supported:

Now I have a complete picture of the ResourceEditor class. Let me write the documentation.

# Editing Resources Temporarily with ResourceEditor

Temporarily modify Kubernetes and OpenShift resources during tests and have their original values automatically restored when you're done. This is essential for test isolation—ensuring that changes made during a test don't leak into other tests or persist in the cluster.

## Prerequisites

- `openshift-python-wrapper` installed in your project (see [Installing and Creating Your First Resource](quickstart.html))
- A cluster connection established with a privileged client (see [Connecting to Clusters](connecting-to-clusters.html))
- One or more existing resources on the cluster that you want to temporarily modify

> **Warning:** The client used to retrieve resources must have sufficient privileges. Do not use an unprivileged user client with `ResourceEditor`.

## Quick Example

```python
from ocp_resources.resource import ResourceEditor
from ocp_resources.node import Node

node = Node(name="worker-0")

with ResourceEditor(
    patches={node: {"metadata": {"labels": {"test-label": "true"}}}}
):
    # The node now has the label "test-label": "true"
    # Run your test logic here...
    pass

# The label is automatically removed when the block exits
```

That's it—when the `with` block ends (even if an exception occurs), the original resource state is restored.

## Step-by-Step: Using ResourceEditor as a Context Manager

### 1. Import and identify your target resource

```python
from ocp_resources.resource import ResourceEditor
from ocp_resources.config_map import ConfigMap

cm = ConfigMap(name="my-config", namespace="my-namespace")
```

### 2. Define your patch

Patches are dictionaries that mirror the resource's YAML structure. Only include the fields you want to change:

```python
patch = {"data": {"feature_flag": "enabled", "log_level": "debug"}}
```

### 3. Wrap your test logic in a `with` block

```python
with ResourceEditor(patches={cm: patch}):
    # ConfigMap now has updated data fields
    assert cm.instance.data.feature_flag == "enabled"
    # Run tests that depend on the modified config...
```

### 4. Original values are restored automatically

When the `with` block exits, the original `data` values are written back to the resource. Fields that didn't exist before the patch are removed (set to `None` in the restore payload, which tells the API to delete them).

## Patching Multiple Resources at Once

Pass multiple resource-patch pairs in a single `ResourceEditor`:

```python
from ocp_resources.resource import ResourceEditor
from ocp_resources.namespace import Namespace
from ocp_resources.config_map import ConfigMap

ns = Namespace(name="test-ns")
cm = ConfigMap(name="app-config", namespace="test-ns")

patches = {
    ns: {"metadata": {"labels": {"env": "test"}}},
    cm: {"data": {"database_url": "postgres://test-db:5432"}},
}

with ResourceEditor(patches=patches):
    # Both resources are patched; run tests here
    pass
# Both resources are restored to their original state
```

## Using update() and restore() Without a Context Manager

If you need finer control over when patches are applied and reverted—for example, in `setup`/`teardown` fixtures—use the `update()` and `restore()` methods directly:

```python
from ocp_resources.resource import ResourceEditor
from ocp_resources.config_map import ConfigMap

cm = ConfigMap(name="app-config", namespace="default")

editor = ResourceEditor(
    patches={cm: {"data": {"mode": "maintenance"}}}
)

# Apply the patch and create backups
editor.update(backup_resources=True)

# ... run tests ...

# Restore original values
editor.restore()
```

> **Note:** When calling `update()` manually, pass `backup_resources=True` to ensure original values are captured. Without this flag, no backup is created and `restore()` will have nothing to revert.

## Advanced Usage

### Replace Instead of Patch

By default, `ResourceEditor` uses the `"update"` action, which sends a merge-patch (`application/merge-patch+json`). This merges your changes into the existing resource. If you need to *replace* the entire resource (for example, to remove fields that merge-patch can't delete), use `action="replace"`:

```python
from ocp_resources.resource import ResourceEditor

with ResourceEditor(
    patches={my_resource: {"spec": {"replicas": 3}}},
    action="replace",
):
    # The resource is fully replaced, not merged
    pass
```

| Action | Method Used | Behavior |
|---|---|---|
| `"update"` (default) | Merge patch | Merges patch into existing resource; cannot remove fields by omission |
| `"replace"` | Full replacement | Replaces the entire resource; fields not in the patch are removed |

> **Warning:** With `action="replace"`, the patch must include all required fields for the resource, not just the fields you want to change. The replacement payload automatically includes `metadata.name`, `metadata.namespace`, `metadata.resourceVersion`, `kind`, and `apiVersion`.

### Providing Your Own Backups

If you already know what the restore state should be (or need custom restore logic), pass `user_backups` to skip the automatic backup calculation:

```python
from ocp_resources.resource import ResourceEditor

custom_backup = {my_resource: {"spec": {"replicas": 1}}}

with ResourceEditor(
    patches={my_resource: {"spec": {"replicas": 5}}},
    user_backups=custom_backup,
):
    # Resource scaled to 5 replicas
    pass
# Restored to 1 replica (your custom backup), regardless of what the original value was
```

### Inspecting Backups

Access the automatically generated backup data through the `backups` property:

```python
editor = ResourceEditor(
    patches={my_resource: {"metadata": {"labels": {"env": "staging"}}}}
)
editor.update(backup_resources=True)

# See what was backed up
print(editor.backups)
# {<Resource>: {'metadata': {'labels': {'env': 'production'}}}}

editor.restore()
```

### No-Op Detection

`ResourceEditor` automatically detects when a patch produces no actual changes. If the patch values already match the resource's current state, the resource is skipped entirely and a warning is logged:

```
ResourceEdit: no diff found in patch for my-resource -- skipping
```

This prevents unnecessary API calls and avoids triggering watch events for no-op changes.

### Automatic Retry on Conflicts

All patch and restore operations are wrapped with automatic retry logic. If a `ConflictError` occurs (for example, due to a concurrent update changing the `resourceVersion`), the operation is retried automatically with a 5-second sleep interval and a 30-second timeout.

## API Reference

### Constructor

```python
ResourceEditor(
    patches: dict,
    action: str = "update",
    user_backups: dict | None = None,
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `patches` | `dict` | *(required)* | Mapping of resource objects to patch dicts: `{resource: {yaml_patch}}` |
| `action` | `str` | `"update"` | Either `"update"` (merge patch) or `"replace"` (full replacement) |
| `user_backups` | `dict \| None` | `None` | Custom backup dicts to use for restore instead of auto-generated ones |

### Properties

| Property | Return Type | Description |
|---|---|---|
| `backups` | `dict` | The backup data captured for each patched resource: `{resource: backup_dict}` |
| `patches` | `dict` | The patches dict provided in the constructor |

### Methods

| Method | Parameters | Description |
|---|---|---|
| `update(backup_resources=False)` | `backup_resources: bool` | Apply patches. Set `backup_resources=True` to capture original values for later restore. |
| `restore()` | — | Re-apply the stored backup dicts to revert all patched resources. |

### Context Manager Protocol

| Method | Behavior |
|---|---|
| `__enter__()` | Calls `update(backup_resources=True)` and returns the `ResourceEditor` instance |
| `__exit__()` | Calls `restore()` to revert all changes |

## Troubleshooting

| Problem | Cause | Solution |
|---|---|---|
| Restore doesn't revert changes | Called `update()` without `backup_resources=True` | Always pass `backup_resources=True` when calling `update()` manually, or use the context manager (`with` block) which does this automatically |
| `NotFoundError` during backup | Resource cannot be found by name (known with some CRDs like `ServiceMonitor`) | `ResourceEditor` handles this automatically by falling back to a field-selector query |
| `ConflictError` during patch | Another process modified the resource concurrently | Automatic retries handle this; if it persists beyond 30 seconds, check for controllers continuously modifying the resource |
| Patch has no effect | The resource already has the values in your patch | This is expected—`ResourceEditor` logs a warning and skips the resource. Check that you're patching the correct fields. |
| `replace` action fails | Patch is missing required fields | When using `action="replace"`, provide all required spec fields since the entire resource is replaced |

> **Tip:** For creating and cleaning up resources (rather than editing existing ones), see [Creating and Managing Resources](creating-and-managing-resources.html). For managing groups of similar resources, see [Managing Bulk Resources with ResourceList](managing-resource-lists.html).

## Related Pages

- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Resource and NamespacedResource API](resource-api.html)
- [Common Resource Patterns](common-patterns.html)
- [Managing Bulk Resources with ResourceList](managing-resource-lists.html)
- [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html)
