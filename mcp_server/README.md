# OpenShift Python Wrapper MCP Server

An MCP (Model Context Protocol) server that provides powerful tools to interact with OpenShift/Kubernetes clusters using the `openshift-python-wrapper` library.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Access to an OpenShift/Kubernetes cluster
- Valid kubeconfig file

### Installation

```bash
# Install with uv (recommended)
uv tool install openshift-python-wrapper

# Or install with pip
pip install openshift-python-wrapper
```

### Running the Server

Once installed, you can run the MCP server with:

```bash
# Run the MCP server
openshift-mcp-server
```

For development or running from source:

```bash
# Clone and install in development mode
git clone https://github.com/RedHatQE/openshift-python-wrapper.git
cd openshift-python-wrapper

# Or run directly
uv run mcp_server/server.py
```

## 📋 Available Tools

### Resource Management

#### `list_resources`

List Kubernetes/OpenShift resources with filtering capabilities.

**Parameters:**

- `resource_type` (required): Type of resource (e.g., "pod", "deployment")
- `namespace` (optional): Namespace to search in
- `label_selector` (optional): Filter by labels (e.g., "app=nginx")
- `field_selector` (optional): Filter by fields
- `limit` (optional): Maximum number of results

**Example:**

```python
# List all pods in the default namespace
list_resources(resource_type="pod", namespace="default")

# List deployments with specific label
list_resources(resource_type="deployment", label_selector="app=frontend")
```

#### `get_resource`

Get detailed information about a specific resource.

**Parameters:**

- `resource_type` (required): Type of resource
- `name` (required): Resource name
- `namespace` (optional): Namespace (required for namespaced resources)
- `output_format` (optional): Format - "info", "yaml", "json", "wide" (default: "info")

**Example:**

```python
# Get pod details in YAML format
get_resource(resource_type="pod", name="nginx", namespace="default", output_format="yaml")
```

#### `create_resource`

Create a new resource from YAML or specifications.

**Parameters:**

- `resource_type` (required): Type of resource
- `name` (required): Resource name
- `namespace` (optional): Namespace for namespaced resources
- `yaml_content` (optional): Complete YAML definition
- `spec` (optional): Resource specification as dict
- `labels` (optional): Labels to apply
- `annotations` (optional): Annotations to apply
- `wait` (optional): Wait for resource to be ready

**Example:**

```python
# Create a namespace
create_resource(resource_type="namespace", name="test-ns", spec={})

# Create from YAML
yaml = """
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:latest
"""
create_resource(resource_type="pod", name="nginx", yaml_content=yaml)
```

#### `update_resource`

Update an existing resource using patch operations.

**Parameters:**

- `resource_type` (required): Type of resource
- `name` (required): Resource name
- `namespace` (optional): Namespace
- `patch` (required): Patch data as dict
- `patch_type` (optional): "merge", "strategic", "json" (default: "merge")

**Example:**

```python
# Scale a deployment
update_resource(
    resource_type="deployment",
    name="my-app",
    namespace="default",
    patch={"spec": {"replicas": 3}}
)
```

#### `delete_resource`

Delete a resource.

**Parameters:**

- `resource_type` (required): Type of resource
- `name` (required): Resource name
- `namespace` (optional): Namespace
- `wait` (optional): Wait for deletion to complete (default: true)
- `timeout` (optional): Deletion timeout in seconds (default: 60)

**Example:**

```python
delete_resource(resource_type="pod", name="nginx", namespace="default")
```

#### `apply_yaml`

Apply YAML manifests containing one or more resources.

**Parameters:**

- `yaml_content` (required): YAML content with one or more resources
- `namespace` (optional): Default namespace for resources without namespace

**Example:**

```python
yaml_content = """
---
apiVersion: v1
kind: Namespace
metadata:
  name: test-app
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: test-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
"""
apply_yaml(yaml_content=yaml_content)
```

### Pod Operations

#### `get_pod_logs`

Retrieve logs from pod containers.

**Parameters:**

- `name` (required): Pod name
- `namespace` (required): Namespace
- `container` (optional): Container name (for multi-container pods)
- `tail_lines` (optional): Number of lines from end
- `since_seconds` (optional): Logs since N seconds ago
- `previous` (optional): Get logs from previous container instance

**Example:**

```python
# Get last 100 lines of logs
get_pod_logs(name="my-app-abc123", namespace="production", tail_lines=100)

# Get logs from last hour
get_pod_logs(name="my-app-abc123", namespace="production", since_seconds=3600)
```

#### `exec_in_pod`

Execute commands inside pod containers.

**Parameters:**

- `name` (required): Pod name
- `namespace` (required): Namespace
- `command` (required): Command to execute as list
- `container` (optional): Container name

**Example:**

```python
# Check nginx config
exec_in_pod(
    name="nginx-pod",
    namespace="default",
    command=["nginx", "-t"]
)

# List files
exec_in_pod(
    name="my-app",
    namespace="default",
    command=["ls", "-la", "/app"]
)
```

### Event and Discovery

#### `get_resource_events`

Get Kubernetes events related to a resource.

**Parameters:**

- `resource_type` (required): Type of resource
- `name` (required): Resource name
- `namespace` (optional): Namespace
- `limit` (optional): Maximum events to return (default: 10)

**Example:**

```python
# Get pod events
get_resource_events(resource_type="pod", name="crashloop-pod", namespace="default")
```

#### `get_resource_types`

Get all available resource types.

**Parameters:**

- `random_string` (required): Any string (required by MCP protocol)

**Example:**

```python
get_resource_types(random_string="x")
```

## 🔧 Integration with AI Assistants

### Cursor Integration

Add to your Cursor settings (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "openshift-mcp-server"
    }
  }
}
```

Then use in Cursor with `@openshift-python-wrapper`.

### Claude Desktop Integration

Add to Claude Desktop config:

```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "openshift-mcp-server"
    }
  }
}
```

If you need to specify a custom kubeconfig location:

```json
{
  "mcpServers": {
    "openshift-python-wrapper": {
      "command": "openshift-mcp-server",
      "env": {
        "KUBECONFIG": "/home/user/.kube/config"
      }
    }
  }
}
```

## 🔍 Common Use Cases

### 1. Troubleshooting a Failing Pod

```python
# Check pod status
pod = get_resource("pod", "failing-app", "production")

# Get recent events
events = get_resource_events("pod", "failing-app", "production")

# Check logs
logs = get_pod_logs("failing-app", "production", tail_lines=200)

# Execute diagnostic command
exec_in_pod("failing-app", "production", ["cat", "/etc/app/config.yaml"])
```

### 2. Deploying a Complete Application

```python
# Apply all resources at once
yaml = """
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
"""
apply_yaml(yaml)
```

### 3. Checking Cluster Health

```python
# List nodes
nodes = list_resources("node")

# Check for pod issues
problem_pods = list_resources("pod", field_selector="status.phase!=Running,status.phase!=Succeeded")

# Review recent events
events = list_resources("event", limit=50)
```

### 4. Managing OpenShift Virtualization

```python
# Check CNV version
csv = list_resources("clusterserviceversion", namespace="openshift-cnv")

# List VMs
vms = list_resources("virtualmachine", namespace="my-vms")

# Check VM status
vm = get_resource("virtualmachine", "rhel9-vm", "my-vms")
```

## 📊 Supported Resource Types

The server dynamically discovers all available resource types from your cluster. Common types include:

### Core Kubernetes

- `pod`, `service`, `deployment`, `replicaset`, `daemonset`
- `configmap`, `secret`, `persistentvolume`, `persistentvolumeclaim`
- `namespace`, `node`, `event`, `endpoint`
- `serviceaccount`, `role`, `rolebinding`, `clusterrole`, `clusterrolebinding`

### OpenShift Specific

- `route`, `project`, `imagestream`, `buildconfig`, `deploymentconfig`
- `user`, `group`, `oauth`, `securitycontextconstraints`

### OpenShift Virtualization

- `virtualmachine`, `virtualmachineinstance`, `datavolume`
- `hyperconverged`, `kubevirt`, `cdi`

### Operators

- `clusterserviceversion`, `subscription`, `installplan`, `operatorgroup`
- `catalogsource`, `packagemanifest`

## 🛡️ Security Best Practices

1. **RBAC**: Ensure your kubeconfig has appropriate permissions
2. **Namespaces**: Use namespace isolation for multi-tenant environments
3. **Resource Limits**: Set appropriate limits when listing resources
4. **Sensitive Data**: Be careful with secrets and configmaps

## 🐛 Troubleshooting

### Connection Issues

```bash
# Test cluster connectivity
kubectl cluster-info

# Check kubeconfig
echo $KUBECONFIG
kubectl config current-context
```

### Permission Errors

```bash
# Check your permissions
kubectl auth can-i --list
```

### MCP Server Issues

```bash
# Run in debug mode
SIMPLE_LOGGER_LEVEL=DEBUG python mcp_server/server.py

# Check logs
tail -f /tmp/mcp_server_debug.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

### Adding New Resource Types

New resource types are automatically discovered from the cluster. To ensure proper support:

1. Add the resource module to `ocp_resources/`
2. Ensure it has `api_group` and `api_version` attributes
3. Test with the MCP server

## 📄 License

This project is licensed under the Apache License 2.0.
