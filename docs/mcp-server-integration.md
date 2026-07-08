# Integrating with AI Assistants via MCP Server

The openshift-python-wrapper ships with a built-in [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that lets AI assistants like Cursor, Claude Desktop, and other MCP-compatible tools directly manage your OpenShift/Kubernetes cluster resources.

## Configure the MCP Server for Cursor

Connect your Cursor IDE to your cluster so the AI assistant can list, create, update, and delete resources on your behalf.

```json
// ~/.cursor/mcp.json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "openshift-mcp-server"
    }
  }
}
```

After saving, restart Cursor and reference the server with `@openshift-python-wrapper` in your prompts. The server uses your active kubeconfig context automatically.

> **Note:** The `openshift-mcp-server` command is installed as a script entry point when you install the package. See [Installing and Creating Your First Resource](quickstart.html) for installation instructions.

## Configure the MCP Server for Claude Desktop

Set up Claude Desktop to interact with your cluster through natural language.

```json
// macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
// Windows: %APPDATA%\Claude\claude_desktop_config.json
// Linux: ~/.config/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "openshift-mcp-server"
    }
  }
}
```

Claude Desktop will connect to the server on startup. You can then ask it to list pods, create resources, check logs, and more using natural language.

## Configure a Custom Kubeconfig Path

Point the MCP server at a specific kubeconfig when your default location doesn't apply.

```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "openshift-mcp-server",
      "env": {
        "KUBECONFIG": "/home/user/.kube/my-cluster-config"
      }
    }
  }
}
```

The `KUBECONFIG` environment variable is passed to the server process at startup. This is useful when managing multiple clusters or when your kubeconfig is in a non-standard location.

> **Tip:** See [Connecting to Clusters](connecting-to-clusters.html) for all authentication methods supported by openshift-python-wrapper, including tokens, basic auth, and in-cluster config.

## Run the MCP Server from Source (Development)

Run the server directly from a cloned repository for development or testing.

```bash
git clone https://github.com/RedHatQE/openshift-python-wrapper.git
cd openshift-python-wrapper
uv run mcp_server/server.py
```

For MCP client configuration when running from source:

```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "uv",
      "args": ["run", "mcp_server/server.py"],
      "cwd": "/path/to/openshift-python-wrapper"
    }
  }
}
```

This bypasses the installed entry point and runs the server module directly, which is useful when testing local changes.

## List Cluster Resources via AI Chat

Ask your AI assistant to list resources — the MCP server exposes a `list_resources` tool that supports type filtering, namespaces, label selectors, and limits.

```
Prompt: "List all pods in the openshift-monitoring namespace with label app=prometheus"
```

The AI will call the `list_resources` tool, which maps to:

```python
list_resources(
    resource_type="pod",
    namespace="openshift-monitoring",
    label_selector="app=prometheus",
    limit=20
)
```

Returned data includes name, namespace, UID, creation timestamp, labels, phase, and conditions for each matched resource.

> **Tip:** Use `get_resource_types` to discover all available resource types. The server dynamically scans every module in `ocp_resources/` at startup, so any resource supported by the library — including OpenShift-specific types like `route`, `virtualmachine`, or `clusterserviceversion` — is available.

## Get Detailed Resource Information

Retrieve a single resource with full metadata, status, and optionally the raw YAML or JSON.

```
Prompt: "Show me the deployment 'api-server' in namespace 'production' as YAML"
```

The AI calls:

```python
get_resource(
    resource_type="deployment",
    name="api-server",
    namespace="production",
    output_format="yaml"    # also accepts "json" or "info"
)
```

The `info` format (default) returns structured metadata plus resource-specific details: for pods you get container statuses and node placement; for deployments you get replica counts; for services you get ports and cluster IP.

## Create Resources Through Natural Language

Ask the AI to create resources — it can use either YAML content or structured spec parameters.

```
Prompt: "Create a ConfigMap called 'app-settings' in the 'staging' namespace with keys
database_host=db.staging.svc and log_level=debug"
```

The AI calls:

```python
create_resource(
    resource_type="configmap",
    name="app-settings",
    namespace="staging",
    spec={"data": {"database_host": "db.staging.svc", "log_level": "debug"}},
    labels={"managed-by": "mcp-server"}
)
```

You can also provide full YAML:

```python
create_resource(
    resource_type="pod",
    name="nginx",
    yaml_content="""
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: default
spec:
  containers:
  - name: nginx
    image: nginx:1.27
    ports:
    - containerPort: 80
"""
)
```

> **Warning:** The MCP server creates real resources on your cluster. Make sure your AI assistant is targeting the correct cluster and namespace before confirming creation operations.

## Apply Multi-Document YAML Manifests

Deploy a complete application stack from a single YAML block containing multiple resources.

```
Prompt: "Apply this manifest to create a namespace, deployment, and service for my app"
```

The AI calls:

```python
apply_yaml(yaml_content="""
---
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: api
        image: myapp/backend:v1.0
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: my-app
spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 8080
""")
```

The response includes a summary with `total_resources`, `successful`, and `failed` counts, plus per-resource results. Each YAML document is parsed and deployed independently.

## Update Resources with Patches

Modify existing resources using merge or strategic-merge patches.

```
Prompt: "Scale the 'web-frontend' deployment in 'production' to 5 replicas"
```

The AI calls:

```python
update_resource(
    resource_type="deployment",
    name="web-frontend",
    namespace="production",
    patch={"spec": {"replicas": 5}},
    patch_type="merge"       # or "strategic"
)
```

The `patch_type` parameter controls the content type: `"merge"` uses `application/merge-patch+json`, while `"strategic"` uses `application/strategic-merge-patch+json`.

## Delete Resources

Remove resources with optional wait-for-deletion behavior.

```
Prompt: "Delete the pod 'debug-pod' in namespace 'default' and wait for it to be gone"
```

The AI calls:

```python
delete_resource(
    resource_type="pod",
    name="debug-pod",
    namespace="default",
    wait=True,
    timeout=60
)
```

If the resource doesn't exist, the server returns a success response with a warning rather than an error, making the operation idempotent.

## Retrieve Pod Logs

Fetch logs from running or crashed pods with filtering options.

```
Prompt: "Show me the last 200 lines of logs from pod 'api-server-7f8b9c' container 'app'
in namespace 'production'"
```

The AI calls:

```python
get_pod_logs(
    name="api-server-7f8b9c",
    namespace="production",
    container="app",
    tail_lines=200
)
```

- Use `since_seconds=3600` to get logs from the last hour
- Use `previous=True` to get logs from a crashed container's previous instance
- Omit `container` for single-container pods

## Execute Commands in Pods

Run diagnostic commands inside a running pod container.

```
Prompt: "Check the nginx config in pod 'web-server' namespace 'production'"
```

The AI calls:

```python
exec_in_pod(
    name="web-server",
    namespace="production",
    command=["nginx", "-t"],
    container="nginx"
)
```

The response includes `stdout`, `stderr`, and `returncode`. If the command fails, the exit code and error output are captured rather than raising an exception.

> **Warning:** Pod exec gives shell-level access to your containers. Ensure your RBAC policies restrict which service accounts and users can perform `exec` operations.

## Get Resource Events

Retrieve Kubernetes events related to a specific resource for troubleshooting.

```
Prompt: "Show me the events for pod 'crashloop-pod' in 'default' namespace"
```

The AI calls:

```python
get_resource_events(
    resource_type="pod",
    name="crashloop-pod",
    namespace="default",
    limit=10
)
```

Events are filtered using field selectors on `involvedObject.name`, `involvedObject.namespace`, and `involvedObject.kind`. Each event includes type (Normal/Warning), reason, message, count, timestamps, and source component.

## Troubleshoot a Failing Pod (End-to-End Workflow)

Combine multiple MCP tools in sequence to diagnose pod issues — the AI assistant will chain these calls automatically.

```
Prompt: "Pod 'payment-svc-6d4f8' in namespace 'checkout' keeps crashing. Help me figure out why."
```

The AI will typically execute this sequence:

1. **Check status:** `get_resource(resource_type="pod", name="payment-svc-6d4f8", namespace="checkout")` — gets phase, container statuses, restart count
2. **Review events:** `get_resource_events(resource_type="pod", name="payment-svc-6d4f8", namespace="checkout")` — shows scheduling, pulling, crash events
3. **Read current logs:** `get_pod_logs(name="payment-svc-6d4f8", namespace="checkout", tail_lines=100)` — application output before crash
4. **Read previous crash logs:** `get_pod_logs(name="payment-svc-6d4f8", namespace="checkout", previous=True)` — logs from the last terminated container
5. **Inspect config:** `exec_in_pod(name="payment-svc-6d4f8", namespace="checkout", command=["cat", "/etc/app/config.yaml"])` — verify mounted configuration

The AI then synthesizes all the data into a diagnosis with suggested fixes.

## Write a Programmatic MCP Client

Connect to the MCP server programmatically using `FastMCPClient` for automation scripts.

```python
import asyncio
from fastmcp import FastMCPClient


async def main():
    async with FastMCPClient() as client:
        await client.connect_stdio(cmd=["openshift-mcp-server"])

        # Discover available resource types
        types = await client.call_tool(
            name="get_resource_types",
            arguments={"random_string": "x"},
        )
        print(f"Available types: {types['total_count']}")

        # List pods in a namespace
        pods = await client.call_tool(
            name="list_resources",
            arguments={"resource_type": "pod", "namespace": "default", "limit": 5},
        )
        for pod in pods["resources"]:
            print(f"  {pod['name']} — {pod.get('phase', 'Unknown')}")


if __name__ == "__main__":
    asyncio.run(main())
```

This uses the same stdio transport that AI assistants use. The `FastMCPClient` is provided by the `fastmcp` library, which is already a dependency of openshift-python-wrapper.

## Debug MCP Server Issues

Enable debug logging and inspect the server log file when tools aren't behaving as expected.

```bash
# Check the MCP server log file
tail -f /tmp/mcp_server_debug.log
```

```bash
# Run with debug-level logging from the simple-logger
SIMPLE_LOGGER_LEVEL=DEBUG openshift-mcp-server
```

The server writes debug logs to `/tmp/mcp_server_debug.log` by default, including every resource scan at startup, client creation events, and detailed error tracebacks.

- Verify cluster connectivity independently: `kubectl cluster-info`
- Check your permissions: `kubectl auth can-i --list`
- Confirm the entry point is installed: `which openshift-mcp-server`

> **Tip:** See [Environment Variables and Configuration](environment-variables.html) for other environment variables that affect library behavior.

## Available MCP Tools Reference

The MCP server exposes ten tools. All resource type names are case-insensitive (e.g., `"Pod"`, `"pod"`, and `"POD"` all work).

| Tool | Purpose | Required Parameters |
|------|---------|-------------------|
| `list_resources` | List resources by type with optional filters | `resource_type` |
| `get_resource` | Get a single resource by name | `resource_type`, `name` |
| `create_resource` | Create a resource from spec or YAML | `resource_type`, `name`, plus `spec` or `yaml_content` |
| `update_resource` | Patch an existing resource | `resource_type`, `name`, `patch` |
| `delete_resource` | Delete a resource | `resource_type`, `name` |
| `get_pod_logs` | Retrieve pod container logs | `name`, `namespace` |
| `exec_in_pod` | Execute a command in a pod | `name`, `namespace`, `command` |
| `get_resource_events` | Get events for a resource | `resource_type`, `name` |
| `apply_yaml` | Apply one or more YAML documents | `yaml_content` |
| `get_resource_types` | List all discovered resource types | `random_string` (any value) |

> **Note:** Namespaced resources (pods, deployments, configmaps, etc.) require a `namespace` parameter. Cluster-scoped resources (nodes, namespaces, cluster roles) do not. The server validates this automatically and returns a clear error if a namespace is missing.

## Related Pages

- [Connecting to Clusters](connecting-to-clusters.html)
- [Installing and Creating Your First Resource](quickstart.html)
- [Environment Variables and Configuration](environment-variables.html)
- [Executing Commands in Pods and Retrieving Logs](pod-execution-and-logs.html)
- [Querying and Watching Resources](querying-resources.html)
