Let me start by reading the exclusions file and pages manifest, then explore the codebase.

Now let me look at how the Resource base class integrates validation:

Now let me check the exceptions module:

Now let me check how `deploy` and context managers interact with validation:

Now I have a comprehensive understanding of the validation feature. Let me write the documentation.

# Validating Resources Against OpenAPI Schemas

Catch configuration mistakes before they reach the Kubernetes API by validating resource definitions against OpenAPI schemas. This saves debugging time and prevents failed deployments caused by typos, missing fields, or incorrect types.

## Prerequisites

- openshift-python-wrapper installed (see [Installing and Creating Your First Resource](quickstart.html))
- A connection to a cluster, or use the fake client for offline validation (see [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html))

## Quick Example

```python
from ocp_resources.pod import Pod

pod = Pod(
    name="nginx-pod",
    namespace="default",
    containers=[{"name": "nginx", "image": "nginx:latest"}],
)

# Validate against the OpenAPI schema — raises ValidationError if invalid
pod.validate()
```

If the resource is valid, `validate()` returns silently. If something is wrong, it raises a `ValidationError` with a clear message pointing to the problematic field.

## Manual Validation

Call `.validate()` on any resource instance to check it against the OpenAPI schema for its kind:

```python
from ocp_resources.exceptions import ValidationError
from ocp_resources.service import Service

service = Service(
    name="nginx-service",
    namespace="default",
    selector={"app": "nginx"},
    ports=[{"port": 80, "targetPort": 80, "protocol": "TCP"}],
)

try:
    service.validate()
    print("Service configuration is valid")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

> **Tip:** Use manual validation in CI pipelines or pre-commit hooks to catch errors before applying resources to a cluster.

## Validating Dictionaries Without Creating Objects

Use the `validate_dict()` class method to validate a raw resource dictionary without instantiating a resource object:

```python
from ocp_resources.deployment import Deployment
from ocp_resources.exceptions import ValidationError

deployment_dict = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "nginx-deployment", "namespace": "default"},
    "spec": {
        "replicas": 3,
        "selector": {"matchLabels": {"app": "nginx"}},
        "template": {
            "metadata": {"labels": {"app": "nginx"}},
            "spec": {
                "containers": [
                    {"name": "nginx", "image": "nginx:1.21", "ports": [{"containerPort": 80}]}
                ],
            },
        },
    },
}

try:
    Deployment.validate_dict(resource_dict=deployment_dict)
    print("Deployment configuration is valid")
except ValidationError as e:
    print(f"Invalid: {e}")
```

This is useful when you have a dictionary from a YAML file or external source and want to validate it before creating the resource.

## Enabling Auto-Validation on Create

Set `schema_validation_enabled=True` when creating a resource instance to automatically validate before every `create()`, `deploy()`, or `update_replace()` call:

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ValidationError

pod = Pod(
    client=client,
    name="auto-validated-pod",
    namespace="default",
    containers=[{"name": "nginx", "image": "nginx:latest"}],
    schema_validation_enabled=True,
)

# Validation runs automatically before the resource is sent to the API
pod.deploy()
```

If validation fails, the resource is **not** created and a `ValidationError` is raised:

```python
invalid_pod = Pod(
    client=client,
    name="bad-pod",
    namespace="default",
    containers=[{"name": "nginx"}],  # Missing required 'image' field
    schema_validation_enabled=True,
)

try:
    invalid_pod.deploy()
except ValidationError as e:
    print(f"Blocked: {e}")
```

> **Note:** Auto-validation is **disabled by default** (`schema_validation_enabled=False`). You must opt in per instance.

### When Auto-Validation Runs

| Operation          | Auto-validates? | Notes                                      |
|--------------------|-----------------|---------------------------------------------|
| `create()` / `deploy()` | ✅ Yes          | Validates the full resource before sending |
| `update_replace()`      | ✅ Yes          | Validates the replacement dictionary       |
| `update()`              | ❌ No           | Sends a partial patch, not a full resource |

Auto-validation also applies when using context managers, since they call `deploy()` internally. See [Creating and Managing Resources](creating-and-managing-resources.html) for details on resource lifecycle methods.

### Toggling Validation at Runtime

You can enable or disable validation on an existing instance:

```python
pod = Pod(
    client=client,
    name="my-pod",
    namespace="default",
    containers=[{"name": "nginx", "image": "nginx:latest"}],
)

# Enable after creation
pod.schema_validation_enabled = True
pod.deploy()  # Will validate first

# Disable for a subsequent operation
pod.schema_validation_enabled = False
```

## Advanced Usage

### Validating Resources with Duplicate API Groups

Some resource kinds (like `DNS`) exist in multiple API groups. The validator uses the resource's `api_group` to select the correct schema automatically:

```python
# These two resources share the kind "DNS" but use different API groups.
# Each is validated against its own schema.
dns_config.validate()       # Uses config.openshift.io schema
dns_operator.validate()     # Uses operator.openshift.io schema
```

See [Common Resource Patterns](common-patterns.html) for more on working with resources that share a kind name.

### Pre-Warming the Schema Cache

The first validation for a resource kind loads and resolves the schema (~25ms). Subsequent validations for the same kind use a cache and are much faster (~2ms). Pre-warm the cache at application startup for critical resource types:

```python
from ocp_resources.pod import Pod
from ocp_resources.deployment import Deployment
from ocp_resources.service import Service
from ocp_resources.exceptions import ValidationError

for resource_cls in [Pod, Deployment, Service]:
    try:
        resource_cls.validate_dict({
            "apiVersion": "v1",
            "kind": resource_cls.kind,
            "metadata": {"name": "warmup"}
        })
    except ValidationError:
        pass  # Expected — we just want to load the schemas
```

### Disabling Validation for Bulk Operations

When creating many resources in a loop, disable auto-validation to avoid repeated checks if you've already validated your templates:

```python
# Validate the template once
Pod.validate_dict(resource_dict=pod_template)

# Then create many instances without per-instance validation
for i in range(100):
    pod = Pod(
        client=client,
        name=f"worker-{i}",
        namespace="default",
        containers=[{"name": "app", "image": "myapp:latest"}],
        schema_validation_enabled=False,  # Skip — already validated
    )
    pod.deploy()
```

## Troubleshooting

### Reading Validation Error Messages

Validation errors include three key pieces of information:

```
Resource validation failed for Pod/my-pod
  Field: spec.containers[0].image
  Error: 123 is not of type 'string'
  Expected type: string
```

- **Resource identifier** — which resource failed (kind and name)
- **Field path** — the JSON path to the problematic field
- **Error details** — what went wrong and what was expected

### Common Validation Error Patterns

| Error message pattern                        | Cause                              | Fix                                              |
|----------------------------------------------|-------------------------------------|--------------------------------------------------|
| `'X' is a required property`                 | Missing a required field           | Add the missing field to your resource definition |
| `'X' is not of type 'Y'`                     | Wrong data type                    | Use the correct type (e.g., `3` not `"3"`)       |
| `'X' does not match pattern`                 | Invalid format                     | Follow Kubernetes naming rules (lowercase, alphanumeric, hyphens) |
| `'X' is not one of [...]`                    | Invalid enum value                 | Use one of the allowed values listed in the error |
| `Additional properties are not allowed`       | Unknown field name                 | Check for typos in field names                   |

### Validation Passes But API Rejects the Resource

OpenAPI schema validation catches structural issues (wrong types, missing fields, invalid formats) but cannot check everything the API server validates. For example:

- Unique name constraints within a namespace
- Resource quota limits
- Admission webhook rules
- Cross-resource references (e.g., a ConfigMap that doesn't exist)

If validation passes but the API still rejects your resource, the issue is likely a server-side constraint.

### No Schema Available for a Resource

If no schema is bundled for a resource kind, `validate()` silently succeeds instead of raising an error. A debug-level log message is emitted:

```
No schema found for MyCustomResource, skipping validation
```

To update bundled schemas, see [class-generator CLI Reference](class-generator-cli.html).

## Related Pages

- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Schema Validation and Code Generation Architecture](schema-validation-internals.html)
- [Error Handling and Exception Reference](error-handling.html)
- [class-generator CLI Reference](class-generator-cli.html)
- [Resource and NamespacedResource API](resource-api.html)
