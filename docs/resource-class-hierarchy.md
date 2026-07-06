Let me start by reading the exclusions file and pages manifest, then explore the codebase thoroughly.

Now let me look at some generated resource subclasses to understand how they extend the base classes:

Now let me look at some more examples - a cluster-scoped resource, the `ResourceConstants`, the class generator, and the `virtual_machine.py` for a more complex subclass:

Now let me look at the `kind` property and how it's derived, plus some other resources for variety:

Now let me look at how the `kind` property works (the `sub_resource_level` function) and the `conversion.py` for the kind name derivation:

Now let me look at how resources discover their API version dynamically:

Let me now look at one more important aspect - how the `get` method works differently in the two base classes, and how `_base_body` differs:

Now let me check the `__init__.py` to see what's exported:

Let me also check for examples:

Now I have enough context to write the documentation. Let me draft it:

# Understanding the Resource Class Hierarchy

Every Kubernetes and OpenShift object you interact with through openshift-python-wrapper — whether it's a Pod, a Namespace, or a VirtualMachine — is a Python class that inherits from a small set of base classes. Understanding how these classes relate to each other helps you know **what capabilities any resource has**, **why some resources require a `namespace` argument and others don't**, and **how new resource types get added to the library**.

This page explains the architecture so you can use existing resources effectively and extend the library when you need to work with a new custom resource.

---

## The Big Picture

The class hierarchy has three conceptual layers:

| Layer | Classes | Purpose |
|---|---|---|
| **Constants** | `ResourceConstants` | Provides shared status strings, condition names, and type constants used across all resources |
| **Base classes** | `Resource`, `NamespacedResource` | Define all CRUD operations, lifecycle management, waiting, validation, and API discovery logic |
| **Concrete resource classes** | `Pod`, `Namespace`, `Deployment`, `VirtualMachine`, and 200+ others | Represent specific Kubernetes/OpenShift resource kinds, adding kind-specific parameters and behavior |

The inheritance flows like this:

```
ResourceConstants
  └── Resource                  ← cluster-scoped resources (Node, Namespace, StorageClass, ClusterRole, …)
        └── NamespacedResource  ← namespace-scoped resources (Pod, Deployment, ConfigMap, Secret, Route, …)
```

Every concrete resource class inherits from either `Resource` (for cluster-scoped resources) or `NamespacedResource` (for namespace-scoped resources). This single design decision controls whether the class requires a `namespace` argument and how it builds API requests.

---

## Key Concepts

### ResourceConstants: Shared Vocabulary

At the root of the hierarchy sits `ResourceConstants`, which defines inner classes for common values:

- **`Status`** — Strings like `RUNNING`, `SUCCEEDED`, `FAILED`, `PENDING`, `ACTIVE`
- **`Condition`** — Condition types like `READY`, `AVAILABLE`, `DEGRADED` and their status values (`TRUE`, `FALSE`, `UNKNOWN`)
- **`Type`** — Service types like `ClusterIP`, `NodePort`, `LoadBalancer`

Because `Resource` inherits from `ResourceConstants`, every resource class in the library can reference these constants:

```python
from ocp_resources.namespace import Namespace

ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=120)
```

Concrete classes can extend these constants with kind-specific values. For example, `VirtualMachine` adds statuses like `MIGRATING`, `STOPPED`, and `PROVISIONING` to the base `Status` class.

### Resource: The Foundation for Cluster-Scoped Resources

`Resource` is the main base class. It provides everything needed to manage a Kubernetes resource:

| Capability | Methods / Properties |
|---|---|
| **CRUD operations** | `create()`, `delete()`, `update()`, `update_replace()` |
| **Lifecycle management** | `deploy()`, `clean_up()`, context manager (`with` statement) |
| **Querying** | `exists`, `instance`, `status`, `labels` |
| **Waiting** | `wait()`, `wait_deleted()`, `wait_for_status()`, `wait_for_condition()` |
| **Listing** | `get()` class method — yields resource objects matching filters |
| **Validation** | `validate()`, `validate_dict()` |
| **Serialization** | `to_dict()`, `to_yaml()` |
| **API discovery** | Automatic `api_version` resolution from the cluster when only `api_group` is set |

Resources that exist at the cluster level — not inside any namespace — inherit directly from `Resource`. Examples include `Namespace`, `Node`, `StorageClass`, `ClusterRole`, and `CustomResourceDefinition`.

```python
from ocp_resources.namespace import Namespace

# No namespace argument needed — Namespace is cluster-scoped
ns = Namespace(client=client, name="my-namespace")
```

#### Automatic Kind Detection

You never set the `kind` field manually. The `kind` property is a class-level property that automatically derives the Kubernetes kind name from the **class name** using Python's method resolution order (MRO). When you define a class named `StorageClass`, its `kind` is automatically `"StorageClass"`.

#### API Version Discovery

Resources can specify their API identity in two ways:

1. **`api_version`** — A fixed version string (e.g., `"v1"`), used for core Kubernetes resources
2. **`api_group`** — An API group string (e.g., `"apps"`, `"kubevirt.io"`), where the full `apiVersion` is discovered dynamically from the cluster

When only `api_group` is set, the library queries the cluster at runtime to find the latest supported version for that resource kind. This means resource classes automatically work across cluster versions without code changes.

```python
class Namespace(Resource):
    # Core resource — fixed version, no group
    api_version: str = Resource.ApiVersion.V1

class ClusterRole(Resource):
    # Grouped resource — version discovered from cluster
    api_group = Resource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO
```

> **Note:** The `Resource.ApiGroup` and `Resource.ApiVersion` inner classes provide predefined constants for all known API groups and versions. Using these constants avoids typos and makes your code self-documenting.

### NamespacedResource: Adding Namespace Awareness

`NamespacedResource` extends `Resource` with one critical addition: **namespace handling**. It requires a `namespace` argument during construction and injects the namespace into all API calls.

The differences from `Resource` are focused but important:

| Behavior | `Resource` | `NamespacedResource` |
|---|---|---|
| `namespace` required? | No | Yes (unless using `yaml_file` or `kind_dict`) |
| `to_dict()` output | No namespace in metadata | Adds `metadata.namespace` |
| `get()` yields | Objects with `name` only | Objects with both `name` and `namespace` |
| `instance` property | Fetches by name only | Fetches by name and namespace |

```python
from ocp_resources.pod import Pod

# Namespace is required for namespaced resources
pod = Pod(client=client, name="my-pod", namespace="default",
          containers=[{"name": "app", "image": "nginx"}])
```

### Concrete Resource Classes: Where Specifics Live

Concrete classes add three things on top of the base classes:

1. **API identity** — Setting `api_group` or `api_version` to identify which Kubernetes API to call
2. **Constructor parameters** — Typed arguments for the resource's spec fields (like `containers` for Pod, `replicas` for Deployment)
3. **Custom `to_dict()` method** — Builds the Kubernetes resource dictionary from constructor arguments

Here is how a typical generated class is structured:

```python
class Deployment(NamespacedResource):
    # 1. API identity
    api_group: str = NamespacedResource.ApiGroup.APPS

    def __init__(self, replicas=None, selector=None, template=None, **kwargs):
        # 2. Pass common args to base class, store kind-specific args
        super().__init__(**kwargs)
        self.replicas = replicas
        self.selector = selector
        self.template = template

    def to_dict(self):
        # 3. Build the resource dictionary
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]
            _spec["selector"] = self.selector
            _spec["template"] = self.template
            if self.replicas is not None:
                _spec["replicas"] = self.replicas
```

> **Tip:** You can always bypass the typed constructor entirely by passing `yaml_file` or `kind_dict` to any resource class. When you do, the `to_dict()` logic is skipped and the resource is created from your raw definition instead.

#### Adding Kind-Specific Behavior

Many concrete classes go beyond what the generator produces by adding custom methods and properties. For example:

- **Pod** adds `execute()` for running commands, `log()` for reading logs, and a `node` property
- **Deployment** adds `scale_replicas()` and `wait_for_replicas()`
- **Secret** overrides `keys_to_hash` to ensure sensitive data is masked in logs

These additions are preserved across regeneration because the class generator recognizes the `# End of generated code` marker and keeps any code written below it.

### How Generated Classes Are Created

Most concrete resource classes in the library are **code-generated** from the cluster's OpenAPI schema using the `class-generator` tool. The generator:

1. Reads the resource definition from the cluster's OpenAPI schema
2. Determines whether the resource is namespaced (→ `NamespacedResource`) or cluster-scoped (→ `Resource`)
3. Extracts spec fields with their types and descriptions
4. Renders a Python class from a Jinja2 template
5. Preserves any hand-written code below the `# End of generated code` marker

This means the hierarchy is not just an architectural choice — it is **enforced by the code generation pipeline**. Every generated class correctly inherits from the appropriate base class based on the resource's actual scope in Kubernetes.

See [Generating New Resource Classes with class-generator](generating-resource-classes.html) for details on generating classes for new resource types.

---

## How It Affects You

Understanding the hierarchy helps you in several practical ways:

### Knowing What Methods Are Available

Every resource — regardless of kind — inherits the full set of CRUD, waiting, and lifecycle methods from `Resource`. You don't need to check whether a particular resource supports `wait_for_condition()` or context managers; they all do.

```python
# Works for any resource type
with SomeResource(client=client, name="example", **specific_args) as res:
    res.wait_for_condition(condition="Ready", status="True")
```

See [Resource and NamespacedResource API](resource-api.html) for the complete method reference.

### Understanding Constructor Requirements

The base class determines what arguments are mandatory:

| If you're using... | Required arguments |
|---|---|
| `Resource` subclass | `client`, `name` |
| `NamespacedResource` subclass | `client`, `name`, `namespace` |
| Any class with `yaml_file` | `client`, `yaml_file` |
| Any class with `kind_dict` | `client`, `kind_dict` |

See [Creating and Managing Resources](creating-and-managing-resources.html) for full examples of all creation methods.

### Using Status and Condition Constants

The `Status` and `Condition` constants inherited from `ResourceConstants` are available on every resource class. Concrete classes may extend them:

```python
from ocp_resources.virtual_machine import VirtualMachine

# Base constants work on all resources
vm.wait_for_status(status=VirtualMachine.Status.RUNNING)

# Kind-specific constants are added by the concrete class
vm.wait_for_status(status=VirtualMachine.Status.STOPPED)
```

### Extending the Library

If you need to work with a CRD that isn't included in the library, you have two options:

1. **Use the class generator** to scaffold a new class automatically — see [Generating New Resource Classes with class-generator](generating-resource-classes.html)
2. **Write a class manually** by inheriting from `Resource` or `NamespacedResource` and setting `api_group` or `api_version`

A minimal hand-written resource class looks like this:

```python
from ocp_resources.resource import NamespacedResource

class MyCustomResource(NamespacedResource):
    api_group = "example.com"
    # That's it — you get full CRUD, waiting, and lifecycle support
```

> **Warning:** Your class name must match the Kubernetes `kind` exactly (in PascalCase). The `kind` property is derived from the class name automatically — a class named `MyCustomResource` will have `kind = "MyCustomResource"`.

---

## Related Pages

- [Resource and NamespacedResource API](resource-api.html) — Complete method and property reference for the base classes
- [Creating and Managing Resources](creating-and-managing-resources.html) — Practical guide to creating, updating, and deleting resources
- [Generating New Resource Classes with class-generator](generating-resource-classes.html) — Generate Python classes for any CRD
- [Querying and Watching Resources](querying-resources.html) — Use the `get()` class method and watchers to list and observe resources
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html) — Use the waiting methods inherited from the base classes
- [Validating Resources Against OpenAPI Schemas](validating-resources.html) — Validate resources using the built-in schema validation
- [Environment Variables and Configuration](environment-variables.html) — Configure logging, resource reuse, and teardown behavior

## Related Pages

- [Resource and NamespacedResource API](resource-api.html)
- [Generating New Resource Classes with class-generator](generating-resource-classes.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Schema Validation and Code Generation Architecture](schema-validation-internals.html)
- [Validating Resources Against OpenAPI Schemas](validating-resources.html)
