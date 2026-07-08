Let me start by reading the knowledge graph and the pages manifest, then explore the codebase.

Now let me look at more resource files for networking, RBAC, and DataVolume:

Now let me look at the secret, network policy, network attachment definition, and the duplicate API groups handling:

Now let me look at the duplicate API groups handling:

Now let me look at some files with duplicate kinds to understand the pattern:

Now let me look at how to exec in pods and also look at the user_defined_network and apply_yaml approach:

Now let me look at how the `yaml_file` parameter works and look at the event-related code:

Now let me check some gateway files to see the pattern for duplicate API groups:

Now let me look at the `user_defined_network.py` for newer networking resources:

Now I have enough information. Let me write the documentation page:

# Common Resource Patterns

Copy-paste recipes for the most common Kubernetes and OpenShift resource operations using openshift-python-wrapper.

> **Note:** All recipes assume you already have a connected client. See [Connecting to Clusters](connecting-to-clusters.html) for setup instructions.

```python
# Preamble used by all recipes below
from ocp_resources.resource import get_client
client = get_client()
```

---

## Create and Run a Pod

Create a pod with a single container and wait for it to start.

```python
from ocp_resources.pod import Pod

pod = Pod(
    client=client,
    name="my-nginx",
    namespace="default",
    containers=[{
        "name": "nginx",
        "image": "nginx:1.25",
        "ports": [{"containerPort": 80}],
    }],
    restart_policy="Never",
)
pod.deploy()
pod.wait_for_status(status=Pod.Status.RUNNING, timeout=120)
```

The `deploy()` method creates the pod on the cluster. `wait_for_status` polls until the pod reaches `Running`. Use `restart_policy="Always"` for long-running pods.

---

## Create a Pod as a Context Manager

Automatically clean up a pod when the block exits — ideal for tests.

```python
from ocp_resources.pod import Pod

with Pod(
    client=client,
    name="test-curl",
    namespace="default",
    containers=[{
        "name": "curl",
        "image": "curlimages/curl:8.5.0",
        "command": ["sleep", "3600"],
    }],
) as pod:
    pod.wait_for_status(status=Pod.Status.RUNNING, timeout=60)
    output = pod.execute(command=["curl", "-s", "http://httpbin.org/get"])
    print(output)
# Pod is automatically deleted here
```

The context manager calls `deploy()` on enter and `clean_up()` on exit. Set `teardown=False` to skip automatic deletion.

> **Tip:** See [Creating and Managing Resources](creating-and-managing-resources.html) for all lifecycle management patterns.

---

## Execute a Command Inside a Pod

Run a shell command inside an already-running pod and capture the output.

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-nginx", namespace="default", ensure_exists=True)
output = pod.execute(command=["cat", "/etc/nginx/nginx.conf"], timeout=30)
print(output)
```

`execute()` streams output via the Kubernetes exec API. Use `container="sidecar"` to target a specific container in multi-container pods. Set `ignore_rc=True` to suppress errors from non-zero exit codes.

---

## Get Pod Logs

Retrieve logs from a running or completed pod.

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-nginx", namespace="default", ensure_exists=True)

# Full logs
print(pod.log())

# Last 50 lines
print(pod.log(tail_lines=50))

# Logs from a specific container
print(pod.log(container="sidecar"))
```

The `log()` method passes kwargs through to the Kubernetes `read_namespaced_pod_log` API, so all standard parameters like `tail_lines`, `since_seconds`, and `container` are supported.

---

## Create a Deployment and Wait for Replicas

Deploy an application with multiple replicas and wait until they are all ready.

```python
from ocp_resources.deployment import Deployment

dep = Deployment(
    client=client,
    name="web-app",
    namespace="default",
    replicas=3,
    selector={"matchLabels": {"app": "web-app"}},
    template={
        "metadata": {"labels": {"app": "web-app"}},
        "spec": {
            "containers": [{
                "name": "app",
                "image": "nginx:1.25",
                "ports": [{"containerPort": 80}],
            }]
        },
    },
)
dep.deploy()
dep.wait_for_replicas(deployed=True, timeout=300)
```

`wait_for_replicas` polls until `availableReplicas == readyReplicas == updatedReplicas == spec.replicas`. Pass `deployed=False` to wait for all replicas to be scaled down.

---

## Scale a Deployment

Change the replica count of an existing deployment.

```python
from ocp_resources.deployment import Deployment

dep = Deployment(client=client, name="web-app", namespace="default", ensure_exists=True)

# Scale up
dep.scale_replicas(replica_count=5)
dep.wait_for_replicas(deployed=True, timeout=300)

# Scale down
dep.scale_replicas(replica_count=1)
dep.wait_for_replicas(deployed=True, timeout=300)
```

`scale_replicas` patches the deployment's `spec.replicas` field. Always follow with `wait_for_replicas` to confirm the rollout completes.

---

## Create a Service

Expose a deployment via a ClusterIP service.

```python
from ocp_resources.service import Service

svc = Service(
    client=client,
    name="web-app-svc",
    namespace="default",
    selector={"app": "web-app"},
    ports=[{
        "protocol": "TCP",
        "port": 80,
        "targetPort": 80,
    }],
    type="ClusterIP",
)
svc.deploy()
```

Change `type` to `"NodePort"` or `"LoadBalancer"` as needed. The `selector` must match labels on your target pods.

---

## Create an OpenShift Route

Expose a service externally via an OpenShift Route.

```python
from ocp_resources.route import Route

route = Route(
    client=client,
    name="web-app-route",
    namespace="default",
    service="web-app-svc",
)
route.deploy()

# Get the assigned hostname
print(route.host)
```

For TLS re-encrypt routes, pass `destination_ca_cert="<PEM certificate string>"`. Access the exposed service name with `route.exposed_service` and the TLS termination type with `route.termination`.

---

## Create a Namespace

Create a namespace (or use as a context manager for automatic cleanup).

```python
from ocp_resources.namespace import Namespace

# Simple creation
ns = Namespace(client=client, name="test-ns")
ns.deploy()

# As a context manager (deleted on exit)
with Namespace(client=client, name="ephemeral-ns") as ns:
    # ... do work in the namespace ...
    pass
```

`Namespace` extends `Resource` (cluster-scoped), so no `namespace` parameter is needed.

---

## Create a ConfigMap

Store configuration data for pods to consume.

```python
from ocp_resources.config_map import ConfigMap

cm = ConfigMap(
    client=client,
    name="app-config",
    namespace="default",
    data={
        "DATABASE_URL": "postgres://db:5432/myapp",
        "LOG_LEVEL": "info",
    },
)
cm.deploy()
```

Use `binary_data` for non-UTF-8 content. Set `immutable=True` to prevent changes after creation.

---

## Create a Secret

Store sensitive data such as credentials.

```python
from ocp_resources.secret import Secret

secret = Secret(
    client=client,
    name="db-credentials",
    namespace="default",
    string_data={
        "username": "admin",
        "password": "s3cur3-pa$$word",
    },
    type="Opaque",
)
secret.deploy()
```

Use `data_dict` instead of `string_data` if your values are already base64-encoded. Secret data is automatically hashed in log output for security.

---

## Create a Job

Run a one-off task to completion.

```python
from ocp_resources.job import Job

job = Job(
    client=client,
    name="db-migration",
    namespace="default",
    backoff_limit=3,
    restart_policy="Never",
    containers=[{
        "name": "migrate",
        "image": "my-app:latest",
        "command": ["python", "manage.py", "migrate"],
    }],
)
job.deploy()
job.wait_for_condition(
    condition=Job.Condition.COMPLETE,
    status=Job.Condition.Status.TRUE,
    timeout=300,
)
```

Set `background_propagation_policy="Background"` to delete leftover pods when the job is cleaned up. The `backoff_limit` controls how many times the job retries on failure.

---

## Create a PersistentVolumeClaim

Request persistent storage for your workloads.

```python
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim

pvc = PersistentVolumeClaim(
    client=client,
    name="app-data",
    namespace="default",
    accessmodes=PersistentVolumeClaim.AccessMode.RWO,
    size="10Gi",
    storage_class="gp3-csi",
    volume_mode=PersistentVolumeClaim.VolumeMode.FILE,
)
pvc.deploy()
pvc.wait_for_status(status=PersistentVolumeClaim.Status.BOUND, timeout=120)
```

Use the `AccessMode` and `VolumeMode` constants instead of raw strings. The `storage_class` must match an available StorageClass on your cluster.

---

## Create a DataVolume (KubeVirt / CDI)

Import a VM disk image into a PVC using the Containerized Data Importer.

```python
from ocp_resources.datavolume import DataVolume

dv = DataVolume(
    client=client,
    name="fedora-disk",
    namespace="default",
    source_dict={"http": {"url": "https://download.fedoraproject.org/pub/fedora/linux/releases/40/Cloud/x86_64/images/Fedora-Cloud-Base-40-1.14.x86_64.qcow2"}},
    size="30Gi",
    storage_class="ocs-storagecluster-ceph-rbd-virtualization",
    access_modes=DataVolume.AccessMode.RWX,
    volume_mode=DataVolume.VolumeMode.BLOCK,
    api_name="storage",
)
dv.deploy()
dv.wait_for_dv_success(timeout=600)
```

Always pass `api_name="storage"` explicitly — the default will change in a future release. Use `source_dict={"blank": {}}` for empty disks, or `source_dict={"pvc": {"name": "source-pvc", "namespace": "default"}}` for cloning.

- **Clone a DataVolume:**
  ```python
  dv_clone = DataVolume(
      client=client,
      name="fedora-disk-clone",
      namespace="default",
      source_dict={"pvc": {"name": "fedora-disk", "namespace": "default"}},
      size="30Gi",
      storage_class="ocs-storagecluster-ceph-rbd-virtualization",
      access_modes=DataVolume.AccessMode.RWX,
      volume_mode=DataVolume.VolumeMode.BLOCK,
      api_name="storage",
  )
  ```

> **Tip:** See [Working with Virtual Machines (KubeVirt)](working-with-virtual-machines.html) for full VM lifecycle recipes.

---

## Create a NetworkPolicy

Restrict traffic to pods matching a label selector.

```python
from ocp_resources.network_policy import NetworkPolicy

netpol = NetworkPolicy(
    client=client,
    name="allow-http-only",
    namespace="default",
    pod_selector={"matchLabels": {"app": "web-app"}},
    policy_types=["Ingress"],
    ingress=[{
        "ports": [{"protocol": "TCP", "port": 80}],
        "from": [
            {"namespaceSelector": {"matchLabels": {"env": "production"}}},
        ],
    }],
)
netpol.deploy()
```

This allows TCP port 80 ingress only from namespaces labeled `env=production`. Omit `ingress` and set `policy_types=["Ingress"]` to deny all inbound traffic.

---

## Create a NetworkAttachmentDefinition

Attach pods to a secondary network using Multus.

```python
from ocp_resources.network_attachment_definition import LinuxBridgeNetworkAttachmentDefinition

nad = LinuxBridgeNetworkAttachmentDefinition(
    client=client,
    name="br-100",
    namespace="default",
    bridge_name="br-100",
    cni_type="cnv-bridge",
    vlan=100,
    mtu=1500,
)
nad.deploy()
```

Variant classes are available for different bridge types:
- `LinuxBridgeNetworkAttachmentDefinition` — Linux bridge (cnv-bridge)
- `OvsBridgeNetworkAttachmentDefinition` — OVS bridge
- `OVNOverlayNetworkAttachmentDefinition` — OVN overlay (layer 2/3)

---

## Create an RBAC Role and RoleBinding

Grant specific permissions to a service account within a namespace.

```python
from ocp_resources.role import Role
from ocp_resources.role_binding import RoleBinding
from ocp_resources.service_account import ServiceAccount

sa = ServiceAccount(
    client=client,
    name="app-sa",
    namespace="default",
)
sa.deploy()

role = Role(
    client=client,
    name="pod-reader",
    namespace="default",
    rules=[{
        "apiGroups": [""],
        "resources": ["pods", "pods/log"],
        "verbs": ["get", "list", "watch"],
    }],
)
role.deploy()

binding = RoleBinding(
    client=client,
    name="app-sa-pod-reader",
    namespace="default",
    subjects_kind="ServiceAccount",
    subjects_name="app-sa",
    subjects_namespace="default",
    role_ref_kind="Role",
    role_ref_name="pod-reader",
)
binding.deploy()
```

This grants the `app-sa` service account read-only access to pods in the `default` namespace.

---

## Create a ClusterRole and ClusterRoleBinding

Grant cluster-wide permissions to a service account.

```python
from ocp_resources.cluster_role import ClusterRole
from ocp_resources.cluster_role_binding import ClusterRoleBinding

cr = ClusterRole(
    client=client,
    name="node-viewer",
    rules=[{
        "apiGroups": [""],
        "resources": ["nodes"],
        "verbs": ["get", "list", "watch"],
    }],
)
cr.deploy()

crb = ClusterRoleBinding(
    client=client,
    name="app-sa-node-viewer",
    cluster_role="node-viewer",
    subjects=[{
        "kind": "ServiceAccount",
        "name": "app-sa",
        "namespace": "default",
    }],
)
crb.deploy()
```

`ClusterRole` and `ClusterRoleBinding` are cluster-scoped (`Resource` subclasses), so no `namespace` parameter is needed on the role or binding itself.

---

## List and Filter Resources

Query existing resources using label and field selectors.

```python
from ocp_resources.pod import Pod
from ocp_resources.namespace import Namespace

# List all pods in a namespace
for pod in Pod.get(client=client, namespace="default"):
    print(f"{pod.name} — {pod.status}")

# Filter by label
for pod in Pod.get(client=client, namespace="default", label_selector="app=web-app"):
    print(pod.name)

# Filter by field
for pod in Pod.get(client=client, namespace="default", field_selector="status.phase=Running"):
    print(pod.name)

# List cluster-scoped resources (no namespace)
for ns in Namespace.get(client=client, label_selector="env=staging"):
    print(ns.name)
```

The `get()` class method returns a generator of resource objects. Pass `raw=True` to get raw `ResourceInstance` objects instead.

> **Tip:** See [Querying and Watching Resources](querying-resources.html) for advanced querying patterns.

---

## Create a Resource from a YAML File

Load a resource definition from an existing YAML file.

```python
from ocp_resources.pod import Pod

pod = Pod(
    client=client,
    yaml_file="manifests/my-pod.yaml",
)
pod.deploy()
```

When using `yaml_file`, the `name` and `namespace` are read from the file automatically. You cannot combine `yaml_file` with `kind_dict`.

---

## Create a Resource from a Dictionary

Pass a raw Kubernetes resource dict directly.

```python
from ocp_resources.deployment import Deployment

dep = Deployment(
    client=client,
    kind_dict={
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "from-dict-app",
            "namespace": "default",
        },
        "spec": {
            "replicas": 2,
            "selector": {"matchLabels": {"app": "from-dict"}},
            "template": {
                "metadata": {"labels": {"app": "from-dict"}},
                "spec": {
                    "containers": [{
                        "name": "app",
                        "image": "nginx:1.25",
                    }],
                },
            },
        },
    },
)
dep.deploy()
```

Using `kind_dict` bypasses all constructor logic in `to_dict()` — the dictionary is sent as-is to the API. This is useful when migrating existing manifests.

---

## Handle Resources with Duplicate API Groups

Some Kubernetes resource kinds (e.g., `DNS`, `Ingress`, `Gateway`) exist in multiple API groups. The wrapper provides separate modules for each variant.

```python
# DNS from config.openshift.io (cluster DNS config)
from ocp_resources.dns_config_openshift_io import DNS as DNSConfig

dns_config = DNSConfig(client=client, name="cluster", ensure_exists=True)
print(dns_config.instance.spec.baseDomain)

# DNS from operator.openshift.io (CoreDNS operator)
from ocp_resources.dns_operator_openshift_io import DNS as DNSOperator

dns_operator = DNSOperator(client=client, name="default", ensure_exists=True)
print(dns_operator.instance.spec.logLevel)
```

```python
# Ingress from config.openshift.io (cluster ingress config)
from ocp_resources.ingress_config_openshift_io import Ingress as IngressConfig

ingress = IngressConfig(client=client, name="cluster", ensure_exists=True)
print(ingress.instance.spec.domain)

# Ingress from networking.k8s.io (K8s Ingress rules)
from ocp_resources.ingress_networking_k8s_io import Ingress as K8sIngress

k8s_ingress = K8sIngress(
    client=client,
    name="my-app-ingress",
    rules=[{
        "host": "app.example.com",
        "http": {
            "paths": [{
                "path": "/",
                "pathType": "Prefix",
                "backend": {"service": {"name": "web-app-svc", "port": {"number": 80}}},
            }],
        },
    }],
)
```

The naming convention for duplicate-kind modules is `<kind>_<api_group_snake_case>.py`. Use Python import aliases (`as`) to distinguish them in your code.

**Common duplicate kinds and their modules:**

| Kind | Module | API Group |
|------|--------|-----------|
| `DNS` | `dns_config_openshift_io` | `config.openshift.io` |
| `DNS` | `dns_operator_openshift_io` | `operator.openshift.io` |
| `Ingress` | `ingress_config_openshift_io` | `config.openshift.io` |
| `Ingress` | `ingress_networking_k8s_io` | `networking.k8s.io` |
| `Gateway` | `gateway` | `networking.istio.io` |
| `Gateway` | `gateway_gateway_networking_k8s_io` | `gateway.networking.k8s.io` |
| `Gateway` | `gateway_networking_istio_io` | `networking.istio.io` |

> **Warning:** Importing the wrong module will target the wrong API group, causing `NotFoundError` or unexpected behavior. Always verify the `api_group` attribute on your resource class.

---

## Manage Multiple Similar Resources with ResourceList

Create N copies of a resource with auto-numbered names.

```python
from ocp_resources.namespace import Namespace
from ocp_resources.resource import ResourceList

with ResourceList(
    resource_class=Namespace,
    num_resources=3,
    client=client,
    name="perf-test-ns",
) as namespaces:
    # Creates: perf-test-ns-1, perf-test-ns-2, perf-test-ns-3
    for ns in namespaces:
        print(ns.name)
# All 3 namespaces are deleted on exit
```

> **Tip:** See [Managing Bulk Resources with ResourceList](managing-resource-lists.html) for `NamespacedResourceList` and other bulk patterns.

---

## Deploy One Resource Per Namespace with NamespacedResourceList

Create an identical namespaced resource in each of several namespaces.

```python
from ocp_resources.namespace import Namespace
from ocp_resources.config_map import ConfigMap
from ocp_resources.resource import ResourceList, NamespacedResourceList

with ResourceList(
    resource_class=Namespace,
    num_resources=3,
    client=client,
    name="team-ns",
) as namespaces:
    with NamespacedResourceList(
        resource_class=ConfigMap,
        namespaces=namespaces,
        client=client,
        name="shared-config",
        data={"REGION": "us-east-1"},
    ) as configmaps:
        # One ConfigMap "shared-config" in each of team-ns-1, team-ns-2, team-ns-3
        for cm in configmaps:
            print(f"{cm.namespace}/{cm.name}")
```

`NamespacedResourceList` requires a `ResourceList` of `Namespace` objects. All resources are cleaned up in reverse order on exit.

---

## Temporarily Edit a Resource with ResourceEditor

Apply temporary patches during a test and automatically restore original values.

```python
from ocp_resources.resource import ResourceEditor
from ocp_resources.config_map import ConfigMap

cm = ConfigMap(client=client, name="app-config", namespace="default", ensure_exists=True)

with ResourceEditor(
    patches={cm: {"data": {"LOG_LEVEL": "debug"}}},
    action="update",
):
    # LOG_LEVEL is now "debug"
    print(cm.instance.data.LOG_LEVEL)
# Original LOG_LEVEL is restored here
```

`ResourceEditor` backs up original values on enter and restores them on exit. Use `action="replace"` when you need to remove fields entirely rather than patch them.

> **Tip:** See [Editing Resources Temporarily with ResourceEditor](editing-resources-temporarily.html) for complete details.

---

## Validate a Resource Before Creating It

Catch schema errors before submitting to the API server.

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ValidationError

pod = Pod(
    client=client,
    name="validated-pod",
    namespace="default",
    containers=[{
        "name": "app",
        "image": "nginx:1.25",
    }],
    schema_validation_enabled=True,  # Auto-validate on create()
)

# Manual validation
try:
    pod.validate()
    print("Resource is valid")
except ValidationError as e:
    print(f"Validation failed: {e}")

# Or validate a raw dict without instantiation
try:
    Pod.validate_dict({
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": "test"},
        "spec": {"containers": [{"name": "app", "image": "nginx"}]},
    })
except ValidationError as e:
    print(f"Dict validation failed: {e}")
```

When `schema_validation_enabled=True`, `create()` and `update_replace()` automatically validate before sending to the API. Validation requires OpenAPI schemas to be available.

> **Tip:** See [Validating Resources Against OpenAPI Schemas](validating-resources.html) for schema setup and troubleshooting.

---

## Check If a Resource Exists

Verify a resource exists before operating on it.

```python
from ocp_resources.deployment import Deployment

dep = Deployment(client=client, name="web-app", namespace="default")

if dep.exists:
    print(f"Deployment exists, status: {dep.instance.status.availableReplicas} replicas available")
else:
    print("Deployment not found")
```

`exists` returns the resource instance if found or `None` if not. For fail-fast behavior, use `ensure_exists=True` in the constructor — it raises `ResourceNotFoundError` immediately if the resource is missing.

---

## Watch Resource Events

Stream events related to a specific resource.

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-nginx", namespace="default", ensure_exists=True)

# Watch events for this pod (10 second window)
for event in pod.events(timeout=10):
    ev = event["object"]
    print(f"[{ev.type}] {ev.reason}: {ev.message}")
```

Use `field_selector` to narrow results further, for example: `field_selector="type==Warning"`. The `events()` method automatically filters by `involvedObject.name`.

---

## List Recent Events in a Namespace

Get existing events (not a watch stream) from the last N seconds.

```python
from ocp_resources.event import Event

# Warning events from the last 5 minutes
events = Event.list(
    client=client,
    namespace="default",
    field_selector="type==Warning",
    since_seconds=300,
)
for ev in events:
    print(f"[{ev.reason}] {ev.message}")
```

`Event.list()` returns a sorted list (most recent first), unlike `Event.get()` which is a live watch stream.

---

## Wait for a Resource Condition

Block until a resource reaches a specific condition.

```python
from ocp_resources.deployment import Deployment

dep = Deployment(client=client, name="web-app", namespace="default", ensure_exists=True)

dep.wait_for_condition(
    condition="Available",
    status="True",
    timeout=300,
)
```

Use `stop_condition` to fail fast if an unrecoverable condition is detected:

```python
dep.wait_for_condition(
    condition="Available",
    status="True",
    timeout=300,
    stop_condition="ReplicaFailure",
    stop_status="True",
)
```

> **Tip:** See [Waiting for Resource Conditions and Status](waiting-for-conditions.html) for advanced waiting patterns.

---

## Get a Resource's YAML Representation

Dump the intended resource dict as YAML (useful for debugging).

```python
from ocp_resources.pod import Pod

pod = Pod(
    client=client,
    name="debug-pod",
    namespace="default",
    containers=[{"name": "app", "image": "busybox", "command": ["sleep", "3600"]}],
)
print(pod.to_yaml())
```

`to_yaml()` calls `to_dict()` internally and returns the YAML string. This shows what would be sent to the API, not the live state.

---

## Get the Pod's Node and IP

Access commonly needed runtime properties of a pod.

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-nginx", namespace="default", ensure_exists=True)

# Node where the pod is running
print(f"Node: {pod.node.name}")

# Pod IP address
print(f"IP: {pod.ip}")
```

The `node` property returns a `Node` resource object. The `ip` property reads from `status.podIP`.

## Related Pages

- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Querying and Watching Resources](querying-resources.html)
- [Working with Virtual Machines (KubeVirt)](working-with-virtual-machines.html)
- [Executing Commands in Pods and Retrieving Logs](pod-execution-and-logs.html)
- [Working with Kubernetes Events](working-with-events.html)
