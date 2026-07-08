Let me start by reading the knowledge graph and page manifest, then explore the relevant source code.

Now let me examine the resource-specific wait methods, the `wait_for_condition` more closely, and the constants used:

Now let me look at the `Status` class, `Condition` class, and how `create` integrates with `wait`:

Now let me look at how Status/Condition are exposed on the base Resource class and how `deploy` / `create` uses wait:

Now let me see the `deploy` method more fully and how `wait` is passed through:

Now let me check the `sriov_network_node_state.py` and `virtual_machine_restore.py` for more wait patterns, and also look at the `TimeoutExpiredError` import:

Now let me check the `cdi_config.py` wait method and look at the `wait_for_resource` parameter in the constructor:

Now let me look at how `create` uses `wait`:

Now let me look at more of the `status` property:

Now I have all the information I need. Let me also check the `TimeoutSampler` import to understand the exception:

Let me check if there are any virtual machine import wait patterns with more stop_status details:

Now let me look at the `node_network_state.py` wait patterns:

I now have comprehensive understanding of all the wait methods. Let me compile the documentation.

# Waiting for Resource Conditions and Status

Wait for Kubernetes and OpenShift resources to reach a desired status, condition, or lifecycle state using built-in polling methods with configurable timeouts and early exit on failure.

## Prerequisites

- `openshift-python-wrapper` installed in your project
- A connected client (see [Connecting to Clusters](connecting-to-clusters.html))
- A resource instance to wait on (see [Creating and Managing Resources](creating-and-managing-resources.html))

## Quick Example

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-pod", namespace="default")
pod.create(wait=True)  # Creates the pod and waits for it to exist

# Wait for the pod to reach "Running" status
pod.wait_for_status(status=Pod.Status.RUNNING)
```

## Waiting for a Resource to Exist

The `wait()` method polls until a resource exists on the cluster. This is useful after creating a resource or when waiting for an external controller to produce one.

```python
from ocp_resources.namespace import Namespace

ns = Namespace(client=client, name="my-namespace")
ns.create()
ns.wait(timeout=120, sleep=2)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `int` | `240` (4 minutes) | Maximum seconds to wait |
| `sleep` | `int` | `1` | Seconds between polls |

**Raises:** `TimeoutExpiredError` if the resource does not appear before the timeout.

> **Tip:** Pass `wait=True` to `create()` or `deploy()` to combine creation and existence waiting in one call:
> ```python
> pod.create(wait=True)
> # or
> pod.deploy(wait=True)
> ```

## Waiting for Deletion

The `wait_deleted()` method polls until a resource no longer exists:

```python
pod.delete(wait=True, timeout=120)

# Or call wait_deleted() separately:
pod.delete()
success = pod.wait_deleted(timeout=120)
if not success:
    print("Resource still exists after timeout")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `int` | `240` (4 minutes) | Maximum seconds to wait |

**Returns:** `True` if the resource was deleted, `False` if the timeout was reached.

> **Note:** Unlike most wait methods, `wait_deleted()` returns `False` on timeout rather than raising an exception.

## Waiting for Status (Phase)

The `wait_for_status()` method polls `status.phase` until it matches the expected value:

```python
from ocp_resources.datavolume import DataVolume

dv = DataVolume(client=client, name="my-dv", namespace="default")
dv.wait_for_status(status=DataVolume.Status.SUCCEEDED, timeout=600)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `status` | `str` | *(required)* | Expected `status.phase` value |
| `timeout` | `int` | `240` (4 minutes) | Maximum seconds to wait |
| `stop_status` | `str \| None` | `Status.FAILED` | Status that aborts the wait immediately |
| `sleep` | `int` | `1` | Seconds between polls |
| `exceptions_dict` | `dict` | Protocol + cluster retry errors | Exceptions to catch and retry |

**Raises:** `TimeoutExpiredError` if the resource does not reach the desired status, or if `stop_status` is encountered.

### Using `stop_status` for early failure

By default, `wait_for_status()` aborts immediately if the resource enters a `"Failed"` phase. Override this to detect a different failure phase:

```python
from ocp_resources.virtual_machine_instance import VirtualMachineInstance

vmi = VirtualMachineInstance(client=client, name="my-vmi", namespace="default")
vmi.wait_for_status(
    status=VirtualMachineInstance.Status.RUNNING,
    stop_status="ErrorUnschedulable",
    timeout=300,
)
```

### Built-in status constants

Every resource inherits status constants from its base class. Resource-specific subclasses extend these with additional values:

```python
# Base status constants (available on all resources)
from ocp_resources.resource import Resource

Resource.Status.SUCCEEDED    # "Succeeded"
Resource.Status.FAILED       # "Failed"
Resource.Status.RUNNING      # "Running"
Resource.Status.PENDING      # "Pending"

# Resource-specific statuses
from ocp_resources.virtual_machine import VirtualMachine

VirtualMachine.Status.MIGRATING     # "Migrating"
VirtualMachine.Status.STOPPED       # "Stopped"
VirtualMachine.Status.STARTING      # "Starting"
VirtualMachine.Status.PAUSED        # "Paused"

from ocp_resources.persistent_volume_claim import PersistentVolumeClaim

PersistentVolumeClaim.Status.BOUND  # "Bound"
```

## Waiting for Conditions

The `wait_for_condition()` method waits for a specific entry in `status.conditions[]` to match a desired type, status, and optionally a reason or message:

```python
from ocp_resources.user_defined_network import UserDefinedNetwork

udn = UserDefinedNetwork(client=client, name="my-net", namespace="default")
udn.wait_for_condition(
    condition=UserDefinedNetwork.Condition.NETWORK_READY,
    status=UserDefinedNetwork.Condition.Status.TRUE,
    timeout=30,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `condition` | `str` | *(required)* | Condition type to match (e.g. `"Ready"`, `"Available"`) |
| `status` | `str` | *(required)* | Expected condition status (`"True"`, `"False"`, `"Unknown"`) |
| `timeout` | `int` | `300` (5 minutes) | Maximum seconds to wait |
| `sleep_time` | `int` | `1` | Seconds between polls |
| `reason` | `str \| None` | `None` | If set, the condition's `reason` field must also match |
| `message` | `str` | `""` | Text that must appear in the condition's `message` field |
| `stop_condition` | `str \| None` | `None` | A condition type that aborts the wait immediately |
| `stop_status` | `str` | `"True"` | The status of the stop condition that triggers early abort |

**Raises:**
- `TimeoutExpiredError` — if the condition is not met before the timeout
- `ConditionError` — if the `stop_condition` is detected before the desired condition

### Matching by reason and message

```python
pod.wait_for_condition(
    condition="Ready",
    status="True",
    reason="PodCompleted",
    message="containers with",
    timeout=120,
)
```

The `reason` must be an exact match. The `message` is checked using substring inclusion — the condition's message field must *contain* the provided string.

### Using `stop_condition` for early abort

Stop conditions let you fail fast when an unrecoverable condition appears:

```python
from ocp_resources.exceptions import ConditionError

try:
    resource.wait_for_condition(
        condition="Ready",
        status="True",
        stop_condition="Failed",
        stop_status="True",
        timeout=300,
    )
except ConditionError as e:
    print(f"Resource hit a failure condition: {e}")
```

> **Note:** The `stop_condition` matching only checks the condition `type` and `status`. The `reason` and `message` parameters are ignored when evaluating stop conditions.

### Built-in condition constants

```python
from ocp_resources.resource import Resource

# Condition types
Resource.Condition.READY         # "Ready"
Resource.Condition.AVAILABLE     # "Available"
Resource.Condition.DEGRADED      # "Degraded"
Resource.Condition.PROGRESSING   # "Progressing"
Resource.Condition.UPGRADEABLE   # "Upgradeable"
Resource.Condition.NETWORK_READY # "NetworkReady"

# Condition statuses
Resource.Condition.Status.TRUE    # "True"
Resource.Condition.Status.FALSE   # "False"
Resource.Condition.Status.UNKNOWN # "Unknown"

# Condition reasons
Resource.Condition.Reason.ALL_REQUIREMENTS_MET  # "AllRequirementsMet"
Resource.Condition.Reason.INSTALL_SUCCEEDED     # "InstallSucceeded"
```

## Waiting with Context Managers

When using a resource as a context manager, set `wait_for_resource=True` to automatically wait for the resource to exist after creation:

```python
from ocp_resources.pod import Pod

with Pod(
    client=client,
    name="my-pod",
    namespace="default",
    wait_for_resource=True,
) as pod:
    # Pod exists when you reach this line
    pod.wait_for_status(status=Pod.Status.RUNNING)
```

See [Creating and Managing Resources](creating-and-managing-resources.html) for more on context manager usage.

## Advanced Usage

### Waiting for any conditions to appear

The `wait_for_conditions()` method waits up to 30 seconds for the resource's `status.conditions` list to be populated (non-empty). This is useful when you need to inspect conditions but aren't sure they've been set yet:

```python
resource.wait_for_conditions()
# Now resource.instance.status.conditions is available
```

### Resource-specific wait methods

Many resource types provide specialized wait methods beyond the base `wait_for_status()` and `wait_for_condition()`. These methods encapsulate domain-specific logic.

#### Deployments

```python
from ocp_resources.deployment import Deployment

deploy = Deployment(client=client, name="my-app", namespace="default")
deploy.wait_for_replicas(deployed=True, timeout=240)   # All replicas ready
deploy.wait_for_replicas(deployed=False, timeout=120)   # Scale to zero complete
```

#### DaemonSets

```python
from ocp_resources.daemonset import DaemonSet

ds = DaemonSet(client=client, name="my-ds", namespace="default")
ds.wait_until_deployed(timeout=240)  # All desired pods are ready
```

#### VirtualMachines (KubeVirt)

```python
from ocp_resources.virtual_machine import VirtualMachine
from ocp_resources.virtual_machine_instance import VirtualMachineInstance

vm = VirtualMachine(client=client, name="my-vm", namespace="default")

# Wait for VM ready status (True = running, None = stopped)
vm.wait_for_ready_status(status=True, timeout=240)

# Wait for a specific status field to become None
vm.wait_for_status_none(status="snapshotInProgress", timeout=240)

# Wait for VMI to be running
vmi = VirtualMachineInstance(client=client, name="my-vm", namespace="default")
vmi.wait_until_running(timeout=240, logs=True)

# Wait for VMI pause state
vmi.wait_for_pause_status(pause=True, timeout=240)
```

See [Working with Virtual Machines (KubeVirt)](working-with-virtual-machines.html) for the full VM lifecycle.

#### DataVolumes

```python
from ocp_resources.datavolume import DataVolume

dv = DataVolume(client=client, name="my-dv", namespace="default")
dv.wait_for_dv_success(
    timeout=600,
    failure_timeout=120,
    pvc_wait_for_bound_timeout=60,
)
```

The `wait_for_dv_success()` method handles the full DataVolume lifecycle: it waits for the status to leave `Pending`, then waits for `Succeeded`, and finally confirms the PVC is `Bound`.

You can pass a `stop_status_func` callback to abort early on custom conditions:

```python
def dv_is_stuck(dv):
    return dv.instance.status.conditions.restartCount > 3

dv.wait_for_dv_success(
    stop_status_func=dv_is_stuck,
    dv=dv,  # passed as keyword argument to the function
)
```

#### VirtualMachineSnapshot / VirtualMachineRestore

```python
from ocp_resources.virtual_machine_snapshot import VirtualMachineSnapshot
from ocp_resources.virtual_machine_restore import VirtualMachineRestore

snapshot = VirtualMachineSnapshot(client=client, name="snap-1", namespace="default")
snapshot.wait_snapshot_done(timeout=240)    # readyToUse + VM snapshotInProgress is None

restore = VirtualMachineRestore(client=client, name="restore-1", namespace="default")
restore.wait_restore_done(timeout=240)     # complete + VM restoreInProgress is None
```

#### MachineSet

```python
from ocp_resources.machine_set import MachineSet

ms = MachineSet(client=client, name="worker-set", namespace="openshift-machine-api")
ms.wait_for_replicas(timeout=300, sleep=1)
```

Returns `True` when ready replicas match desired replicas, `False` on timeout.

#### NodeNetworkConfigurationPolicy

```python
from ocp_resources.node_network_configuration_policy import NodeNetworkConfigurationPolicy

nncp = NodeNetworkConfigurationPolicy(client=client, name="br1-policy")
nncp.wait_for_status_success()  # Uses the resource's own success_timeout
```

Raises `NNCPConfigurationFailed` if the policy fails or finds no matching nodes.

### Timeout constants

The library provides predefined timeout constants you can use with any wait method:

```python
from ocp_resources.utils.constants import (
    TIMEOUT_1SEC,       # 1
    TIMEOUT_5SEC,       # 5
    TIMEOUT_10SEC,      # 10
    TIMEOUT_30SEC,      # 30
    TIMEOUT_1MINUTE,    # 60
    TIMEOUT_2MINUTES,   # 120
    TIMEOUT_4MINUTES,   # 240
    TIMEOUT_10MINUTES,  # 600
)

pod.wait_for_status(status=Pod.Status.RUNNING, timeout=TIMEOUT_10MINUTES)
```

### Custom exception retries

Wait methods handle transient cluster errors automatically (connection resets, etcd leader changes, protocol errors). You can customize which exceptions are retried:

```python
from ocp_resources.utils.constants import (
    PROTOCOL_ERROR_EXCEPTION_DICT,
    DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
)

# Combine default retry exceptions
pod.wait_for_status(
    status=Pod.Status.RUNNING,
    exceptions_dict={
        **PROTOCOL_ERROR_EXCEPTION_DICT,
        **DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
    },
)
```

The default retry exceptions cover:
- `ProtocolError` — network-level failures
- `MaxRetryError`, `ConnectionAbortedError`, `ConnectionResetError` — connection failures
- `InternalServerError` — etcd leader changes, webhook failures, RPC errors
- `ServerTimeoutError` — API server timeouts
- `ForbiddenError` — context deadline exceeded errors

## Troubleshooting

### `TimeoutExpiredError` is raised unexpectedly

- **Increase the timeout.** The default is 240 seconds (4 minutes), which may not be enough for slow operations like DataVolume imports or VM migrations.
- **Check `stop_status`.** `wait_for_status()` defaults `stop_status` to `Status.FAILED`. If your resource legitimately passes through a `"Failed"` phase, set `stop_status` to a value that won't match, or set it to `None`.
- **Inspect the current status.** The error log includes the last observed status. Read it to understand where the resource got stuck.

### `ConditionError` on `wait_for_condition()`

This means the `stop_condition` was matched before the desired condition. The error message includes the full condition details. Review your `stop_condition` and `stop_status` settings.

### Resource exists but `wait_for_status()` times out

The `wait_for_status()` method reads from `status.phase`. Some resources use different status fields (e.g., `status.ready`, `status.readyToUse`, `status.syncStatus`). For those resources, use the resource-specific wait methods documented above, or use `wait_for_condition()` to match on `status.conditions[]` entries instead.

## Related Pages

- [Querying and Watching Resources](querying-resources.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Working with Virtual Machines (KubeVirt)](working-with-virtual-machines.html)
- [Error Handling and Exception Reference](error-handling.html)
- [Resource and NamespacedResource API](resource-api.html)
