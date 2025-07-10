# OpenShift Python Wrapper MCP Server

This MCP (Model Context Protocol) server provides tools to interact with OpenShift/Kubernetes resources using the `ocp_resources` library.

## Features

The MCP server exposes the following tools:

### Resource Management
- **list_resources** - List resources of a specific type with optional filtering
- **get_resource** - Get detailed information about a specific resource
- **create_resource** - Create new resources from YAML or programmatically
- **update_resource** - Update existing resources using patches
- **delete_resource** - Delete resources
- **apply_yaml** - Apply YAML manifests containing one or more resources

### Pod Operations
- **get_pod_logs** - Retrieve logs from pod containers
- **exec_in_pod** - Execute commands inside pod containers

### Utilities
- **get_resource_events** - Get events related to specific resources
- **get_resource_types** - List all available resource types

## Installation

1. Ensure you have the openshift-python-wrapper installed with FastMCP support:
```bash
pip install openshift-python-wrapper[mcp]
```

2. Make sure you have a valid kubeconfig file configured to connect to your cluster.

## Running the Server

### Standalone Mode

Run the MCP server directly:

```bash
python mcp_server/server.py
```

Or using the FastMCP CLI:

```bash
fastmcp run mcp_server/server.py
```

### Development Mode

For development with the MCP Inspector:

```bash
fastmcp dev mcp_server/server.py
```

### Integration with Cursor

To use this MCP server with Cursor, add the following to your Cursor settings (~/.cursor/mcp.json):

**Option 1: Using the launch script (recommended)**
```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "/home/myakove/git/openshift-python-wrapper/mcp_server/launch.sh"
    }
  }
}
```

**Option 2: Using uv directly**
```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "uv",
      "args": ["run", "/home/myakove/git/openshift-python-wrapper/mcp_server/server.py"]
    }
  }
}
```

Note: If you need to specify a custom kubeconfig, add the env section:
```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "uv",
      "args": ["run", "/home/myakove/git/openshift-python-wrapper/mcp_server/server.py"],
      "env": {
        "KUBECONFIG": "/home/myakove/.kube/config"
      }
    }
  }
}
```

Then restart Cursor and use the server with `@openshift-python-wrapper` in your prompts.

## Configuration

The server uses your default kubeconfig file to connect to the cluster. You can specify a different context or config file by setting environment variables:

```bash
export KUBECONFIG=/path/to/kubeconfig
```

## Usage Examples

### List all pods in a namespace
```json
{
  "tool": "list_resources",
  "arguments": {
    "resource_type": "pod",
    "namespace": "default"
  }
}
```

### Get specific deployment details
```json
{
  "tool": "get_resource",
  "arguments": {
    "resource_type": "deployment",
    "name": "my-app",
    "namespace": "production",
    "output_format": "yaml"
  }
}
```

### Create a new namespace
```json
{
  "tool": "create_resource",
  "arguments": {
    "resource_type": "namespace",
    "name": "test-namespace",
    "spec": {}
  }
}
```

### Apply YAML manifest
```json
{
  "tool": "apply_yaml",
  "arguments": {
    "yaml_content": "apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: my-config\n  namespace: default\ndata:\n  key: value"
  }
}
```

### Get pod logs
```json
{
  "tool": "get_pod_logs",
  "arguments": {
    "name": "my-pod",
    "namespace": "default",
    "tail_lines": 50
  }
}
```

## Supported Resource Types

The server supports all standard Kubernetes resources and OpenShift-specific resources:

### Workloads
- pod, deployment, replicaset, daemonset, job, cronjob

### Services & Networking
- service, route, networkpolicy

### Configuration & Storage
- configmap, secret, persistentvolume, persistentvolumeclaim, storageclass

### RBAC
- serviceaccount, role, rolebinding, clusterrole, clusterrolebinding

### Cluster Resources
- namespace, node, event, limitrange, resourcequota

### OpenShift Specific
- project, route, imagestream, template

## Error Handling

All tools return structured responses with error information when operations fail:

```json
{
  "error": "Description of what went wrong",
  "type": "ExceptionType"
}
```

## Security Considerations

- The server uses the credentials from your kubeconfig file
- Ensure proper RBAC permissions are configured for the service account or user
- Be cautious when exposing the MCP server over a network

## Contributing

Contributions are welcome! Please ensure that any new resource types are properly added to the `RESOURCE_TYPES` mapping and imported correctly.
