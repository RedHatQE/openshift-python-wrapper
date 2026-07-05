Let me start by exploring the knowledge graph and understanding the repository structure.

Now let me look at the remaining VM-related resources and check the `RunStrategy` and `Status` constants, as well as the `data_volume.py`:

Now let me check how the `api_request` method works in the base `Resource` class:

Now let me look at the `data_volume.py` to check any VM-related interactions:

Now let me check the `RunStrategy` constants in VirtualMachineInstance:

Now let me look at the `Status` class in the base `Resource` for context and the VMI's `RunStrategy`:

Let me find the Status class definition:

Now let me check the `ApiGroup` constants for KubeVirt:

Now let me check for any tests related to VMs:

Now let me check the `deploy` and `clean_up` method signatures:

Now I have a thorough understanding of the VM-related API. Let me write the documentation:

# Working with Virtual Machines (KubeVirt)

Manage the full lifecycle of KubeVirt virtual machines on OpenShift — create VMs, start and stop them, live-migrate between nodes, take snapshots, and interact with their running instances — all from Python.

## Prerequisites

- `openshift-python-wrapper` installed (see [Installing and Creating Your First Resource](quickstart.html))
- A cluster connection configured (see [Connecting to Clusters](connecting-to-clusters.html))
- KubeVirt / OpenShift Virtualization installed on your cluster

## Quick Example

```python
from ocp_resources.virtual_machine import VirtualMachine

vm = VirtualMachine(
    name="my-vm",
    namespace="my-namespace",
    body={
        "spec": {
            "domain": {
                "devices": {"disks": [{"disk": {"bus": "virtio"}, "name": "rootdisk"}]},
                "resources": {"requests": {"memory": "1Gi"}},
            },
            "volumes": [{"name": "rootdisk", "containerDisk": {"image": "quay.io/containerdisks/fedora"}}],
        }
    },
)

with vm:
    vm.start(wait=True)
    print(f"VM ready: {vm.ready}")       # True
    print(f"Status: {vm.printable_status}")  # "Running"
    vm.stop(wait=True)
# VM is automatically cleaned up when the context manager exits
```

## Creating a VirtualMachine

```python
from ocp_resources.virtual_machine import VirtualMachine

vm = VirtualMachine(
    name="my-vm",
    namespace="my-namespace",
    body={
        "spec": {
            "domain": {
                "devices": {"disks": [{"disk": {"bus": "virtio"}, "name": "rootdisk"}]},
                "resources": {"requests": {"memory": "2Gi"}},
            },
            "volumes": [
                {
                    "name": "rootdisk",
                    "containerDisk": {"image": "quay.io/containerdisks/fedora"},
                }
            ],
        }
    },
)
vm.deploy()
```

The `body` parameter accepts a dictionary that maps to the KubeVirt VM `spec.template` structure. If you omit `body`, a minimal skeleton (`{"template": {"spec": {}}}`) is created automatically.

You can also create a VM from a YAML file:

```python
vm = VirtualMachine(
    name="my-vm",
    namespace="my-namespace",
    yaml_file="vm-definition.yaml",
)
vm.deploy()
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | `None` | Name of the VirtualMachine resource |
| `namespace` | `str` | `None` | Target namespace |
| `client` | `DynamicClient` | `None` | Kubernetes client; auto-resolved if omitted |
| `body` | `dict` | `None` | VM spec body dictionary |
| `teardown` | `bool` | `True` | Whether to delete the resource on cleanup |
| `yaml_file` | `str` | `None` | Path to a YAML file defining the VM |
| `delete_timeout` | `int` | `240` (seconds) | Timeout for delete operations |

> **Tip:** Use the context manager (`with vm:`) to ensure automatic cleanup. See [Creating and Managing Resources](creating-and-managing-resources.html) for details on `deploy()`, `clean_up()`, and context managers.

## Starting, Stopping, and Restarting

### Start a VM

```python
# Fire-and-forget
vm.start()

# Wait until the VM is ready
vm.start(wait=True)

# Custom timeout (seconds)
vm.start(timeout=600, wait=True)
```

### Stop a VM

```python
# Fire-and-forget
vm.stop()

# Wait for the VM to stop and the VMI to be deleted
vm.stop(wait=True)

# Custom timeouts
vm.stop(timeout=300, vmi_delete_timeout=300, wait=True)
```

### Restart a VM

```python
vm.restart(wait=True)
```

When `wait=True`, `restart()` waits for the old virt-launcher pod to be deleted and the new VMI to reach the `Running` state.

## Checking VM Status

```python
# Boolean ready status: True if running, None if stopped
vm.ready  # True

# Human-readable status string
vm.printable_status  # "Running", "Stopped", "Starting", "Migrating", etc.

# Wait for ready status
vm.wait_for_ready_status(status=True, timeout=300)   # Wait for running
vm.wait_for_ready_status(status=None, timeout=300)    # Wait for stopped

# Wait for a specific status field to clear
vm.wait_for_status_none(status="snapshotInProgress")
```

### Run Strategy Constants

Use built-in constants for the `runStrategy` field:

```python
VirtualMachine.RunStrategy.ALWAYS            # "Always"
VirtualMachine.RunStrategy.HALTED            # "Halted"
VirtualMachine.RunStrategy.MANUAL            # "Manual"
VirtualMachine.RunStrategy.RERUNONFAILURE    # "RerunOnFailure"
```

### Status Constants

```python
VirtualMachine.Status.STARTING       # "Starting"
VirtualMachine.Status.RUNNING        # "Running"  (inherited)
VirtualMachine.Status.STOPPED        # "Stopped"
VirtualMachine.Status.STOPPING       # "Stopping"
VirtualMachine.Status.MIGRATING      # "Migrating"
VirtualMachine.Status.PAUSED         # "Paused"
VirtualMachine.Status.PROVISIONING   # "Provisioning"
VirtualMachine.Status.ERROR_UNSCHEDULABLE  # "ErrorUnschedulable"
VirtualMachine.Status.DATAVOLUME_ERROR     # "DataVolumeError"
```

## Working with VirtualMachineInstances

Every running VM has an associated `VirtualMachineInstance` (VMI). Access it through the VM or create one directly.

### Accessing the VMI from a VM

```python
vmi = vm.vmi  # Returns a VirtualMachineInstance object
```

### Creating a Standalone VMI

```python
from ocp_resources.virtual_machine_instance import VirtualMachineInstance

vmi = VirtualMachineInstance(
    name="my-vmi",
    namespace="my-namespace",
    domain={
        "devices": {"disks": [{"disk": {"bus": "virtio"}, "name": "rootdisk"}]},
        "resources": {"requests": {"memory": "1Gi"}},
    },
    volumes=[
        {"name": "rootdisk", "containerDisk": {"image": "quay.io/containerdisks/fedora"}}
    ],
)
vmi.deploy()
```

> **Note:** The `domain` parameter is **required** when creating a VMI programmatically. Omitting it raises `MissingRequiredArgumentError`.

### VMI Constructor Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | `dict` | **Yes** | Domain spec (CPU, memory, devices) |
| `volumes` | `list` | No | Volumes to mount |
| `networks` | `list` | No | Network interfaces |
| `affinity` | `dict` | No | Scheduling affinity rules |
| `node_selector` | `dict` | No | Node label selector |
| `tolerations` | `list` | No | Toleration rules |
| `eviction_strategy` | `str` | No | `"LiveMigrate"`, `"LiveMigrateIfPossible"`, `"None"`, or `"External"` |
| `termination_grace_period_seconds` | `int` | No | Seconds to wait before force-killing |
| `hostname` | `str` | No | VM hostname |
| `priority_class_name` | `str` | No | Pod priority class |
| `scheduler_name` | `str` | No | Custom scheduler name |
| `start_strategy` | `str` | No | Set to `"Paused"` to start paused |
| `access_credentials` | `list` | No | Public keys to inject |
| `topology_spread_constraints` | `list` | No | Topology spread rules |

### Waiting for a VMI to Run

```python
vmi.wait_until_running(timeout=300)
```

If the VMI fails to start, `wait_until_running` raises `TimeoutExpiredError` and logs the virt-launcher pod status and logs for debugging. Set `logs=False` to suppress this:

```python
vmi.wait_until_running(timeout=300, logs=False)
```

You can also specify a `stop_status` to abort early if the VMI enters a failure state:

```python
vmi.wait_until_running(timeout=300, stop_status="Failed")
```

### Pausing and Unpausing

```python
vmi.pause(wait=True)    # Pause the VMI
vmi.unpause(wait=True)  # Resume the VMI
```

### Resetting a VMI

```python
vmi.reset()  # Hard-reset the VMI (like pressing the reset button)
```

### Getting the VMI Node

```python
node = vmi.get_node()
print(node.name)
```

### Network Interfaces

```python
# All interfaces from the VMI status
interfaces = vmi.interfaces

# Get IP address for a specific interface
ip = vmi.interface_ip("eth0")
```

### Guest Agent Information

When the QEMU guest agent is installed in the VM:

```python
vmi.guest_os_info       # OS information
vmi.guest_fs_info       # Filesystem information
vmi.guest_user_info     # Logged-in user information
vmi.os_version          # OS version string
```

> **Note:** If no guest agent is installed, `os_version` returns an empty dict and logs a warning.

### Accessing the Virt-Launcher Pod

```python
pod = vmi.get_virt_launcher_pod()
print(pod.name)
print(pod.status)

# Access logs from the compute container
logs = pod.log(container="compute")
```

For clusters where a privileged client is required:

```python
pod = vmi.get_virt_launcher_pod(privileged_client=admin_client)
```

### Accessing the Virt-Handler Pod

```python
handler_pod = vmi.get_virt_handler_pod(privileged_client=admin_client)
```

### Executing Virsh Commands

Run virsh commands inside the virt-launcher pod:

```python
# Get the XML definition
xml_output = vmi.get_xml()

# Get the XML as a parsed Python dict
xml_dict = vmi.get_xml_dict()

# Get domain memory stats
memstats = vmi.get_dommemstat()

# Run any arbitrary virsh command
output = vmi.execute_virsh_command(command="dominfo")
```

### Checking Root Status

```python
pod = vmi.get_virt_launcher_pod()

# Check if the virt-launcher pod runs as root
VirtualMachineInstance.is_pod_root(pod=pod)  # True or False

# Get the pod's runAsUser UID
VirtualMachineInstance.get_pod_user_uid(pod=pod)  # int or None
```

## Live Migration

Trigger a live migration by creating a `VirtualMachineInstanceMigration`:

```python
from ocp_resources.virtual_machine_instance_migration import VirtualMachineInstanceMigration

migration = VirtualMachineInstanceMigration(
    name="migrate-my-vm",
    namespace="my-namespace",
    vmi_name="my-vm",
)
migration.deploy()
```

Monitor migration by checking the VMI's status. Once migration completes, the VMI runs on the target node. See [Waiting for Resource Conditions and Status](waiting-for-conditions.html) for condition-based waiting.

### Migration Resource Quotas

Control resource allocation for migrations:

```python
from ocp_resources.virtual_machine_migration_resource_quota import VirtualMachineMigrationResourceQuota

quota = VirtualMachineMigrationResourceQuota(
    name="migration-quota",
    namespace="my-namespace",
    requests_cpu="2",
    requests_memory="4Gi",
    limits_cpu="4",
    limits_memory="8Gi",
)
quota.deploy()
```

## Snapshots and Restores

### Taking a Snapshot

```python
from ocp_resources.virtual_machine_snapshot import VirtualMachineSnapshot

snapshot = VirtualMachineSnapshot(
    name="my-vm-snapshot",
    namespace="my-namespace",
    vm_name="my-vm",
)
snapshot.deploy()

# Wait for the snapshot to be ready
snapshot.wait_ready_to_use(timeout=300)

# Wait for both snapshot readiness AND the VM's snapshotInProgress to clear
snapshot.wait_snapshot_done(timeout=300)
```

### Restoring from a Snapshot

```python
from ocp_resources.virtual_machine_restore import VirtualMachineRestore

restore = VirtualMachineRestore(
    name="my-vm-restore",
    namespace="my-namespace",
    vm_name="my-vm",
    snapshot_name="my-vm-snapshot",
)
restore.deploy()

# Wait for restore to complete
restore.wait_restore_done(timeout=300)
```

The `wait_restore_done()` method checks both the restore's `complete` status and that the VM's `restoreInProgress` field is cleared.

| Parameter | Type | Description |
|---|---|---|
| `vm_name` | `str` | Target VirtualMachine name |
| `snapshot_name` | `str` | Source VirtualMachineSnapshot name |
| `volume_restore_policy` | `str` | Optional policy for volume restoration |

## Cloning VMs

```python
from ocp_resources.virtual_machine_clone import VirtualMachineClone

clone = VirtualMachineClone(
    name="clone-my-vm",
    namespace="my-namespace",
    source_name="my-vm",
    target_name="my-vm-clone",
)
clone.deploy()
```

> **Note:** `source_name` is **required**. If omitted, `MissingRequiredArgumentError` is raised.

### Clone Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `source_name` | `str` | **Required** | Name of the source VM |
| `source_kind` | `str` | `"VirtualMachine"` | Kind of the source resource |
| `target_name` | `str` | Auto-generated | Name for the cloned VM |
| `label_filters` | `list` | `None` | Labels to copy, e.g. `["*", "!someKey/*"]` |
| `annotation_filters` | `list` | `None` | Annotations to copy |
| `new_mac_addresses` | `dict` | `None` | Override MACs: `{"nic0": "00:11:22:33:44:55"}` |
| `new_smbios_serial` | `str` | `None` | Override SMBIOS serial number |
| `volume_name_policy` | `str` | `None` | Volume naming policy for the clone |

## Exporting VMs

```python
from ocp_resources.virtual_machine_export import VirtualMachineExport

export = VirtualMachineExport(
    name="export-my-vm",
    namespace="my-namespace",
    source={"apiGroup": "kubevirt.io", "kind": "VirtualMachine", "name": "my-vm"},
    token_secret_ref="my-export-token",
    ttl_duration="1h",
)
export.deploy()
```

> **Note:** The `source` parameter is **required**. If omitted, `MissingRequiredArgumentError` is raised.

## Advanced Usage

### Instance Types and Preferences

KubeVirt instance types define reusable VM sizing profiles. Preferences define non-sizing defaults (clock, firmware, devices).

#### Namespaced Instance Type

```python
from ocp_resources.virtual_machine_instancetype import VirtualMachineInstancetype

instancetype = VirtualMachineInstancetype(
    name="small",
    namespace="my-namespace",
    cpu={"guest": 2},
    memory={"guest": "4Gi"},
)
instancetype.deploy()
```

Both `cpu` and `memory` are **required**. Omitting either raises `MissingRequiredArgumentError`.

#### Cluster-Scoped Instance Type

```python
from ocp_resources.virtual_machine_cluster_instancetype import VirtualMachineClusterInstancetype

cluster_instancetype = VirtualMachineClusterInstancetype(
    name="large",
    cpu={"guest": 8},
    memory={"guest": "16Gi"},
    gpus=[{"deviceName": "nvidia.com/A100", "name": "gpu0"}],
)
cluster_instancetype.deploy()
```

#### Namespaced Preference

```python
from ocp_resources.virtual_machine_preference import VirtualMachinePreference

preference = VirtualMachinePreference(
    name="linux-pref",
    namespace="my-namespace",
    cpu={"preferredCPUTopology": "preferSockets"},
    firmware={"preferredUseEfi": True},
)
preference.deploy()
```

#### Cluster-Scoped Preference

```python
from ocp_resources.virtual_machine_cluster_preference import VirtualMachineClusterPreference

cluster_preference = VirtualMachineClusterPreference(
    name="windows-pref",
    clock={"preferredTimer": {"hpet": {"present": False}}},
    features={"preferredHyperv": {"spinlocks": {"spinlocks": 8191}}},
)
cluster_preference.deploy()
```

### VMI Replica Sets

Scale out VMIs horizontally:

```python
from ocp_resources.virtual_machine_instance_replica_set import VirtualMachineInstanceReplicaSet

replica_set = VirtualMachineInstanceReplicaSet(
    name="my-vmi-rs",
    namespace="my-namespace",
    replicas=3,
    selector={"matchLabels": {"app": "my-vmi"}},
    template={
        "metadata": {"labels": {"app": "my-vmi"}},
        "spec": {
            "domain": {
                "devices": {},
                "resources": {"requests": {"memory": "1Gi"}},
            }
        },
    },
)
replica_set.deploy()
```

Both `selector` and `template` are **required**.

### Storage Migration

Migrate VM storage between storage classes:

```python
from ocp_resources.virtual_machine_storage_migration_plan import VirtualMachineStorageMigrationPlan
from ocp_resources.virtual_machine_storage_migration import VirtualMachineStorageMigration

# Create a migration plan
plan = VirtualMachineStorageMigrationPlan(
    name="migrate-storage",
    namespace="my-namespace",
    virtual_machines=[
        {"name": "my-vm", "volumes": [{"name": "rootdisk", "target": {"storageClassName": "fast-ssd"}}]}
    ],
    retention_policy="deleteSource",
)
plan.deploy()

# Execute the migration
migration = VirtualMachineStorageMigration(
    name="migrate-storage-exec",
    namespace="my-namespace",
    virtual_machine_storage_migration_plan_ref={"name": "migrate-storage", "namespace": "my-namespace"},
)
migration.deploy()
```

### VM Templates

```python
from ocp_resources.virtual_machine_template import VirtualMachineTemplate

template = VirtualMachineTemplate(
    name="fedora-template",
    namespace="my-namespace",
    virtual_machine={
        "spec": {
            "template": {
                "spec": {
                    "domain": {
                        "devices": {},
                        "resources": {"requests": {"memory": "2Gi"}},
                    }
                }
            }
        }
    },
    parameters=[
        {"name": "VM_NAME", "description": "Name of the VM", "required": True}
    ],
    message="Use this template to create Fedora VMs.",
)
template.deploy()
```

### Listing VMs Across Namespaces

```python
# List all VMs in a namespace
for vm in VirtualMachine.get(namespace="my-namespace"):
    print(f"{vm.name}: {vm.instance.get('status', {}).get('printableStatus')}")

# List with label selectors
for vm in VirtualMachine.get(
    namespace="my-namespace",
    label_selector="app=webserver",
):
    print(vm.name)
```

See [Querying and Watching Resources](querying-resources.html) for more query options.

### Getting VM Network Interfaces

```python
interfaces = vm.get_interfaces()
for iface in interfaces:
    print(f"Name: {iface['name']}, Model: {iface.get('model', 'default')}")
```

## Troubleshooting

### VM Stuck in "Starting" Status

Check the VMI's virt-launcher pod for scheduling or image-pull issues:

```python
vmi = vm.vmi
try:
    pod = vmi.get_virt_launcher_pod()
    print(f"Pod status: {pod.status}")
    print(pod.log(container="compute"))
except ResourceNotFoundError:
    print("Virt-launcher pod not found — VM may not have been scheduled yet")
```

### TimeoutExpiredError on start/stop

Increase the timeout parameter:

```python
vm.start(timeout=600, wait=True)  # 10 minutes instead of default 4
```

### MissingRequiredArgumentError

This is raised when a required constructor parameter is missing. Common cases:

| Resource | Required Parameters |
|---|---|
| `VirtualMachineInstance` | `domain` |
| `VirtualMachineInstancetype` | `cpu`, `memory` |
| `VirtualMachineClone` | `source_name` |
| `VirtualMachineExport` | `source` |
| `VirtualMachineInstanceReplicaSet` | `selector`, `template` |
| `VirtualMachineStorageMigration` | `virtual_machine_storage_migration_plan_ref` |
| `VirtualMachineTemplate` | `virtual_machine` |

### Guest Agent Not Reporting

If `vmi.os_version` returns an empty dict, the QEMU guest agent is not installed or not running inside the VM. Install and start `qemu-guest-agent` in the guest OS.

## Related Pages

- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html)
- [Querying and Watching Resources](querying-resources.html)
- [Common Resource Patterns](common-patterns.html)
- [Executing Commands in Pods and Retrieving Logs](pod-execution-and-logs.html)
