Let me start by reading the knowledge graph and understanding the codebase structure.

Now let me explore the key source files related to querying, listing, watching, existence checks, and status retrieval.

Now let me look at the `_prepare_resources` method and the `get` method more closely to understand the filtering parameters:

Now let me look at the event module and test files for querying:

Now let me look at the test files for get/list/watch operations:

Now let me check the conftest to understand fake_client and look at the `Condition` attribute and `Status` attribute patterns:

Now let me check how `get` is called with selectors:

Let me look at how `get` passes `field_selector`, `label_selector`, and `namespace` through kwargs:

Now let me look at more examples of how get() is used with various kwargs, and check what other files show:

Let me check how `_build_event_field_selector` and events work:

Now let me check the namespace.py to see how get() is used in a simple resource:

Now let me look at the node.py for a cluster-scoped resource usage of get:

Now let me check the exceptions module for ConditionError:

Let me also check `ensure_exists`:

Let me also look for properties that relate to querying the resource (uuid, labels):

Now let me check the test for events and any resource-specific tests about querying:

Let me also look at the fake_client to understand what kwargs `get` passes through:

Now I have a thorough understanding of the codebase. Let me write the documentation page.

# Querying and Watching Resources

Find, filter, and monitor Kubernetes and OpenShift resources in your cluster — whether you need to list all pods by label, check if a resource exists, watch for real-time changes, or inspect status and conditions.

## Prerequisites

- `openshift-python-wrapper` installed (see [Installing and Creating Your First Resource](quickstart.html))
- A connected `DynamicClient` instance (see [Connecting to Clusters](connecting-to-clusters.html))

## Quick Example

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()

# List all pods in a namespace
for pod in Pod.get(client=client, namespace="my-namespace"):
    print(f"{pod.name} — {pod.status}")
```

## Listing Resources

Every resource class provides a `get()` class method that returns a generator of resource objects. The method accepts standard Kubernetes query parameters as keyword arguments.

### List all resources of a type

```python
from ocp_resources.namespace import Namespace

for ns in Namespace.get(client=client):
    print(ns.name)
```

### Filter by namespace

Namespaced resources (like `Pod`, `Service`, `ConfigMap`) accept a `namespace` keyword:

```python
from ocp_resources.pod import Pod

for pod in Pod.get(client=client, namespace="default"):
    print(pod.name)
```

### Filter by label selector

Use `label_selector` with standard Kubernetes label selector syntax:

```python
from ocp_resources.pod import Pod

# Single label
for pod in Pod.get(client=client, namespace="my-app", label_selector="app=nginx"):
    print(pod.name)

# Multiple labels (comma-separated)
for pod in Pod.get(client=client, label_selector="app=nginx,tier=frontend"):
    print(pod.name)
```

### Filter by field selector

Use `field_selector` with standard Kubernetes field selector syntax:

```python
from ocp_resources.pod import Pod

# Find pods on a specific node
for pod in Pod.get(client=client, field_selector="spec.nodeName=worker-1"):
    print(pod.name)

# Find pods by status phase
for pod in Pod.get(client=client, namespace="default", field_selector="status.phase=Running"):
    print(pod.name)
```

### Get raw resource objects

By default, `get()` returns wrapper objects. Pass `raw=True` to get the underlying `ResourceInstance` or `ResourceField` objects directly:

```python
from ocp_resources.pod import Pod

for pod in Pod.get(client=client, namespace="default", raw=True):
    # Returns raw ResourceField objects instead of Pod instances
    print(pod.metadata.name, pod.status.phase)
```

### List all cluster resources

To iterate over every resource type in the cluster:

```python
from ocp_resources.resource import Resource

for resource in Resource.get_all_cluster_resources(client=client):
    print(f"{resource.kind}: {resource.metadata.name}")

# Filter with label selector
for resource in Resource.get_all_cluster_resources(client=client, label_selector="my-label=value"):
    print(f"{resource.kind}: {resource.metadata.name}")
```

## `get()` Method Reference

```python
@classmethod
def get(
    cls,
    client: DynamicClient | None = None,
    singular_name: str = "",
    exceptions_dict: dict[type[Exception], list[str]] = DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
    raw: bool = False,
    *args,
    **kwargs,
) -> Generator
```

| Parameter | Type | Description |
|---|---|---|
| `client` | `DynamicClient` | Kubernetes dynamic client (required) |
| `singular_name` | `str` | Resource kind in lowercase; used when multiple resources match the same kind |
| `raw` | `bool` | If `True`, return raw `ResourceInstance`/`ResourceField` objects instead of wrapper instances |
| `exceptions_dict` | `dict` | Exceptions to retry on during API calls |
| `**kwargs` | | Passed through to the Kubernetes API: `namespace`, `label_selector`, `field_selector`, `limit`, `resource_version`, `timeout_seconds`, etc. |

**Returns:** A generator yielding resource objects.

## Checking Resource Existence

The `exists` property queries the API server and returns the resource instance if it exists, or `None` if it does not.

```python
from ocp_resources.namespace import Namespace

ns = Namespace(client=client, name="my-namespace")

if ns.exists:
    print("Namespace exists")
else:
    print("Namespace not found")
```

### Require existence at initialization

Use `ensure_exists=True` to raise `ResourceNotFoundError` immediately if the resource is not found:

```python
from ocp_resources.pod import Pod

# Raises ResourceNotFoundError if the pod doesn't exist
pod = Pod(client=client, name="my-pod", namespace="default", ensure_exists=True)
```

> **Tip:** Use `ensure_exists=True` when you need a reference to a resource that must already be on the cluster, such as a pre-existing ConfigMap or Secret.

## Getting the Resource Instance

The `instance` property fetches the full live resource from the API server:

```python
pod = Pod(client=client, name="my-pod", namespace="default")

# Get the full resource instance
inst = pod.instance
print(inst.metadata.name)
print(inst.metadata.uid)
print(inst.metadata.resourceVersion)

# Convert to a plain dictionary
resource_dict = pod.instance.to_dict()
```

> **Note:** Each access to `.instance` makes an API call. Cache the result in a local variable if you need multiple fields from the same snapshot.

## Retrieving Labels

The `labels` property returns the resource's labels:

```python
ns = Namespace(client=client, name="my-namespace")
print(ns.labels)  # {'kubernetes.io/metadata.name': 'my-namespace', ...}

# Check a specific label
if "app" in ns.labels:
    print(f"App label: {ns.labels['app']}")
```

## Retrieving Resource Status

### Status phase

The `status` property returns the current phase (e.g., `Running`, `Pending`, `Active`):

```python
from ocp_resources.namespace import Namespace

ns = Namespace(client=client, name="my-namespace")
print(ns.status)  # "Active"
```

Each resource class defines status constants you can compare against:

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-pod", namespace="default")
if pod.status == Pod.Status.RUNNING:
    print("Pod is running")
```

Common status constants available on all resources:

| Constant | Value |
|---|---|
| `Status.RUNNING` | `"Running"` |
| `Status.PENDING` | `"Pending"` |
| `Status.SUCCEEDED` | `"Succeeded"` |
| `Status.FAILED` | `"Failed"` |
| `Status.ACTIVE` | `"Active"` |
| `Status.TERMINATING` | `"Terminating"` |
| `Status.COMPLETED` | `"Completed"` |
| `Status.ERROR` | `"Error"` |

### Condition messages

Use `get_condition_message()` to retrieve the message for a specific condition type:

```python
pod = Pod(client=client, name="my-pod", namespace="default")

# Get message for a condition type
msg = pod.get_condition_message(condition_type="Ready")
print(msg)

# Optionally filter by condition status
msg = pod.get_condition_message(
    condition_type="Ready",
    condition_status="False",
)
print(msg)  # Returns empty string if status doesn't match
```

**Signature:**
```python
def get_condition_message(
    self,
    condition_type: str,
    condition_status: str = "",
) -> str
```

| Parameter | Type | Description |
|---|---|---|
| `condition_type` | `str` | The condition type to look up (e.g., `"Ready"`, `"Available"`) |
| `condition_status` | `str` | If provided, only return the message when the condition has this status |

**Returns:** The condition message string, or `""` if not found or status doesn't match.

### Condition constants

Resources provide built-in condition constants:

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-pod", namespace="default")

# Use condition constants
msg = pod.get_condition_message(
    condition_type=Pod.Condition.READY,
    condition_status=Pod.Condition.Status.TRUE,
)
```

Common condition constants:

| Constant | Value |
|---|---|
| `Condition.READY` | `"Ready"` |
| `Condition.AVAILABLE` | `"Available"` |
| `Condition.PROGRESSING` | `"Progressing"` |
| `Condition.DEGRADED` | `"Degraded"` |
| `Condition.UPGRADEABLE` | `"Upgradeable"` |
| `Condition.Status.TRUE` | `"True"` |
| `Condition.Status.FALSE` | `"False"` |
| `Condition.Status.UNKNOWN` | `"Unknown"` |

## Watching for Changes

### Watch a specific resource

The `watcher()` method streams events for a specific resource instance:

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-pod", namespace="default")

for event in pod.watcher(timeout=60):
    print(f"Event type: {event['type']}")       # ADDED, MODIFIED, DELETED
    print(f"Object: {event['object'].metadata.name}")
    print(f"Raw: {event['raw_object']}")
```

**Signature:**
```python
def watcher(
    self,
    timeout: int,
    resource_version: str = "",
) -> Generator[dict[str, Any], None, None]
```

| Parameter | Type | Description |
|---|---|---|
| `timeout` | `int` | How long to watch (in seconds) |
| `resource_version` | `str` | Only receive events newer than this version. Defaults to the resource version at creation time. |

Each yielded event is a dict with these keys:

| Key | Description |
|---|---|
| `type` | Event type: `"ADDED"`, `"MODIFIED"`, or `"DELETED"` |
| `object` | A `ResourceInstance` wrapping the resource |
| `raw_object` | A plain dict representing the resource |

## Querying Events

### Stream events for a resource

The `events()` method watches Kubernetes events associated with a resource:

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-pod", namespace="default")

for event in pod.events(timeout=30):
    print(f"Reason: {event.object.reason}")
    print(f"Message: {event.object.message}")
```

**Signature:**
```python
def events(
    self,
    name: str = "",
    label_selector: str = "",
    field_selector: str = "",
    resource_version: str = "",
    timeout: int = 240,
) -> Generator
```

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | Filter by event name |
| `label_selector` | `str` | Filter by labels (comma-separated `key=value`) |
| `field_selector` | `str` | Additional field filters (merged with auto-generated `involvedObject.name` filter) |
| `resource_version` | `str` | Only return events newer than this version |
| `timeout` | `int` | Watch timeout in seconds (default: 240) |

```python
# Example: filter for Warning events with a specific reason
for event in pod.events(
    field_selector="type==Warning,reason==BackOff",
    timeout=10,
):
    print(event.object.message)
```

### List existing events (non-streaming)

Use `Event.list()` to get a snapshot of existing events without streaming:

```python
from ocp_resources.event import Event

# List Warning events from the last 5 minutes
events = Event.list(
    client=client,
    namespace="my-namespace",
    field_selector="type==Warning",
)
for event in events:
    print(f"{event.reason}: {event.message}")

# List events from the last 10 minutes
events = Event.list(
    client=client,
    namespace="my-namespace",
    since_seconds=600,
)
```

**Signature:**
```python
@classmethod
def Event.list(
    cls,
    client: DynamicClient,
    namespace: str | None = None,
    field_selector: str | None = None,
    label_selector: str | None = None,
    since_seconds: int = 300,
) -> list
```

Events are returned sorted by timestamp (most recent first).

### Delete events

Clean up events before tests to avoid false positives:

```python
from ocp_resources.event import Event

Event.delete_events(
    client=client,
    namespace="my-namespace",
    field_selector="reason=AnEventReason",
)
```

## Advanced Usage

### Handling resources with duplicate API groups

Some resource kinds exist in multiple API groups. Use `singular_name` to disambiguate:

```python
from ocp_resources.dns import DNS

# When a kind exists in multiple API groups, pass singular_name
for dns in DNS.get(client=client, singular_name="dns"):
    print(dns.name)
```

### Using `full_api()` for low-level access

The `full_api()` method returns the raw Kubernetes API resource object, giving you direct access to the API:

```python
ns = Namespace(client=client, name="my-namespace")
api = ns.full_api()

# Use the API directly for custom queries
result = api.get(
    label_selector="app=nginx",
    field_selector="status.phase=Active",
    limit=10,
)
```

`full_api()` accepts these keyword arguments:

| Parameter | Description |
|---|---|
| `pretty` | Pretty-print output |
| `_continue` | Continuation token for paginated results |
| `field_selector` | Filter by fields |
| `label_selector` | Filter by labels |
| `limit` | Maximum number of results |
| `resource_version` | Filter by resource version |
| `timeout_seconds` | Server-side timeout |
| `watch` | Enable watch mode |

### Converting resources to YAML

```python
ns = Namespace(client=client, name="my-namespace")
print(ns.to_yaml())
```

### Wait for conditions and status

For polling-based waiting (e.g., wait until a pod is `Running` or a condition is `True`), see [Waiting for Resource Conditions and Status](waiting-for-conditions.html).

### Querying during tests with the fake client

You can use all querying methods with the fake client for unit testing:

```python
from ocp_resources.resource import get_client
from ocp_resources.namespace import Namespace

client = get_client(fake=True)
ns = Namespace(client=client, name="test-ns")
ns.deploy()

# All query methods work the same way
assert ns.exists
assert ns.instance
assert ns.status == Namespace.Status.ACTIVE

# Listing works too
for ns in Namespace.get(client=client):
    print(ns.name)
```

See [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html) for details.

## Troubleshooting

**`ResourceNotFoundError` when using `ensure_exists=True`**
The resource does not exist on the cluster. Verify the name, namespace, and that the resource has been created before initializing the wrapper.

**`NotImplementedError: Couldn't find <Kind> in <api_group>`**
The resource kind is not available on your cluster. This typically means the CRD has not been installed or the API group is incorrect.

**`get()` returns no results**
- Verify the `namespace` is correct (omit it for cluster-scoped resources).
- Check your `label_selector` and `field_selector` syntax — use `==` for equality (e.g., `field_selector="status.phase==Running"`).
- Ensure the client has permissions to list the resource type.

**`status` property raises `AttributeError`**
Not all resources have a `status.phase` field. Access `instance.status` directly to inspect what status fields are available for your resource type.

## Related Pages

- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html)
- [Working with Kubernetes Events](working-with-events.html)
- [Common Resource Patterns](common-patterns.html)
- [Resource and NamespacedResource API](resource-api.html)
