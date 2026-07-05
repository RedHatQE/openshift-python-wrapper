Let me explore the repository structure and understand the codebase first.

Now let me check the `read_namespaced_pod_log` kwargs available, and look at how the MCP server uses log parameters:

Now let me check the import paths and verify the `get_client` function:

Now let me check test files for pod execution tests:

Now let me also verify whether the Node class has a `name` property:

Now I have all the information I need to write the documentation. Let me compose it:

# Executing Commands in Pods and Retrieving Logs

Run commands inside running pods and retrieve their logs to debug and interact with workloads on your OpenShift or Kubernetes cluster.

## Prerequisites

- A connected cluster client (see [Connecting to Clusters](connecting-to-clusters.html))
- An existing, running pod you want to interact with

## Quick Example

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()
pod = Pod(client=client, name="my-app", namespace="default")

# Run a command inside the pod
output = pod.execute(command=["echo", "hello"])
print(output)  # "hello\n"

# Get pod logs
logs = pod.log()
print(logs)
```

## Executing Commands with `Pod.execute()`

`Pod.execute()` runs a command inside a pod container using the Kubernetes exec API and returns the standard output as a string.

### Method Signature

```python
Pod.execute(
    command: list[str],
    timeout: int = 60,
    container: str = "",
    ignore_rc: bool = False,
) -> str
```

| Parameter   | Type         | Default | Description                                                                                 |
|-------------|--------------|---------|---------------------------------------------------------------------------------------------|
| `command`   | `list[str]`  | —       | The command to run, as a list of strings (e.g., `["ls", "-la", "/tmp"]`)                    |
| `timeout`   | `int`        | `60`    | Maximum seconds to wait for the command to complete                                         |
| `container` | `str`        | `""`    | Container name to execute in. If empty, uses the first container in the pod spec            |
| `ignore_rc` | `bool`       | `False` | When `True`, return stdout even if the command exits with a non-zero return code            |

**Returns:** `str` — the standard output of the command.

**Raises:** `ExecOnPodError` — when the command fails (non-zero exit code) and `ignore_rc` is `False`.

### Step-by-Step: Running a Simple Command

1. Get a reference to the pod:

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()
pod = Pod(client=client, name="my-app", namespace="my-namespace")
```

2. Execute a command:

```python
output = pod.execute(command=["cat", "/etc/hostname"])
print(output)
```

3. Use the result for further logic:

```python
files = pod.execute(command=["ls", "/app/data"])
for filename in files.strip().split("\n"):
    print(f"Found: {filename}")
```

### Selecting a Container

For multi-container pods, specify which container to run the command in. If you omit `container`, the first container defined in the pod spec is used.

```python
# Execute in a specific container
output = pod.execute(
    command=["cat", "/var/log/app.log"],
    container="sidecar",
)
```

### Setting a Timeout

Long-running commands may need a longer timeout. The default is 60 seconds.

```python
# Allow up to 5 minutes for a heavy operation
output = pod.execute(
    command=["pg_dump", "mydb"],
    timeout=300,
)
```

When the timeout is exceeded, an `ExecOnPodError` is raised with the error message `"stream resp is closed"`.

### Ignoring Non-Zero Exit Codes

Some commands return a non-zero exit code as part of normal operation (e.g., `grep` returns 1 when no match is found). Use `ignore_rc=True` to get the output regardless:

```python
# grep returns exit code 1 when there's no match — don't treat that as an error
output = pod.execute(
    command=["grep", "ERROR", "/var/log/app.log"],
    ignore_rc=True,
)
if output:
    print("Errors found:", output)
else:
    print("No errors in logs")
```

### Handling Errors with `ExecOnPodError`

When a command fails, `ExecOnPodError` provides structured access to the failure details.

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ExecOnPodError

try:
    pod.execute(command=["ls", "/nonexistent"])
except ExecOnPodError as e:
    print(f"Command: {e.cmd}")      # ['ls', '/nonexistent']
    print(f"Return code: {e.rc}")   # Non-zero exit code (or -1 for stream errors)
    print(f"Stdout: {e.out}")       # Standard output captured before failure
    print(f"Stderr: {e.err}")       # Standard error or error channel details
```

`ExecOnPodError` attributes:

| Attribute | Type        | Description                                                          |
|-----------|-------------|----------------------------------------------------------------------|
| `cmd`     | `list[str]` | The command that was executed                                        |
| `rc`      | `int`       | Return code (`-1` for stream/timeout errors, otherwise the exit code)|
| `out`     | `str`       | Standard output captured from the command                            |
| `err`     | `str` or `dict` | Standard error output, or the Kubernetes error channel response  |

> **Tip:** For a complete list of all custom exceptions, see [Error Handling and Exception Reference](error-handling.html).

## Retrieving Logs with `Pod.log()`

`Pod.log()` returns the logs from a pod container as a string. It passes keyword arguments directly to the Kubernetes `read_namespaced_pod_log` API.

### Basic Usage

```python
logs = pod.log()
print(logs)
```

### Common Keyword Arguments

Pass any parameter supported by the Kubernetes `read_namespaced_pod_log` API:

| Parameter       | Type   | Description                                               |
|-----------------|--------|-----------------------------------------------------------|
| `container`     | `str`  | Container name to get logs from (required for multi-container pods) |
| `previous`      | `bool` | Return logs from a previous terminated container instance  |
| `tail_lines`    | `int`  | Number of lines from the end of the logs to return         |
| `since_seconds` | `int`  | Only return logs newer than this many seconds              |

### Examples

```python
# Get logs from a specific container
logs = pod.log(container="nginx")

# Get the last 50 lines
logs = pod.log(tail_lines=50)

# Get logs from the last 5 minutes
logs = pod.log(since_seconds=300)

# Get logs from a crashed container's previous instance
logs = pod.log(container="app", previous=True)
```

## Accessing Pod Properties

Beyond executing commands and reading logs, the `Pod` class provides properties for inspecting the pod's runtime state.

### Getting the Node

The `node` property returns a `Node` object for the node where the pod is scheduled:

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()

for pod in Pod.get(client=client, label_selector="app=my-app"):
    node = pod.node
    print(f"Pod {pod.name} is running on node {node.name}")
```

> **Note:** The `node` property raises an `AssertionError` if the pod has not yet been scheduled to a node.

### Getting the Pod IP Address

The `ip` property returns the pod's IP address from its status:

```python
pod_ip = pod.ip
print(f"Pod IP: {pod_ip}")
```

### Getting the Pod Status

The `status` property (inherited from the base resource class) returns the pod's phase:

```python
print(f"Pod status: {pod.status}")  # e.g., "Running", "Pending", "Succeeded"
```

## Advanced Usage

### Iterating Over Pods with Selectors

Combine `Pod.get()` with `execute()` or `log()` to debug across multiple pods:

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ExecOnPodError
from ocp_resources.resource import get_client

client = get_client()

for pod in Pod.get(client=client, namespace="production", label_selector="app=web"):
    try:
        uptime = pod.execute(command=["uptime"])
        print(f"{pod.name} on {pod.node.name}: {uptime.strip()}")
    except ExecOnPodError as e:
        print(f"{pod.name}: command failed — {e}")
```

### Executing in Multi-Container Pods

When pods contain sidecar containers (e.g., logging or proxy containers), always specify the target container explicitly:

```python
# Main application container
app_output = pod.execute(command=["cat", "/app/config.yaml"], container="app")

# Envoy sidecar
proxy_stats = pod.execute(command=["curl", "localhost:15000/stats"], container="istio-proxy")

# Logs from each container
app_logs = pod.log(container="app", tail_lines=100)
proxy_logs = pod.log(container="istio-proxy", tail_lines=100)
```

### Collecting Debug Information

A practical recipe for gathering debugging data from a running pod:

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ExecOnPodError
from ocp_resources.resource import get_client

client = get_client()
pod = Pod(client=client, name="my-app", namespace="default")

debug_info = {
    "pod_name": pod.name,
    "node": pod.node.name,
    "ip": pod.ip,
    "status": pod.status,
    "logs_tail": pod.log(tail_lines=20),
}

# Safely attempt commands that might fail
for cmd_name, cmd in [("env", ["env"]), ("df", ["df", "-h"]), ("ps", ["ps", "aux"])]:
    try:
        debug_info[cmd_name] = pod.execute(command=cmd, timeout=10)
    except ExecOnPodError:
        debug_info[cmd_name] = "command failed"

for key, value in debug_info.items():
    print(f"--- {key} ---\n{value}\n")
```

### Using Pod Context Manager for Temporary Pods

Create a pod, run commands, and clean up automatically:

```python
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client

client = get_client()

with Pod(
    client=client,
    name="debug-pod",
    namespace="default",
    containers=[{
        "name": "debug",
        "image": "registry.access.redhat.com/ubi9/ubi:latest",
        "command": ["sleep", "3600"],
    }],
) as pod:
    pod.wait_for_status(status=Pod.Status.RUNNING, timeout=120)
    output = pod.execute(command=["cat", "/etc/os-release"])
    print(output)
# Pod is automatically deleted when the context manager exits
```

> **Note:** See [Creating and Managing Resources](creating-and-managing-resources.html) for more about context managers and resource lifecycle.

## Troubleshooting

### `ExecOnPodError` with `"stream resp is closed"`

This typically means the command timed out. Increase the `timeout` parameter:

```python
pod.execute(command=["long-running-script.sh"], timeout=300)
```

### `AssertionError: Node not found for pod <name>`

The pod is not yet scheduled. Wait for it to be running before accessing `pod.node`:

```python
pod.wait_for_status(status=Pod.Status.RUNNING, timeout=120)
node = pod.node
```

### `ExecOnPodError` with return code `-1` and an error channel dict

This indicates a Kubernetes-level failure (e.g., container not found, pod not running). Check that:

- The pod is in `Running` status
- The `container` name matches one defined in the pod spec
- The container has started and is not in `CrashLoopBackOff`

### Logs return empty string

The container may not have produced any output yet, or it may have restarted. Try:

```python
# Check previous container instance
logs = pod.log(previous=True)

# Or narrow to recent logs
logs = pod.log(since_seconds=60)
```

## Related Pages

- [Common Resource Patterns](common-patterns.html)
- [Working with Kubernetes Events](working-with-events.html)
- [Error Handling and Exception Reference](error-handling.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Working with Virtual Machines (KubeVirt)](working-with-virtual-machines.html)
