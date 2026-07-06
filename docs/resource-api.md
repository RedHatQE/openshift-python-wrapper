Let me start by reading the knowledge graph and the pages manifest, then explore the source code.

Now let me examine the constants and exceptions:

Now let me check the `apply_yaml` function and the `get_client` function signature, plus see what `ResourceConstants` inherits:

Let me look for key public methods in resource.py that I might have missed (the file was truncated before):

Let me also check for import paths:

Now let me look at the `NamespacedResource._base_body` more carefully and check for anything more:

Now let me check what the `Event` class looks like for the events method reference:

Let me also check for `generate_yaml_from_template`:

That's a test utility. Let me check for the `skip_existing_resource_creation_teardown` function:

Now I have all the information needed. Let me write the comprehensive API reference page.

# Resource and NamespacedResource API

Complete API reference for the `Resource` and `NamespacedResource` base classes, the `get_client` factory function, and supporting classes (`ResourceEditor`, `ResourceList`, `NamespacedResourceList`, `KubeAPIVersion`).

**Import path:**

```python
from ocp_resources.resource import (
    Resource,
    NamespacedResource,
    ResourceEditor,
    ResourceList,
    NamespacedResourceList,
    get_client,
)
```

---

## `get_client`

Factory function to obtain a Kubernetes `DynamicClient`.

```python
from ocp_resources.resource import get_client

client = get_client(config_file="~/.kube/config")
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `config_file` | `str \| None` | `None` | Path to a kubeconfig file. Falls back to `KUBECONFIG` env var or `~/.kube/config`. |
| `config_dict` | `dict[str, Any] \| None` | `None` | Dict with kubeconfig configuration. Mutually exclusive with `config_file`. |
| `context` | `str \| None` | `None` | Name of the kubeconfig context to use. |
| `client_configuration` | `kubernetes.client.Configuration \| None` | `None` | Pre-built Kubernetes client configuration object. |
| `persist_config` | `bool` | `True` | Whether to persist config file changes. |
| `temp_file_path` | `str \| None` | `None` | Path to a temporary kubeconfig file. |
| `try_refresh_token` | `bool` | `True` | Try to refresh the authentication token. |
| `username` | `str \| None` | `None` | Username for basic auth. Requires `password` and `host`. |
| `password` | `str \| None` | `None` | Password for basic auth. Requires `username` and `host`. |
| `host` | `str \| None` | `None` | Cluster host URL. |
| `verify_ssl` | `bool \| None` | `None` | Whether to verify SSL certificates. |
| `token` | `str \| None` | `None` | Bearer token for authentication. Requires `host`. |
| `fake` | `bool` | `False` | Return a `FakeDynamicClient` for testing without a cluster. |
| `generate_kubeconfig` | `bool` | `False` | Save the resolved kubeconfig to a temp file and attach the path to the client. |

**Returns:** `DynamicClient | FakeDynamicClient`

```python
# Default kubeconfig
client = get_client()

# With explicit config file and context
client = get_client(config_file="/path/to/kubeconfig", context="my-cluster")

# Token-based auth
client = get_client(host="https://api.cluster.example.com:6443", token="sha256~abc123")

# Basic auth
client = get_client(host="https://api.cluster.example.com:6443", username="admin", password="secret")

# Fake client for unit testing
client = get_client(fake=True)
```

> **Note:** If neither `config_file` nor `config_dict` is provided, the client falls back to the `KUBECONFIG` environment variable, then `~/.kube/config`, and finally in-cluster configuration.

See [Connecting to Clusters](connecting-to-clusters.html) for connection patterns. See [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html) for `fake=True` usage.

---

## `Resource`

```python
from ocp_resources.resource import Resource
```

Base class for **cluster-scoped** Kubernetes/OpenShift resources (e.g., `Namespace`, `Node`, `ClusterRole`). Inherits from `ResourceConstants`. All concrete resource classes inherit from either `Resource` or `NamespacedResource`.

See [Understanding the Resource Class Hierarchy](resource-class-hierarchy.html) for the inheritance model.

### Class Attributes

| Attribute | Type | Default | Description |
|---|---|---|---|
| `api_group` | `str` | `""` | API group for the resource (e.g., `"apps"`, `"batch"`). |
| `api_version` | `str` | `""` | Full API version string (e.g., `"v1"`, `"apps/v1"`). Resolved automatically if `api_group` is set. |
| `singular_name` | `str` | `""` | Singular resource name for API calls. Used to disambiguate when multiple resources match the same kind. |
| `timeout_seconds` | `int` | `60` | Default timeout for API list/watch operations. |

### Constructor

```python
Resource(
    client=client,
    name="my-resource",
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `client` | `DynamicClient \| None` | `None` | Kubernetes dynamic client. Will be mandatory in the next major release. |
| `name` | `str \| None` | `None` | Resource name. Required unless `yaml_file` or `kind_dict` is provided. |
| `teardown` | `bool` | `True` | Whether this resource should be deleted when used as a context manager. |
| `yaml_file` | `str \| None` | `None` | Path to a YAML file defining the resource. Mutually exclusive with `kind_dict`. |
| `delete_timeout` | `int` | `240` | Timeout in seconds for delete operations. |
| `dry_run` | `bool` | `False` | If `True`, create operations use dry-run mode. |
| `node_selector` | `dict[str, Any] \| None` | `None` | Node selector for scheduling. |
| `node_selector_labels` | `dict[str, str] \| None` | `None` | Node selector labels for scheduling. |
| `config_file` | `str \| None` | `None` | Path to kubeconfig. Deprecated; pass `client` instead. |
| `config_dict` | `dict[str, Any] \| None` | `None` | Kubeconfig dict. |
| `context` | `str \| None` | `None` | Kubeconfig context name. Deprecated; pass `client` instead. |
| `label` | `dict[str, str] \| None` | `None` | Labels to set on the resource. |
| `annotations` | `dict[str, str] \| None` | `None` | Annotations to set on the resource. |
| `api_group` | `str` | `""` | Override the class-level `api_group`. |
| `hash_log_data` | `bool` | `True` | Hash sensitive fields (defined by `keys_to_hash`) in log output. |
| `ensure_exists` | `bool` | `False` | Check that the resource already exists on the cluster at init time. Raises `ResourceNotFoundError` if not. |
| `kind_dict` | `dict[Any, Any] \| None` | `None` | Complete resource dict. Mutually exclusive with `yaml_file`. Bypasses `to_dict()` logic. |
| `wait_for_resource` | `bool` | `False` | When used as a context manager, wait for the resource to exist after creation. |
| `schema_validation_enabled` | `bool` | `False` | Enable automatic OpenAPI schema validation on `create()` and `update_replace()`. |

**Raises:**

| Exception | Condition |
|---|---|
| `ValueError` | Both `yaml_file` and `kind_dict` are provided. |
| `NotImplementedError` | Neither `api_group` nor `api_version` is defined on the class. |
| `MissingRequiredArgumentError` | None of `name`, `yaml_file`, or `kind_dict` is provided. |
| `ResourceNotFoundError` | `ensure_exists=True` and the resource does not exist. |

```python
from ocp_resources.namespace import Namespace

# Basic creation
ns = Namespace(client=client, name="my-namespace")

# From a YAML file
ns = Namespace(client=client, yaml_file="namespace.yaml")

# From a dict
ns = Namespace(client=client, kind_dict={"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": "test"}})

# With labels and annotations
ns = Namespace(client=client, name="my-ns", label={"env": "test"}, annotations={"owner": "team-a"})

# Verify it already exists
ns = Namespace(client=client, name="default", ensure_exists=True)
```

---

### Context Manager Protocol

`Resource` supports the Python context manager protocol for automatic creation and cleanup.

```python
from ocp_resources.namespace import Namespace

with Namespace(client=client, name="temp-ns") as ns:
    # Resource is created on __enter__
    print(ns.name)
# Resource is deleted on __exit__ (if teardown=True)
```

| Method | Description |
|---|---|
| `__enter__()` | Calls `deploy(wait=self.wait_for_resource)`. Registers a `SIGINT` handler on the main thread to ensure cleanup on Ctrl+C. Returns `self`. |
| `__exit__(...)` | Calls `clean_up()` if `teardown=True`. Raises `ResourceTeardownError` if cleanup fails. |

> **Tip:** Set `teardown=False` to prevent automatic deletion on context exit.

---

### CRUD Methods

#### `create`

```python
def create(
    self,
    wait: bool = False,
    exceptions_dict: dict[type[Exception], list[str]] = ...,
) -> ResourceInstance | None
```

Create the resource on the cluster.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `wait` | `bool` | `False` | Wait for the resource to exist after creation. |
| `exceptions_dict` | `dict[type[Exception], list[str]]` | `DEFAULT_CLUSTER_RETRY_EXCEPTIONS \| PROTOCOL_ERROR_EXCEPTION_DICT` | Exceptions to retry on. |

**Returns:** `ResourceInstance | None`

**Raises:** `ValidationError` if `schema_validation_enabled=True` and the resource dict is invalid.

```python
ns = Namespace(client=client, name="my-ns")
ns.create(wait=True)
```

#### `delete`

```python
def delete(
    self,
    wait: bool = False,
    timeout: int = 240,
    body: dict[str, Any] | None = None,
) -> bool
```

Delete the resource from the cluster.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `wait` | `bool` | `False` | Wait for the resource to be fully deleted. |
| `timeout` | `int` | `240` | Timeout in seconds when `wait=True`. |
| `body` | `dict[str, Any] \| None` | `None` | Optional delete options body. |

**Returns:** `bool` — `True` if deleted or not found; `False` only if wait timed out.

```python
ns.delete(wait=True, timeout=120)
```

#### `update`

```python
def update(self, resource_dict: dict[str, Any]) -> None
```

Patch the resource with a merge-patch (`application/merge-patch+json`). Only updates the fields present in `resource_dict`.

| Parameter | Type | Description |
|---|---|---|
| `resource_dict` | `dict[str, Any]` | Partial resource dictionary with fields to update. |

> **Note:** Schema validation is **not** applied on `update()` because patches are partial and would fail full-schema validation.

```python
ns.update(resource_dict={"metadata": {"labels": {"env": "staging"}}})
```

#### `update_replace`

```python
def update_replace(self, resource_dict: dict[str, Any]) -> None
```

Replace the full resource. Use this to **remove** existing fields (unlike `update()`, which only adds/modifies).

| Parameter | Type | Description |
|---|---|---|
| `resource_dict` | `dict[str, Any]` | Complete resource dictionary to replace with. |

**Raises:** `ValidationError` if `schema_validation_enabled=True` and the dict is invalid.

```python
full_dict = ns.instance.to_dict()
full_dict["metadata"]["labels"] = {"new-label": "only"}
ns.update_replace(resource_dict=full_dict)
```

---

### Deploy / Clean Up

#### `deploy`

```python
def deploy(self, wait: bool = False) -> Self
```

Create the resource (respects `REUSE_IF_RESOURCE_EXISTS` environment variable).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `wait` | `bool` | `False` | Wait for the resource after creation. |

**Returns:** `Self`

See [Environment Variables and Configuration](environment-variables.html) for `REUSE_IF_RESOURCE_EXISTS` details.

#### `clean_up`

```python
def clean_up(self, wait: bool = True, timeout: int | None = None) -> bool
```

Delete the resource (respects `SKIP_RESOURCE_TEARDOWN` environment variable).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `wait` | `bool` | `True` | Wait for deletion to complete. |
| `timeout` | `int \| None` | `None` | Timeout in seconds. Defaults to `delete_timeout`. |

**Returns:** `bool` — `True` if deleted successfully.

See [Environment Variables and Configuration](environment-variables.html) for `SKIP_RESOURCE_TEARDOWN` details.

---

### Query Methods and Properties

#### `exists`

```python
@property
def exists(self) -> ResourceInstance | None
```

Check if the resource exists on the cluster.

**Returns:** `ResourceInstance` if found, `None` if not.

```python
if ns.exists:
    print("Namespace exists")
```

#### `instance`

```python
@property
def instance(self) -> ResourceInstance
```

Get the live resource instance from the cluster. Retries on transient cluster errors.

**Returns:** `ResourceInstance`

**Raises:** `NotFoundError` if the resource does not exist.

```python
resource_version = ns.instance.metadata.resourceVersion
```

#### `status`

```python
@property
def status(self) -> str
```

Get `status.phase` from the resource instance.

**Returns:** `str` — The status phase string (e.g., `"Running"`, `"Active"`, `"Pending"`).

```python
print(ns.status)  # "Active"
```

#### `labels`

```python
@property
def labels(self) -> ResourceField
```

Get resource labels from `metadata.labels`.

**Returns:** `ResourceField`

```python
for key, value in ns.labels.items():
    print(f"{key}={value}")
```

#### `kind`

```python
@ClassProperty
def kind(cls) -> str | None
```

Get the resource kind name derived from the class hierarchy. This is a **class-level property** — accessible on both the class and instances.

**Returns:** `str | None`

```python
from ocp_resources.namespace import Namespace
print(Namespace.kind)  # "Namespace"
```

#### `api`

```python
@property
def api(self) -> ResourceInstance
```

Get the resource API object (shortcut for `full_api()` with no extra kwargs).

**Returns:** `ResourceInstance`

#### `full_api`

```python
def full_api(self, **kwargs: Any) -> ResourceInstance
```

Get the resource API object with optional filtering kwargs.

| Keyword Argument | Description |
|---|---|
| `pretty` | Pretty-print output. |
| `_continue` | Continuation token for list pagination. |
| `field_selector` | Filter by field. |
| `label_selector` | Filter by label. |
| `limit` | Maximum number of results. |
| `resource_version` | Filter by resource version. |
| `timeout_seconds` | Request timeout. |
| `watch` | Enable watch mode. |

**Returns:** `ResourceInstance`

---

### Class Method: `get`

```python
@classmethod
def get(
    cls,
    client: DynamicClient | None = None,
    dyn_client: DynamicClient | None = None,
    config_file: str = "",
    singular_name: str = "",
    exceptions_dict: dict[type[Exception], list[str]] = ...,
    raw: bool = False,
    context: str | None = None,
    *args: Any,
    **kwargs: Any,
) -> Generator[Any, None, None]
```

List resources of this kind from the cluster.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `client` | `DynamicClient \| None` | `None` | Kubernetes client. |
| `dyn_client` | `DynamicClient \| None` | `None` | Deprecated alias for `client`. |
| `config_file` | `str` | `""` | Path to kubeconfig. Deprecated; pass `client`. |
| `singular_name` | `str` | `""` | Singular resource name for disambiguation. |
| `exceptions_dict` | `dict` | `DEFAULT_CLUSTER_RETRY_EXCEPTIONS` | Exceptions to retry. |
| `raw` | `bool` | `False` | If `True`, yield raw `ResourceInstance` objects instead of wrapper instances. |
| `context` | `str \| None` | `None` | Kubeconfig context. Deprecated; pass `client`. |
| `**kwargs` | | | Passed through to the API (e.g., `label_selector`, `field_selector`). |

**Returns:** `Generator` of resource instances.

> **Note:** For `Resource` (cluster-scoped), yielded objects are constructed with `name` only. For `NamespacedResource`, yielded objects include both `name` and `namespace`.

```python
from ocp_resources.namespace import Namespace

for ns in Namespace.get(client=client):
    print(ns.name)

# With label selector
for ns in Namespace.get(client=client, label_selector="env=production"):
    print(ns.name)

# Raw mode
for raw_ns in Namespace.get(client=client, raw=True):
    print(raw_ns.metadata.name, raw_ns.status.phase)
```

See [Querying and Watching Resources](querying-resources.html) for advanced list/filter patterns.

---

### Static Method: `get_all_cluster_resources`

```python
@staticmethod
def get_all_cluster_resources(
    client: DynamicClient | None = None,
    config_file: str = "",
    context: str | None = None,
    config_dict: dict[str, Any] | None = None,
    *args: Any,
    **kwargs: Any,
) -> Generator[ResourceField, None, None]
```

Yield all resources across **all** API groups in the cluster.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `client` | `DynamicClient \| None` | `None` | Kubernetes client. |
| `**kwargs` | | | Passed to the API (e.g., `label_selector`). |

**Yields:** `ResourceField`

```python
for resource in Resource.get_all_cluster_resources(client=client, label_selector="app=myapp"):
    print(f"{resource.kind}: {resource.metadata.name}")
```

---

### Wait Methods

#### `wait`

```python
def wait(self, timeout: int = 240, sleep: int = 1) -> None
```

Wait until the resource exists on the cluster.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `timeout` | `int` | `240` | Maximum wait time in seconds. |
| `sleep` | `int` | `1` | Sleep interval between retries. |

**Raises:** `TimeoutExpiredError` if the resource does not exist within the timeout.

#### `wait_deleted`

```python
def wait_deleted(self, timeout: int = 240) -> bool
```

Wait until the resource no longer exists.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `timeout` | `int` | `240` | Maximum wait time in seconds. |

**Returns:** `bool` — `True` if deleted, `False` if timed out.

#### `wait_for_status`

```python
def wait_for_status(
    self,
    status: str,
    timeout: int = 240,
    stop_status: str | None = None,
    sleep: int = 1,
    exceptions_dict: dict[type[Exception], list[str]] = ...,
) -> None
```

Wait for `status.phase` to reach the expected value.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `status` | `str` | — | Expected status phase string. |
| `timeout` | `int` | `240` | Maximum wait time in seconds. |
| `stop_status` | `str \| None` | `None` | Stop and fail immediately if this status is reached. Defaults to `Status.FAILED`. |
| `sleep` | `int` | `1` | Sleep interval between retries. |
| `exceptions_dict` | `dict` | `PROTOCOL_ERROR_EXCEPTION_DICT \| DEFAULT_CLUSTER_RETRY_EXCEPTIONS` | Exceptions to retry. |

**Raises:** `TimeoutExpiredError` if the desired status is not reached.

```python
from ocp_resources.pod import Pod

pod.wait_for_status(status=Pod.Status.RUNNING, timeout=120)
```

#### `wait_for_condition`

```python
def wait_for_condition(
    self,
    condition: str,
    status: str,
    timeout: int = 300,
    sleep_time: int = 1,
    reason: str | None = None,
    message: str = "",
    stop_condition: str | None = None,
    stop_status: str = "True",
) -> None
```

Wait for a specific condition to reach the desired state.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `condition` | `str` | — | Condition type name (e.g., `"Ready"`, `"Available"`). |
| `status` | `str` | — | Expected condition status (e.g., `"True"`, `"False"`). |
| `timeout` | `int` | `300` | Maximum wait time in seconds. |
| `sleep_time` | `int` | `1` | Interval between retries. |
| `reason` | `str \| None` | `None` | Expected condition reason. If set, must match exactly. |
| `message` | `str` | `""` | Expected substring within the condition message. |
| `stop_condition` | `str \| None` | `None` | Condition type that, if matched, stops the wait and fails immediately. |
| `stop_status` | `str` | `"True"` | Status for `stop_condition` matching. |

**Raises:**

| Exception | Condition |
|---|---|
| `TimeoutExpiredError` | Condition not met within timeout. |
| `ConditionError` | `stop_condition` is detected with matching `stop_status`. |

```python
ns.wait_for_condition(
    condition="Ready",
    status="True",
    timeout=60,
)
```

See [Waiting for Resource Conditions and Status](waiting-for-conditions.html) for more patterns.

#### `wait_for_conditions`

```python
def wait_for_conditions(self) -> None
```

Wait for the resource to have any conditions populated in its status. Uses a 30-second timeout.

---

### Serialization

#### `to_dict`

```python
def to_dict(self) -> None
```

Populate `self.res` with the intended dict representation of the resource. Called automatically before `create()`. Override this in subclasses to add resource-specific fields.

> **Note:** If `kind_dict` or `yaml_file` was provided, `to_dict()` uses those directly instead of building from individual parameters.

#### `to_yaml`

```python
def to_yaml(self) -> str
```

**Returns:** `str` — YAML string representation of the resource dict.

```python
print(ns.to_yaml())
```

---

### Watch / Events

#### `watcher`

```python
def watcher(
    self,
    timeout: int,
    resource_version: str = "",
) -> Generator[dict[str, Any], None, None]
```

Watch for changes to this specific resource.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `timeout` | `int` | — | Watch duration in seconds. |
| `resource_version` | `str` | `""` | Only return events after this version. Defaults to the version at resource creation time. |

**Yields:** Event dicts with keys `type` (`"ADDED"`, `"MODIFIED"`, `"DELETED"`), `raw_object`, and `object`.

```python
for event in ns.watcher(timeout=30):
    print(event["type"], event["object"].metadata.name)
```

#### `events`

```python
def events(
    self,
    name: str = "",
    label_selector: str = "",
    field_selector: str = "",
    resource_version: str = "",
    timeout: int = 240,
) -> Generator[Any, Any, None]
```

Get Kubernetes events related to this resource.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | `""` | Filter by event name. |
| `label_selector` | `str` | `""` | Comma-separated `key=value` label filters. |
| `field_selector` | `str` | `""` | Additional field selectors (auto-prefixed with `involvedObject.name==<resource_name>`). |
| `resource_version` | `str` | `""` | Filter events by resource version. |
| `timeout` | `int` | `240` | Timeout in seconds. |

**Yields:** `Event` objects.

```python
for event in pod.events(field_selector="type==Warning", timeout=10):
    print(event.object)
```

---

### Validation

#### `validate`

```python
def validate(self) -> None
```

Validate `self.res` against the OpenAPI schema for this resource kind. Called automatically during `create()` and `update_replace()` when `schema_validation_enabled=True`.

**Raises:** `ValidationError` if the resource dict is invalid.

```python
pod = Pod(client=client, name="test", namespace="default")
pod.to_dict()
pod.validate()  # Raises ValidationError on invalid spec
```

#### `validate_dict` (classmethod)

```python
@classmethod
def validate_dict(cls, resource_dict: dict[str, Any]) -> None
```

Validate an arbitrary resource dictionary against the schema without creating a resource instance.

| Parameter | Type | Description |
|---|---|---|
| `resource_dict` | `dict[str, Any]` | Complete resource dictionary. |

**Raises:** `ValidationError` if validation fails.

```python
from ocp_resources.pod import Pod

Pod.validate_dict({
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": "test"},
    "spec": {"containers": [{"name": "web", "image": "nginx"}]},
})
```

See [Validating Resources Against OpenAPI Schemas](validating-resources.html) for full validation guide.

---

### API Request

#### `api_request`

```python
def api_request(
    self,
    method: str,
    action: str,
    url: str,
    retry_params: dict[str, int] | None = None,
    **params: Any,
) -> dict[str, Any]
```

Send a raw HTTP request to the resource's API endpoint. Used internally for subresource actions (e.g., VirtualMachine start/stop).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `method` | `str` | — | HTTP method (`"GET"`, `"PUT"`, `"POST"`, etc.). |
| `action` | `str` | — | Subresource action to append to the URL (e.g., `"start"`, `"stop"`). |
| `url` | `str` | — | Base URL of the resource. |
| `retry_params` | `dict[str, int] \| None` | `None` | Dict with `timeout` and `sleep_time` keys for retry behavior. |
| `**params` | | | Additional params passed to the HTTP request. |

**Returns:** `dict[str, Any]` — Parsed JSON response, or raw response data if not valid JSON.

---

### Utility Methods

#### `retry_cluster_exceptions` (static)

```python
@staticmethod
def retry_cluster_exceptions(
    func: Callable,
    exceptions_dict: dict[type[Exception], list[str]] = DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
    timeout: int = 10,
    sleep_time: int = 1,
    **kwargs: Any,
) -> Any
```

Retry a callable on transient cluster errors.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `func` | `Callable` | — | Function to call. |
| `exceptions_dict` | `dict` | `DEFAULT_CLUSTER_RETRY_EXCEPTIONS` | Map of exception types to message substrings to match. |
| `timeout` | `int` | `10` | Total retry timeout in seconds. |
| `sleep_time` | `int` | `1` | Sleep between retries. |
| `**kwargs` | | | Passed to `func`. |

**Returns:** The return value of `func`.

**Raises:** The last exception if timeout is reached.

#### `get_condition_message`

```python
def get_condition_message(
    self,
    condition_type: str,
    condition_status: str = "",
) -> str
```

Get the message for a specific condition.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `condition_type` | `str` | — | Condition type name. |
| `condition_status` | `str` | `""` | If set, only return the message when the condition status matches. |

**Returns:** `str` — The condition message, or `""` if not found or status doesn't match.

#### `hash_resource_dict`

```python
def hash_resource_dict(self, resource_dict: dict[Any, Any]) -> dict[Any, Any]
```

Replace sensitive fields (defined by `keys_to_hash`) with `"*******"` for logging.

| Parameter | Type | Description |
|---|---|---|
| `resource_dict` | `dict` | The resource dict to hash. |

**Returns:** `dict` — A copy with sensitive values replaced.

> **Tip:** Override the `keys_to_hash` property in subclasses to define which fields to mask.

#### `keys_to_hash`

```python
@property
def keys_to_hash(self) -> list[str]
```

List of key paths to mask in logs. Uses `>` as separator, `[]` for list elements.

**Returns:** `list[str]` — Default: `[]` (no hashing).

```python
# Example override in a Secret subclass:
@property
def keys_to_hash(self):
    return ["data", "stringData"]
```

---

### Inner Classes

#### `Resource.Status`

Pre-defined status phase constants (inherited from `ResourceConstants`).

| Constant | Value |
|---|---|
| `Status.SUCCEEDED` | `"Succeeded"` |
| `Status.FAILED` | `"Failed"` |
| `Status.DELETING` | `"Deleting"` |
| `Status.DEPLOYED` | `"Deployed"` |
| `Status.PENDING` | `"Pending"` |
| `Status.COMPLETED` | `"Completed"` |
| `Status.RUNNING` | `"Running"` |
| `Status.READY` | `"Ready"` |
| `Status.TERMINATING` | `"Terminating"` |
| `Status.ERROR` | `"Error"` |
| `Status.ACTIVE` | `"Active"` |
| `Status.SCHEDULING` | `"Scheduling"` |
| `Status.CRASH_LOOPBACK_OFF` | `"CrashLoopBackOff"` |
| `Status.IMAGE_PULL_BACK_OFF` | `"ImagePullBackOff"` |

```python
pod.wait_for_status(status=Pod.Status.RUNNING)
```

#### `Resource.Condition`

Pre-defined condition type and status constants.

| Constant | Value |
|---|---|
| `Condition.READY` | `"Ready"` |
| `Condition.AVAILABLE` | `"Available"` |
| `Condition.DEGRADED` | `"Degraded"` |
| `Condition.PROGRESSING` | `"Progressing"` |
| `Condition.UPGRADEABLE` | `"Upgradeable"` |
| `Condition.Status.TRUE` | `"True"` |
| `Condition.Status.FALSE` | `"False"` |
| `Condition.Status.UNKNOWN` | `"Unknown"` |

```python
ns.wait_for_condition(
    condition=Resource.Condition.READY,
    status=Resource.Condition.Status.TRUE,
)
```

#### `Resource.ApiGroup`

Pre-defined API group string constants. A selection of commonly used values:

| Constant | Value |
|---|---|
| `ApiGroup.APPS` | `"apps"` |
| `ApiGroup.BATCH` | `"batch"` |
| `ApiGroup.NETWORKING_K8S_IO` | `"networking.k8s.io"` |
| `ApiGroup.RBAC_AUTHORIZATION_K8S_IO` | `"rbac.authorization.k8s.io"` |
| `ApiGroup.STORAGE_K8S_IO` | `"storage.k8s.io"` |
| `ApiGroup.CONFIG_OPENSHIFT_IO` | `"config.openshift.io"` |
| `ApiGroup.KUBEVIRT_IO` | `"kubevirt.io"` |
| `ApiGroup.CDI_KUBEVIRT_IO` | `"cdi.kubevirt.io"` |
| `ApiGroup.ROUTE_OPENSHIFT_IO` | `"route.openshift.io"` |
| `ApiGroup.MACHINE_OPENSHIFT_IO` | `"machine.openshift.io"` |

> **Note:** Over 100 API group constants are available. Use IDE auto-complete to discover all values.

#### `Resource.ApiVersion`

| Constant | Value |
|---|---|
| `ApiVersion.V1` | `"v1"` |
| `ApiVersion.V1BETA1` | `"v1beta1"` |
| `ApiVersion.V1ALPHA1` | `"v1alpha1"` |
| `ApiVersion.V1ALPHA3` | `"v1alpha3"` |

---

## `NamespacedResource`

```python
from ocp_resources.resource import NamespacedResource
```

Base class for **namespace-scoped** resources (e.g., `Pod`, `Deployment`, `Service`, `ConfigMap`). Extends `Resource` with namespace awareness.

### Constructor

```python
NamespacedResource(
    client=client,
    name="my-pod",
    namespace="my-namespace",
)
```

All parameters from [`Resource`](#constructor) are accepted, plus:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `namespace` | `str \| None` | `None` | Kubernetes namespace. Required unless `yaml_file` or `kind_dict` is provided. |

**Raises:** `MissingRequiredArgumentError` if neither (`name` + `namespace`) nor `yaml_file` / `kind_dict` is provided.

```python
from ocp_resources.pod import Pod

pod = Pod(
    client=client,
    name="nginx",
    namespace="default",
    label={"app": "web"},
)
```

### Overridden Methods

#### `instance`

```python
@property
def instance(self) -> ResourceInstance
```

Get the live resource instance, scoped to `self.namespace`.

**Returns:** `ResourceInstance`

#### `to_dict`

```python
def to_dict(self) -> None
```

Populates `self.res` and sets `metadata.namespace`. If using `yaml_file` or `kind_dict`, reads the namespace from the YAML/dict.

**Raises:** `MissingRequiredArgumentError` if namespace is still not set after processing.

#### `get` (classmethod)

Behaves like `Resource.get()`, but yields instances constructed with both `name` and `namespace`.

```python
from ocp_resources.pod import Pod

for pod in Pod.get(client=client, namespace="default"):
    print(f"{pod.namespace}/{pod.name}")

# With label selector
for pod in Pod.get(client=client, namespace="default", label_selector="app=web"):
    print(pod.name)
```

---

## `ResourceEditor`

```python
from ocp_resources.resource import ResourceEditor
```

Temporarily patch resources and automatically restore original values. Designed for test scenarios.

### Constructor

```python
ResourceEditor(
    patches: dict[Any, Any],
    action: str = "update",
    user_backups: dict[Any, Any] | None = None,
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `patches` | `dict` | — | Map of `{Resource: patch_dict}`. |
| `action` | `str` | `"update"` | `"update"` for merge-patch, `"replace"` for full replacement. |
| `user_backups` | `dict \| None` | `None` | Pre-computed backup dicts. If provided, skips automatic backup creation. |

### Context Manager Usage

```python
from ocp_resources.resource import ResourceEditor
from ocp_resources.namespace import Namespace

ns = Namespace(client=client, name="my-ns", ensure_exists=True)

with ResourceEditor(
    patches={ns: {"metadata": {"labels": {"temporary": "true"}}}}
) as editor:
    # Labels are patched
    assert ns.instance.metadata.labels.temporary == "true"
# Labels are restored to original values
```

### Methods

| Method | Signature | Description |
|---|---|---|
| `update` | `update(backup_resources: bool = False) -> None` | Apply patches. If `backup_resources=True`, back up original values first. |
| `restore` | `restore() -> None` | Restore all backed-up values. |

### Properties

| Property | Type | Description |
|---|---|---|
| `backups` | `dict[Any, Any]` | Backed-up original values for each patched resource. |
| `patches` | `dict[Any, Any]` | The patches dict from the constructor. |

> **Warning:** The `DynamicClient` used to obtain the resource objects must have sufficient privileges to patch and replace resources.

See [Editing Resources Temporarily with ResourceEditor](editing-resources-temporarily.html) for detailed patterns.

---

## `ResourceList`

```python
from ocp_resources.resource import ResourceList
```

Create and manage N copies of a cluster-scoped resource with indexed names.

### Constructor

```python
ResourceList(
    resource_class: type[Resource],
    num_resources: int,
    client: DynamicClient,
    **kwargs: Any,
)
```

| Parameter | Type | Description |
|---|---|---|
| `resource_class` | `type[Resource]` | The resource class to instantiate. |
| `num_resources` | `int` | Number of resource copies to create. |
| `client` | `DynamicClient` | Kubernetes client. |
| `**kwargs` | | Passed to each resource constructor. Must include `name` (used as base name). |

Resources are named `{name}-1`, `{name}-2`, ..., `{name}-N`.

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import ResourceList

namespaces = ResourceList(
    resource_class=Namespace,
    num_resources=3,
    client=client,
    name="test-ns",
)

with namespaces:
    # Creates test-ns-1, test-ns-2, test-ns-3
    for ns in namespaces:
        print(ns.name)
# All three namespaces are deleted
```

### Methods (inherited from `BaseResourceList`)

| Method | Signature | Returns | Description |
|---|---|---|---|
| `deploy` | `deploy(wait=False)` | `list[Resource]` | Deploy all resources. |
| `clean_up` | `clean_up(wait=True)` | `bool` | Delete all resources in reverse order. |
| `__len__` | `__len__()` | `int` | Number of resources. |
| `__getitem__` | `__getitem__(index)` | `Resource` | Access by index. |
| `__iter__` | `__iter__()` | `Generator` | Iterate over resources. |

---

## `NamespacedResourceList`

```python
from ocp_resources.resource import NamespacedResourceList
```

Create one instance of a namespaced resource in each namespace from a `ResourceList`.

### Constructor

```python
NamespacedResourceList(
    resource_class: type[NamespacedResource],
    namespaces: ResourceList,
    client: DynamicClient,
    **kwargs: Any,
)
```

| Parameter | Type | Description |
|---|---|---|
| `resource_class` | `type[NamespacedResource]` | The namespaced resource class (e.g., `Pod`). |
| `namespaces` | `ResourceList` | A `ResourceList` of `Namespace` resources. |
| `client` | `DynamicClient` | Kubernetes client. |
| `**kwargs` | | Passed to each resource constructor. Must include `name`. |

**Raises:** `TypeError` if any resource in `namespaces` is not a `Namespace`.

```python
from ocp_resources.namespace import Namespace
from ocp_resources.pod import Pod
from ocp_resources.resource import ResourceList, NamespacedResourceList

namespaces = ResourceList(
    resource_class=Namespace, num_resources=2, client=client, name="test-ns"
)

pods = NamespacedResourceList(
    resource_class=Pod,
    namespaces=namespaces,
    client=client,
    name="nginx",
)

with namespaces:
    with pods:
        # Creates nginx in test-ns-1 and test-ns-2
        for pod in pods:
            print(f"{pod.namespace}/{pod.name}")
```

See [Managing Bulk Resources with ResourceList](managing-resource-lists.html) for full usage patterns.

---

## `KubeAPIVersion`

```python
from ocp_resources.resource import KubeAPIVersion
```

Implements [Kubernetes API versioning](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning) with comparison operators. Extends `packaging.version.Version`.

### Constructor

```python
KubeAPIVersion(vstring: str)
```

| Parameter | Type | Description |
|---|---|---|
| `vstring` | `str` | Version string (e.g., `"v1"`, `"v1beta1"`, `"v1alpha2"`). |

**Raises:** `ValueError` if the version string does not conform to Kubernetes versioning.

### Ordering

Versions are ordered: `v1alpha1 < v1alpha2 < v1beta1 < v1beta2 < v1 < v2`.

```python
assert KubeAPIVersion("v1") > KubeAPIVersion("v1beta1")
assert KubeAPIVersion("v1beta1") > KubeAPIVersion("v1alpha1")
assert KubeAPIVersion("v1") == KubeAPIVersion("v1")
```

---

## Exceptions

All exceptions are importable from `ocp_resources.exceptions`.

```python
from ocp_resources.exceptions import (
    MissingRequiredArgumentError,
    ResourceTeardownError,
    ValidationError,
    ConditionError,
)
```

| Exception | Raised By | Description |
|---|---|---|
| `MissingRequiredArgumentError` | `Resource.__init__`, `NamespacedResource.__init__`, `NamespacedResource._base_body` | Required parameters (`name`, `namespace`) not provided. |
| `ResourceTeardownError` | `Resource.__exit__` | `clean_up()` returned `False` during context manager exit. |
| `ValidationError` | `validate()`, `validate_dict()`, `create()`, `update_replace()` | Resource dict fails OpenAPI schema validation. Has `message`, `path`, and `schema_error` attributes. |
| `ConditionError` | `wait_for_condition()` | A `stop_condition` was detected during condition waiting. |
| `MissingResourceResError` | `Resource._base_body` | Deprecated. `self.res` is empty after `_base_body()`. |

---

## Timeout Constants

Available from `ocp_resources.utils.constants`:

```python
from ocp_resources.utils.constants import (
    TIMEOUT_1SEC,      # 1
    TIMEOUT_5SEC,      # 5
    TIMEOUT_10SEC,     # 10
    TIMEOUT_30SEC,     # 30
    TIMEOUT_1MINUTE,   # 60
    TIMEOUT_2MINUTES,  # 120
    TIMEOUT_4MINUTES,  # 240
    TIMEOUT_10MINUTES, # 600
)
```

---

## Module-Level Functions

### `replace_key_with_hashed_value`

```python
from ocp_resources.resource import replace_key_with_hashed_value

replace_key_with_hashed_value(resource_dict: dict, key_name: str) -> dict
```

Recursively replace the value at a key path with `"*******"`. Supports dict paths (`a>b>c`) and list paths (`a>b[]>c`).

| Parameter | Type | Description |
|---|---|---|
| `resource_dict` | `dict` | The nested dictionary. |
| `key_name` | `str` | Key path using `>` as separator, `[]` for list elements. |

**Returns:** `dict` — A deep copy with the value replaced.

```python
data = {"spec": {"secret": {"token": "sensitive"}}}
hashed = replace_key_with_hashed_value(data, "spec>secret>token")
# {"spec": {"secret": {"token": "*******"}}}

# With list path
data = {"spec": {"containers": [{"env": [{"value": "secret"}]}]}}
hashed = replace_key_with_hashed_value(data, "spec>containers[]>env[]>value")
```

## Related Pages

- [Understanding the Resource Class Hierarchy](resource-class-hierarchy.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Querying and Watching Resources](querying-resources.html)
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html)
- [Environment Variables and Configuration](environment-variables.html)
