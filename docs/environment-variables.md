Let me start by reading the knowledge graph and page manifest, then explore the codebase for environment variables.

Now let me look at the `keys_to_hash` and hash-related functionality more closely:

Now let me look at the `get_logger` import and how log levels work:

Now let me check for any CI/CD or config-related environment variables:

Let me also look for any validation-related environment variables and enable_validation_by_default:

Now let me look at the `get_logger` usage and the `simple_logger` format:

Now let me check the deploy() and clean_up() methods more carefully, and also the hash_resource_dict method:

Let me also check how `replace_key_with_hashed_value` is defined:

Now let me check the MCP server for environment variables:

Now let me check if there are any other environment variable usages in the class_generator:

Let me verify there are no other env vars in tests:

Let me also check the full `get_client` function and the `save_kubeconfig` function:

Now let me look for any additional environment variables in fake_kubernetes_client:

Let me look at how the deploy and clean_up methods use the skip logic:

Now I have all the information needed. Let me write the documentation:

# Environment Variables and Configuration

This page documents all environment variables recognized by `openshift-python-wrapper` at runtime. These variables control logging behavior, resource lifecycle operations, proxy configuration, cluster connectivity, and sensitive data hashing.

## Quick Reference

| Environment Variable | Purpose | Default |
|---|---|---|
| `KUBECONFIG` | Path to kubeconfig file | `~/.kube/config` |
| `HTTPS_PROXY` | HTTPS proxy URL for cluster connections | _(unset)_ |
| `HTTP_PROXY` | HTTP proxy URL for cluster connections | _(unset)_ |
| `OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL` | Logging verbosity level | `INFO` |
| `OPENSHIFT_PYTHON_WRAPPER_LOG_FILE` | Path to log output file | `""` (stdout) |
| `OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA` | Enable/disable hashing sensitive data in logs | `true` |
| `REUSE_IF_RESOURCE_EXISTS` | Skip resource creation if already exists | _(unset)_ |
| `SKIP_RESOURCE_TEARDOWN` | Skip resource deletion during teardown | _(unset)_ |

---

## Cluster Connection

### `KUBECONFIG`

| Property | Value |
|---|---|
| **Type** | `str` |
| **Default** | `~/.kube/config` |
| **Used by** | `get_client()` |
| **Source** | `ocp_resources/resource.py` |

Path to the kubeconfig file used when creating a Kubernetes `DynamicClient`. Read when no explicit `config_file`, `config_dict`, `host`/`token`, or `username`/`password` arguments are passed to `get_client()`.

> **Note:** The standard `kubernetes` Python client reads `KUBECONFIG` at import time. If you set this variable in code (after import), `openshift-python-wrapper` handles it by explicitly passing the value to the client constructor. See [Connecting to Clusters](connecting-to-clusters.html) for all connection options.

```bash
export KUBECONFIG=/path/to/my/kubeconfig
```

```python
from ocp_resources.resource import get_client

# Automatically uses $KUBECONFIG, or falls back to ~/.kube/config
client = get_client()
```

---

### `HTTPS_PROXY` / `HTTP_PROXY`

| Property | Value |
|---|---|
| **Type** | `str` |
| **Default** | _(unset — no proxy)_ |
| **Used by** | `get_client()` |
| **Source** | `ocp_resources/resource.py` |

Sets the proxy on the Kubernetes client configuration when no proxy is already configured on the `client_configuration` object. `HTTPS_PROXY` takes precedence over `HTTP_PROXY` when both are set.

```bash
export HTTPS_PROXY=http://proxy.example.com:8080
```

```python
from ocp_resources.resource import get_client

# Proxy is automatically applied from environment
client = get_client()
```

> **Tip:** If you pass a `client_configuration` object that already has a `.proxy` set, the environment variables are ignored.

**Precedence order:**

1. Explicit `client_configuration.proxy` (if already set)
2. `HTTPS_PROXY` environment variable
3. `HTTP_PROXY` environment variable

---

## Logging

### `OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL`

| Property | Value |
|---|---|
| **Type** | `str` |
| **Default** | `INFO` |
| **Valid values** | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| **Used by** | `Resource._set_logger()` |
| **Source** | `ocp_resources/resource.py` |

Controls the log level for each resource instance's logger. The logger is created per-resource using the `simple_logger` library.

```bash
export OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL=DEBUG
```

```python
import os
os.environ["OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL"] = "DEBUG"

from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()
pod = Pod(name="my-pod", namespace="default", client=client)
# Logger on this Pod instance now uses DEBUG level
```

---

### `OPENSHIFT_PYTHON_WRAPPER_LOG_FILE`

| Property | Value |
|---|---|
| **Type** | `str` |
| **Default** | `""` (empty string — logs to stdout) |
| **Used by** | `Resource._set_logger()` |
| **Source** | `ocp_resources/resource.py` |

Redirects resource log output to a file. When unset or empty, logs are written to stdout.

```bash
export OPENSHIFT_PYTHON_WRAPPER_LOG_FILE=/var/log/ocp-wrapper.log
```

```python
import os
os.environ["OPENSHIFT_PYTHON_WRAPPER_LOG_FILE"] = "/tmp/ocp-wrapper.log"

from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()
ns = Namespace(name="test-ns", client=client)
# All log output for this resource is written to /tmp/ocp-wrapper.log
```

---

## Sensitive Data Hashing

### `OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA`

| Property | Value |
|---|---|
| **Type** | `str` |
| **Default** | `"true"` |
| **Valid values** | `"true"`, `"false"` |
| **Used by** | `Resource.hash_resource_dict()` |
| **Source** | `ocp_resources/resource.py` |

Controls whether sensitive fields in resource dictionaries are replaced with `"*******"` when logged. When set to `"false"`, sensitive data is logged in cleartext.

Hashing is applied to fields declared in each resource class's `keys_to_hash` property. The following built-in resources define sensitive keys:

| Resource Class | Hashed Fields |
|---|---|
| `Secret` | `data`, `stringData` |
| `ConfigMap` | `data`, `binaryData` |
| `SealedSecret` | `spec>data`, `spec>encryptedData` |
| `VirtualMachine` | `spec>template>spec>volumes[]>cloudInitNoCloud>userData` |

> **Warning:** Setting this to `"false"` causes sensitive data (e.g., secrets, tokens) to appear in log output. Use only for debugging in secure environments.

```bash
# Disable hashing to see raw values in logs (debug only)
export OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA=false
```

```python
import os
os.environ["OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA"] = "false"

from ocp_resources.secret import Secret
from ocp_resources.resource import get_client

client = get_client()
secret = Secret(name="my-secret", namespace="default", client=client)
# Logs will now show raw secret data instead of "*******"
```

> **Note:** Hashing also depends on the `hash_log_data` constructor parameter on each resource instance. Both must be enabled for hashing to occur. The `hash_log_data` parameter defaults to `True`. See [Resource and NamespacedResource API](resource-api.html) for constructor details.

**Interaction with `hash_log_data` parameter:**

| `OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA` | `hash_log_data` param | Result |
|---|---|---|
| `"true"` (default) | `True` (default) | Sensitive fields hashed |
| `"true"` | `False` | Sensitive fields **not** hashed |
| `"false"` | `True` | Sensitive fields **not** hashed |
| `"false"` | `False` | Sensitive fields **not** hashed |

---

## Resource Reuse (Skip Creation)

### `REUSE_IF_RESOURCE_EXISTS`

| Property | Value |
|---|---|
| **Type** | `str` (YAML dict syntax) |
| **Default** | _(unset — no resources skipped)_ |
| **Used by** | `Resource.deploy()` |
| **Source** | `ocp_resources/resource.py` |

When set, `deploy()` checks whether the target resource already exists on the cluster. If a match is found, the existing resource is returned without creating a new one. This is intended for debugging and iterative development workflows.

> **Warning:** Spaces are significant in the value syntax. The value is parsed as YAML.

**Value format:**

```
{<Kind>: {<name>: <namespace>}}
```

**Matching rules:**

| Pattern | Behavior |
|---|---|
| `{Pod: {}}` | Skip creation for **all** Pods (match by kind only) |
| `{Pod: {my-pod:}}` | Skip creation for Pod named `my-pod` in **any** namespace |
| `{Pod: {my-pod: my-ns}}` | Skip creation for Pod named `my-pod` in namespace `my-ns` only |
| `{Kind1: {}, Kind2: {name: ns}}` | Multiple resource patterns combined |

**Examples:**

```bash
# Skip all Pod creation if the pod already exists
export REUSE_IF_RESOURCE_EXISTS="{Pod: {}}"

# Skip specific pod in specific namespace
export REUSE_IF_RESOURCE_EXISTS="{Pod: {my-pod: my-namespace}}"

# Skip namespace and pod creation
export REUSE_IF_RESOURCE_EXISTS="{Namespace: {test-ns:}, Pod: {my-pod: test-ns}}"
```

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()

# If REUSE_IF_RESOURCE_EXISTS is set and a matching Pod exists,
# deploy() returns the existing resource without calling create()
pod = Pod(
    name="my-pod",
    namespace="my-namespace",
    client=client,
    containers=[{"name": "test", "image": "nginx"}],
)
pod.deploy()  # Skips creation if resource matches the env var pattern
```

> **Note:** The resource must actually exist on the cluster for the skip to take effect. If the resource does not exist, `deploy()` proceeds with normal creation.

---

## Skip Teardown

### `SKIP_RESOURCE_TEARDOWN`

| Property | Value |
|---|---|
| **Type** | `str` (YAML dict syntax) |
| **Default** | _(unset — no resources skipped)_ |
| **Used by** | `Resource.clean_up()` |
| **Source** | `ocp_resources/resource.py` |

When set, `clean_up()` skips deletion for matching resources and returns `True` without calling `delete()`. This is intended for debugging — preserving resources on the cluster after tests finish.

> **Warning:** Spaces are significant in the value syntax. The value is parsed as YAML.

**Value format:**

Uses the same YAML dict syntax as [`REUSE_IF_RESOURCE_EXISTS`](#reuse_if_resource_exists).

**Matching rules:**

| Pattern | Behavior |
|---|---|
| `{Pod: {}}` | Skip teardown for **all** Pods |
| `{Pod: {my-pod:}}` | Skip teardown for Pod named `my-pod` in **any** namespace |
| `{Pod: {my-pod: my-ns}}` | Skip teardown for Pod named `my-pod` in namespace `my-ns` only |
| `{Kind1: {}, Kind2: {name: ns}}` | Multiple resource patterns combined |

**Examples:**

```bash
# Keep all Namespaces after test run
export SKIP_RESOURCE_TEARDOWN="{Namespace: {}}"

# Keep specific resources
export SKIP_RESOURCE_TEARDOWN="{Namespace: {test-ns:}, Pod: {debug-pod: test-ns}}"
```

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()
pod = Pod(
    name="debug-pod",
    namespace="test-ns",
    client=client,
    containers=[{"name": "test", "image": "nginx"}],
)
pod.deploy()

# If SKIP_RESOURCE_TEARDOWN is set with a matching pattern,
# clean_up() returns True without deleting the resource
pod.clean_up()  # Resource remains on the cluster
```

> **Tip:** Use `REUSE_IF_RESOURCE_EXISTS` and `SKIP_RESOURCE_TEARDOWN` together for a fast debug loop: skip creation if a resource already exists, and skip teardown so it persists between runs.

```bash
export REUSE_IF_RESOURCE_EXISTS="{Pod: {debug-pod: test-ns}}"
export SKIP_RESOURCE_TEARDOWN="{Pod: {debug-pod: test-ns}}"
```

---

## Combined Usage Patterns

### Debug iteration loop

Set both skip variables to avoid re-creating and tearing down resources between test runs:

```bash
export REUSE_IF_RESOURCE_EXISTS="{Namespace: {test-ns:}, Pod: {my-pod: test-ns}}"
export SKIP_RESOURCE_TEARDOWN="{Namespace: {test-ns:}, Pod: {my-pod: test-ns}}"
```

### Full debug logging with unhashed data

```bash
export OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL=DEBUG
export OPENSHIFT_PYTHON_WRAPPER_LOG_FILE=/tmp/debug.log
export OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA=false
```

> **Warning:** This combination logs sensitive data in plaintext. Do not use in production or shared environments.

### Custom kubeconfig with proxy

```bash
export KUBECONFIG=/path/to/custom/kubeconfig
export HTTPS_PROXY=http://corporate-proxy.example.com:3128
```

---

## Programmatic Configuration Alternatives

Several behaviors controlled by environment variables can also be set programmatically via constructor parameters or function arguments. See [Resource and NamespacedResource API](resource-api.html) for full constructor parameter documentation.

| Environment Variable | Programmatic Alternative |
|---|---|
| `KUBECONFIG` | `get_client(config_file="/path/to/kubeconfig")` |
| `HTTPS_PROXY` / `HTTP_PROXY` | `client_configuration.proxy = "http://proxy:port"` |
| `OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA` | `Resource(hash_log_data=False, ...)` constructor parameter |

> **Note:** `OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL`, `OPENSHIFT_PYTHON_WRAPPER_LOG_FILE`, `REUSE_IF_RESOURCE_EXISTS`, and `SKIP_RESOURCE_TEARDOWN` can **only** be configured via environment variables.

## Related Pages

- [Connecting to Clusters](connecting-to-clusters.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Resource and NamespacedResource API](resource-api.html)
- [Common Resource Patterns](common-patterns.html)
- [Error Handling and Exception Reference](error-handling.html)
