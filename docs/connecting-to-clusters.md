Let me start by exploring the repository structure and the knowledge graph.

Now let me explore the client configuration and authentication code:

Now let me look at how the `client` parameter is used in the Resource class:

Now let me look at how resources accept the client parameter:

Now let me look at the NamespacedResource and how it handles client:

Now let me look at the tests for the client configuration:

Let me also check how environment variables relate to client configuration:

Now let me check how `get_client` is used with `generate_kubeconfig`:

Now let me look at the `conftest.py` for the tests to understand how fake_client is set up:

Let me also check the test file for more patterns of client usage:

Now let me check what environment variables are documented:

Now let me check the `generate_kubeconfig` related tests more carefully and how `DynamicClientWithKubeconfig` is used:

Now let me also look at how `get_client` is imported/used in other contexts to understand its full interface:

Let me look at some example files to see real usage patterns:

Now let me check the `get` classmethod for how client is used:

Now let me check for the `client_configuration` parameter and how `verify_ssl` is used:

Now I have all the information I need. Let me write the documentation page.

# Connecting to Clusters

Establish authenticated connections to Kubernetes and OpenShift clusters so you can create, query, and manage resources with openshift-python-wrapper.

## Prerequisites

- openshift-python-wrapper installed (see [Installing and Creating Your First Resource](quickstart.html))
- Access to a Kubernetes or OpenShift cluster (kubeconfig file, token, or in-cluster credentials)

## Quick Example

```python
from ocp_resources.resource import get_client
from ocp_resources.namespace import Namespace

# Connect using default kubeconfig (~/.kube/config or $KUBECONFIG)
client = get_client()

# Use the client with any resource
for ns in Namespace.get(client=client):
    print(ns.name)
```

## Creating a Client

All cluster connections go through `get_client()`, which returns a Kubernetes `DynamicClient`. Pass this client to every resource you create or query.

### Using the Default Kubeconfig

If you have a kubeconfig at `~/.kube/config` or the `KUBECONFIG` environment variable is set, no arguments are needed:

```python
from ocp_resources.resource import get_client

client = get_client()
```

The lookup order is:

1. The `config_file` parameter (if provided)
2. The `KUBECONFIG` environment variable
3. `~/.kube/config`

### Using a Specific Kubeconfig File

```python
client = get_client(config_file="/path/to/my/kubeconfig")
```

### Selecting a Context

If your kubeconfig has multiple contexts, select one by name:

```python
client = get_client(config_file="/path/to/kubeconfig", context="my-staging-cluster")
```

### Authenticating with a Bearer Token

Connect to a cluster API server directly using a host URL and token:

```python
client = get_client(
    host="https://api.my-cluster.example.com:6443",
    token="sha256~my-bearer-token",
)
```

### Authenticating with Username and Password (Basic Auth)

For OpenShift clusters that support OAuth-based basic authentication:

```python
client = get_client(
    host="https://api.my-cluster.example.com:6443",
    username="my-user",
    password="my-password",
)
```

> **Note:** Basic auth requires all three parameters: `host`, `username`, and `password`. This uses OpenShift's OAuth flow internally — it is not plain HTTP Basic Authentication.

### Using a Kubeconfig Dictionary

Pass a kubeconfig as a Python dictionary instead of a file path:

```python
config_dict = {
    "apiVersion": "v1",
    "kind": "Config",
    "clusters": [{"name": "my-cluster", "cluster": {"server": "https://api.example.com:6443"}}],
    "users": [{"name": "my-user", "user": {"token": "my-token"}}],
    "contexts": [{"name": "my-context", "context": {"cluster": "my-cluster", "user": "my-user"}}],
    "current-context": "my-context",
}

client = get_client(config_dict=config_dict)
```

## Passing the Client to Resources

Once you have a client, pass it to resource constructors and class methods:

```python
from ocp_resources.resource import get_client
from ocp_resources.namespace import Namespace
from ocp_resources.pod import Pod

client = get_client()

# Creating a resource
ns = Namespace(client=client, name="my-namespace")
ns.deploy()

# Querying resources
for pod in Pod.get(client=client, namespace="my-namespace"):
    print(pod.name)

# Using context managers
with Namespace(client=client, name="temp-namespace") as ns:
    ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=120)
```

> **Warning:** The `client` parameter will become mandatory in the next major release. Always pass it explicitly. If omitted, the library creates a client automatically using the default kubeconfig, but this triggers a `FutureWarning`.

## Environment Variables

`get_client()` respects several environment variables automatically:

| Variable | Purpose | Default |
|---|---|---|
| `KUBECONFIG` | Path to the kubeconfig file | `~/.kube/config` |
| `HTTPS_PROXY` | HTTPS proxy for cluster connections | None |
| `HTTP_PROXY` | HTTP proxy (used if `HTTPS_PROXY` is not set) | None |

> **Tip:** `HTTPS_PROXY` takes precedence over `HTTP_PROXY` when both are set.

For other environment variables that control logging, resource reuse, and teardown behavior, see [Environment Variables and Configuration](environment-variables.html).

## Advanced Usage

### Disabling TLS Verification

For development clusters with self-signed certificates:

```python
client = get_client(
    host="https://api.dev-cluster.example.com:6443",
    token="sha256~my-token",
    verify_ssl=False,
)
```

> **Warning:** Never disable TLS verification in production environments.

### In-Cluster Configuration

When your code runs inside a pod on the cluster (for example, in a CI/CD pipeline or operator), `get_client()` automatically falls back to in-cluster configuration if the kubeconfig-based connection fails:

```python
# Inside a pod — no config_file or host needed
client = get_client()
```

The library first attempts to connect using the kubeconfig. If that fails with a connection error, it loads credentials from the pod's service account token mounted at `/var/run/secrets/kubernetes.io/serviceaccount/`.

### Generating a Kubeconfig File from a Token Connection

When you connect with `host` and `token`, you might need a kubeconfig file on disk (for example, to pass to external tools). Use `generate_kubeconfig=True`:

```python
client = get_client(
    host="https://api.my-cluster.example.com:6443",
    token="sha256~my-token",
    generate_kubeconfig=True,
)

# Access the generated kubeconfig path
print(client.kubeconfig)
```

The generated kubeconfig file:
- Is written to a temporary file with `0o600` permissions
- Is automatically cleaned up when the process exits

If you already passed a `config_file`, the `generate_kubeconfig` flag reuses that file path instead of creating a new one.

### Passing a Custom Client Configuration

For fine-grained control over TLS settings, timeouts, or proxy configuration, pass a `kubernetes.client.Configuration` object:

```python
import kubernetes
from ocp_resources.resource import get_client

config = kubernetes.client.Configuration()
config.verify_ssl = False
config.proxy = "http://my-proxy:8080"

client = get_client(
    host="https://api.my-cluster.example.com:6443",
    token="sha256~my-token",
    client_configuration=config,
)
```

### Connecting to Multiple Clusters

Create separate clients for each cluster and pass them to different resources:

```python
from ocp_resources.resource import get_client
from ocp_resources.namespace import Namespace

prod_client = get_client(config_file="/path/to/prod-kubeconfig")
staging_client = get_client(config_file="/path/to/staging-kubeconfig")

# Query namespaces on both clusters
prod_namespaces = list(Namespace.get(client=prod_client))
staging_namespaces = list(Namespace.get(client=staging_client))
```

### Using the Fake Client for Testing

For unit tests that don't need a real cluster, pass `fake=True`:

```python
client = get_client(fake=True)
```

This returns a fake client that simulates Kubernetes API operations in memory. See [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html) for full details.

## `get_client()` API Reference

```python
from ocp_resources.resource import get_client

get_client(
    config_file: str | None = None,
    config_dict: dict | None = None,
    context: str | None = None,
    client_configuration: kubernetes.client.Configuration | None = None,
    persist_config: bool = True,
    temp_file_path: str | None = None,
    try_refresh_token: bool = True,
    username: str | None = None,
    password: str | None = None,
    host: str | None = None,
    verify_ssl: bool | None = None,
    token: str | None = None,
    fake: bool = False,
    generate_kubeconfig: bool = False,
) -> DynamicClient
```

| Parameter | Type | Description |
|---|---|---|
| `config_file` | `str \| None` | Path to a kubeconfig file |
| `config_dict` | `dict \| None` | Kubeconfig as a Python dictionary |
| `context` | `str \| None` | Name of the kubeconfig context to use |
| `client_configuration` | `Configuration \| None` | Custom `kubernetes.client.Configuration` object |
| `persist_config` | `bool` | Whether to persist config changes back to the kubeconfig file |
| `temp_file_path` | `str \| None` | Path for temporary kubeconfig file (used with `config_dict`) |
| `try_refresh_token` | `bool` | Attempt to refresh the authentication token (for in-cluster config) |
| `username` | `str \| None` | Username for basic authentication |
| `password` | `str \| None` | Password for basic authentication |
| `host` | `str \| None` | Cluster API server URL (e.g., `https://api.example.com:6443`) |
| `verify_ssl` | `bool \| None` | Set to `False` to skip TLS certificate verification |
| `token` | `str \| None` | Bearer token for authentication |
| `fake` | `bool` | Return a fake in-memory client for testing |
| `generate_kubeconfig` | `bool` | Save connection info to a temporary kubeconfig file accessible via `client.kubeconfig` |

**Returns:** `DynamicClient` — a Kubernetes dynamic client ready for resource operations.

**Raises:**
- `kubernetes.config.ConfigException` — if no valid kubeconfig is found and in-cluster config is unavailable
- `urllib3.exceptions.MaxRetryError` — if the cluster is unreachable (before falling back to in-cluster config)
- `ClientWithBasicAuthError` — if basic auth (username/password) fails

## Authentication Method Priority

When multiple authentication parameters are provided, `get_client()` uses this priority order:

1. **Basic auth** — if `username`, `password`, and `host` are all provided
2. **Token auth** — if `host` and `token` are provided
3. **Config dict** — if `config_dict` is provided
4. **Kubeconfig file** — uses `config_file`, `KUBECONFIG` env var, or `~/.kube/config`
5. **In-cluster config** — automatic fallback if the kubeconfig connection fails

## Troubleshooting

**"FutureWarning: 'client' arg will be mandatory"**
You are creating a resource without passing a `client`. Always call `get_client()` first and pass the result:

```python
client = get_client()
ns = Namespace(client=client, name="my-ns")  # Pass client explicitly
```

**Connection refused or timeout errors**
Verify your cluster is reachable and the kubeconfig or token is correct. Check that `HTTPS_PROXY` / `HTTP_PROXY` environment variables are set correctly if you are behind a proxy.

**"KUBECONFIG environment variable set in code is not detected"**
The Kubernetes Python client reads `KUBECONFIG` at module import time. If you set it dynamically in your code, pass the path directly instead:

```python
import os
# Don't rely on: os.environ["KUBECONFIG"] = "/path/to/config"
# Instead, pass it explicitly:
client = get_client(config_file=os.environ.get("KUBECONFIG", "/path/to/config"))
```

**Basic auth fails with `ClientWithBasicAuthError`**
Basic auth uses the OpenShift OAuth flow. Ensure your cluster has a well-known OAuth endpoint at `/.well-known/oauth-authorization-server`. This method does not work with vanilla Kubernetes clusters.

## Related Pages

- [Installing and Creating Your First Resource](quickstart.html)
- [Environment Variables and Configuration](environment-variables.html)
- [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Error Handling and Exception Reference](error-handling.html)
