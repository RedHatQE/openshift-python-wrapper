Let me explore the repository structure and find all relevant exception definitions and usages.

Now let me look at the `ConditionError` usage more closely and the `MissingTemplateVariables` and `MissingResourceError` exceptions:

Now let me look at how the deploy method uses ValidationError:

Now let me see where `validate` is called during `create`:

Now let me look at the `Pod.execute` method more closely:

Now let me look at how `client_with_basic_auth` works:

Now let me see the NNCP methods in full context:

Let me also look at `MissingTemplateVariables` usage more closely:

Now let me check the `__init__` of Resource to see how `schema_validation_enabled` is handled:

Now let me also check the `wait_for_condition` method signature more closely:

Let me also look at `MissingResourceResError` usage:

Now let me check the test for `ResourceTeardownError`:

Let me see how SecretTestExit is defined:

Let me check the import path for all exceptions:

Now I have a thorough understanding of the codebase. Let me write the reference documentation.

# Error Handling and Exception Reference

All custom exceptions are defined in `ocp_resources.exceptions` and can be imported directly:

```python
from ocp_resources.exceptions import (
    ExecOnPodError,
    MissingRequiredArgumentError,
    ResourceTeardownError,
    ValidationError,
    ConditionError,
    NNCPConfigurationFailed,
    ClientWithBasicAuthError,
    MissingResourceError,
    MissingTemplateVariables,
)
```

> **Tip:** All exceptions inherit from Python's built-in `Exception` class and can be caught with a bare `except Exception` if needed.

---

## ExecOnPodError

Raised when a command executed inside a pod via `Pod.execute()` fails. See [Executing Commands in Pods and Retrieving Logs](pod-execution-and-logs.html) for full usage details.

**Import:**

```python
from ocp_resources.exceptions import ExecOnPodError
```

**Constructor Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | `list[str]` | The command that was executed |
| `rc` | `int` | Return code (`-1` if the return code could not be determined) |
| `out` | `str` | Standard output captured from the command |
| `err` | `Any` | Standard error output or error channel details |

**Attributes on the caught exception:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `cmd` | `list[str]` | The command that was executed |
| `rc` | `int` | The return code |
| `out` | `str` | Standard output |
| `err` | `Any` | Standard error or error channel dict |

**Raised by:** `Pod.execute()` in the following scenarios:

- Command times out (stream response closes before completion) — `rc=-1`
- Error channel returns no status — `rc=-1`
- Error channel status is `"Failure"` — `rc=-1`, `err` contains the full error channel dict
- Command exits with a non-zero exit code — `rc` contains the actual exit code

**String representation:**

```
Command execution failure: ['ls', '/nonexistent'], RC: 2, OUT: , ERR: ls: cannot access '/nonexistent'
```

**Example:**

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ExecOnPodError

pod = Pod(client=client, name="my-pod", namespace="default")

try:
    output = pod.execute(command=["ls", "/nonexistent"], timeout=30)
except ExecOnPodError as e:
    print(f"Command: {e.cmd}")
    print(f"Return code: {e.rc}")
    print(f"Stdout: {e.out}")
    print(f"Stderr: {e.err}")
```

**Handling non-zero exit codes without exceptions:**

```python
# Use ignore_rc=True to suppress ExecOnPodError on non-zero exit codes
output = pod.execute(command=["grep", "pattern", "/var/log/messages"], ignore_rc=True)
```

---

## MissingRequiredArgumentError

Raised when a resource is instantiated without providing required arguments and no `yaml_file` or `kind_dict` was supplied. This error is raised during `to_dict()`, which is called automatically by `create()` and `deploy()`.

**Import:**

```python
from ocp_resources.exceptions import MissingRequiredArgumentError
```

**Constructor Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `argument` | `str` | Name of the missing required argument(s) |

**Attributes on the caught exception:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `argument` | `str` | The missing argument name |

**String representation:**

```
Missing required argument/s. Either provide yaml_file, kind_dict or pass self.containers
```

**Raised by:** The `to_dict()` method of resource subclasses when required spec fields are not provided. Examples of resources that raise this exception:

| Resource Class | Required Arguments |
|---|---|
| `Pod` | `containers` |
| `StorageClass` | `provisioner` |
| `ClusterRoleBinding` | `cluster_role` |
| `ClusterResourceQuota` | `quota`, `selector` |
| `CronJob` | `job_template`, `schedule` |
| `InferenceService` | `predictor` |
| `IPAddressPool` | `addresses` |
| `ResourceQuota` | `hard` |
| `UserDefinedNetwork` | `topology` |

> **Note:** This exception is **not** raised if you construct the resource using `yaml_file` or `kind_dict`, since those bypass the `to_dict()` logic.

**Example:**

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import MissingRequiredArgumentError

try:
    pod = Pod(client=client, name="my-pod", namespace="default")
    pod.deploy()
except MissingRequiredArgumentError as e:
    print(f"Missing: {e.argument}")
    # Output: Missing required argument/s. Either provide yaml_file, kind_dict or pass self.containers
```

---

## ResourceTeardownError

Raised when a resource's `clean_up()` method returns `False` during context manager exit. This indicates the resource could not be deleted.

**Import:**

```python
from ocp_resources.exceptions import ResourceTeardownError
```

**Constructor Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `resource` | `Any` | The resource object that failed to tear down |

**Attributes on the caught exception:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `resource` | `Any` | The resource object that failed teardown |

**String representation:**

```
Failed to execute teardown for resource <resource>
```

**Raised by:** `Resource.__exit__()` — the context manager exit handler. Specifically, this is raised when:

1. The resource was created with `teardown=True` (the default).
2. The `clean_up()` method returns `False`.

**Example:**

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ResourceTeardownError

try:
    with Pod(
        client=client,
        name="my-pod",
        namespace="default",
        containers=[{"name": "nginx", "image": "nginx:latest"}],
    ) as pod:
        # Use pod...
        pass
    # clean_up() is called automatically here
except ResourceTeardownError as e:
    print(f"Could not delete: {e.resource}")
```

> **Tip:** Set `teardown=False` on the resource constructor if you do not want automatic cleanup on context manager exit, and thus never want this exception raised.

---

## ValidationError

Raised when a resource fails schema validation against the OpenAPI specification. See [Validating Resources Against OpenAPI Schemas](validating-resources.html) for full validation guide.

**Import:**

```python
from ocp_resources.exceptions import ValidationError
```

**Constructor Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | `str` | *(required)* | Human-readable error description |
| `path` | `str` | `""` | JSONPath to the invalid field (e.g., `"spec.containers[0].image"`) |
| `schema_error` | `Any` | `None` | Original `jsonschema` validation error for debugging |

**Attributes on the caught exception:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `message` | `str` | Human-readable error message |
| `path` | `str` | JSONPath to the invalid field |
| `schema_error` | `Any` | Original `jsonschema.ValidationError` if available |

**String representation:**

```
Validation error at 'spec.containers[0].image': Invalid type
```

When `path` is empty:

```
Validation error: Field is required
```

**Raised by:**

| Method | Trigger |
|--------|---------|
| `resource.validate()` | Called explicitly by user |
| `resource.create()` | When `schema_validation_enabled=True` |
| `resource.update_replace()` | When `schema_validation_enabled=True` |
| `Resource.validate_dict()` | Class method for validating raw dicts |

> **Note:** `resource.update()` does **not** trigger validation even when `schema_validation_enabled=True`, because updates send partial patches that would fail full schema validation.

**Example — explicit validation:**

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ValidationError

pod = Pod(client=client, name="my-pod", namespace="default",
          containers=[{"name": "nginx", "image": "nginx:latest"}])

try:
    pod.validate()
except ValidationError as e:
    print(f"Error: {e.message}")
    print(f"Path: {e.path}")
    if e.schema_error:
        print(f"Original error: {e.schema_error}")
```

**Example — auto-validation on create:**

```python
from ocp_resources.pod import Pod
from ocp_resources.exceptions import ValidationError

try:
    pod = Pod(
        client=client,
        name="my-pod",
        namespace="default",
        containers=[{"name": "nginx", "image": "nginx:latest"}],
        schema_validation_enabled=True,
    )
    pod.deploy()
except ValidationError as e:
    print(f"Invalid resource: {e}")
```

**Example — validate a raw dictionary:**

```python
from ocp_resources.deployment import Deployment
from ocp_resources.exceptions import ValidationError

deployment_dict = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "my-deploy"},
    "spec": {"replicas": "three"},  # Wrong type — should be int
}

try:
    Deployment.validate_dict(resource_dict=deployment_dict)
except ValidationError as e:
    print(f"Validation failed: {e}")
```

---

## ConditionError

Raised when a resource reaches an undesired stop condition during `wait_for_condition()`. See [Waiting for Resource Conditions and Status](waiting-for-conditions.html) for details.

**Import:**

```python
from ocp_resources.exceptions import ConditionError
```

**Constructor Parameters:** Standard `Exception` — accepts a single string message.

**Raised by:** `Resource.wait_for_condition()` when the `stop_condition` parameter matches before the desired condition is met.

**`wait_for_condition()` parameters relevant to `ConditionError`:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `condition` | `str` | *(required)* | Condition type to wait for |
| `status` | `str` | *(required)* | Expected status value |
| `timeout` | `int` | `300` | Maximum wait time in seconds |
| `sleep_time` | `int` | `1` | Polling interval in seconds |
| `stop_condition` | `str \| None` | `None` | Condition type that should abort the wait |
| `stop_status` | `str` | `"True"` | Status value for the stop condition |

**String representation:**

```
Deployment my-deploy reached stop_condition 'Failed' in status 'True':
{'type': 'Failed', 'status': 'True', 'reason': 'DeadlineExceeded', 'message': '...'}
```

> **Note:** When `stop_condition` is `None` (the default), `ConditionError` is never raised. Instead, `TimeoutExpiredError` is raised if the desired condition is not met within the timeout.

**Example:**

```python
from ocp_resources.deployment import Deployment
from ocp_resources.exceptions import ConditionError
from timeout_sampler import TimeoutExpiredError

deploy = Deployment(client=client, name="my-deploy", namespace="default")

try:
    deploy.wait_for_condition(
        condition="Available",
        status="True",
        timeout=120,
        stop_condition="Failed",
        stop_status="True",
    )
except ConditionError as e:
    print(f"Resource entered failure state: {e}")
except TimeoutExpiredError:
    print("Timed out waiting for condition")
```

---

## NNCPConfigurationFailed

Raised when a `NodeNetworkConfigurationPolicy` (NNCP) fails to configure on one or more nodes.

**Import:**

```python
from ocp_resources.exceptions import NNCPConfigurationFailed
```

**Constructor Parameters:** Standard `Exception` — accepts a single string message describing the failure reason and error details.

**Raised by:** `NodeNetworkConfigurationPolicy.wait_for_status_success()` in two scenarios:

| Scenario | Message Pattern |
|----------|-----------------|
| No matching node found | `"{name}. Reason: NoMatchingNode"` |
| Configuration failed on nodes | `"Reason: FailedToConfigure\n{error_details}"` |

> **Note:** When `wait_for_status_success()` catches `TimeoutExpiredError` or `NNCPConfigurationFailed`, it logs the error with node details and re-raises the exception.

**Example:**

```python
from ocp_resources.node_network_configuration_policy import NodeNetworkConfigurationPolicy
from ocp_resources.exceptions import NNCPConfigurationFailed
from timeout_sampler import TimeoutExpiredError

nncp = NodeNetworkConfigurationPolicy(
    client=client,
    name="my-nncp",
    desired_state={"interfaces": [{"name": "eth1", "type": "ethernet", "state": "up"}]},
)

try:
    nncp.deploy()
    nncp.wait_for_status_success()
except NNCPConfigurationFailed as e:
    print(f"NNCP configuration failed: {e}")
except TimeoutExpiredError:
    print("NNCP configuration timed out")
```

---

## ClientWithBasicAuthError

Raised during OAuth-based client authentication when using username/password credentials to connect to an OpenShift cluster. See [Connecting to Clusters](connecting-to-clusters.html) for connection methods.

**Import:**

```python
from ocp_resources.exceptions import ClientWithBasicAuthError
```

**Constructor Parameters:** Standard `Exception` — accepts a single string message.

**Raised by:** `client_configuration_with_basic_auth()` in the following scenarios:

| Scenario | Message |
|----------|---------|
| OAuth well-known endpoint not reachable | `"No well-known file found at endpoint"` |
| Authorization code not returned after login | `"No authorization code found"` |
| No `authorization_endpoint` in OAuth config | `"No authorization_endpoint found in well-known file"` |
| Token exchange fails | `"Failed to authenticate with basic auth"` |

**Example:**

```python
from ocp_resources.exceptions import ClientWithBasicAuthError
from ocp_resources.resource import client_configuration_with_basic_auth

import kubernetes

configuration = kubernetes.client.Configuration()
configuration.verify_ssl = False

try:
    api_client = client_configuration_with_basic_auth(
        username="admin",
        password="password",
        host="https://api.cluster.example.com:6443",
        configuration=configuration,
    )
except ClientWithBasicAuthError as e:
    print(f"Authentication failed: {e}")
```

---

## MissingResourceError

Raised when a resource object fails to generate its internal representation.

**Import:**

```python
from ocp_resources.exceptions import MissingResourceError
```

**Constructor Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Name of the resource that could not be generated |

**Attributes on the caught exception:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `resource_name` | `str` | The resource name |

**String representation:**

```
Failed to generate resource: my-resource
```

**Example:**

```python
from ocp_resources.exceptions import MissingResourceError

try:
    # Operations that may fail to generate a resource
    ...
except MissingResourceError as e:
    print(f"Resource generation failed: {e.resource_name}")
```

---

## MissingTemplateVariables

Raised when rendering a YAML template and not all required template variables have been provided.

**Import:**

```python
from ocp_resources.exceptions import MissingTemplateVariables
```

**Constructor Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `var` | `str` | Name of the missing template variable |
| `template` | `str` | Path to the template file |

**Attributes on the caught exception:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `var` | `str` | The missing variable name |
| `template` | `str` | The template file path |

**String representation:**

```
Missing variables image for template tests/manifests/vm.yaml
```

**Example:**

```python
from ocp_resources.exceptions import MissingTemplateVariables

try:
    result = generate_yaml_from_template(name="my-vm")
    # If template also requires 'image', raises MissingTemplateVariables
except MissingTemplateVariables as e:
    print(f"Variable '{e.var}' missing in template '{e.template}'")
```

---

## Common Error-Handling Patterns

### Catching Multiple Library Exceptions

```python
from ocp_resources.exceptions import (
    ExecOnPodError,
    MissingRequiredArgumentError,
    ResourceTeardownError,
    ValidationError,
)

try:
    with Pod(client=client, name="worker", namespace="default",
             containers=[{"name": "app", "image": "myapp:latest"}],
             schema_validation_enabled=True) as pod:
        pod.execute(command=["python", "run_task.py"])
except ValidationError as e:
    print(f"Invalid resource spec: {e}")
except ExecOnPodError as e:
    print(f"Task failed (rc={e.rc}): {e.err}")
except ResourceTeardownError as e:
    print(f"Pod cleanup failed: {e}")
except MissingRequiredArgumentError as e:
    print(f"Missing field: {e.argument}")
```

### Safe Condition Waiting with Early Abort

```python
from ocp_resources.exceptions import ConditionError
from timeout_sampler import TimeoutExpiredError

try:
    resource.wait_for_condition(
        condition="Ready",
        status="True",
        timeout=180,
        stop_condition="Failed",
        stop_status="True",
    )
except ConditionError:
    # Resource entered a terminal failure state — no point waiting further
    resource.clean_up()
    raise
except TimeoutExpiredError:
    # Condition not met within timeout — may be transient
    print("Resource is taking too long, investigating...")
```

### Ignoring Non-Critical Command Failures

```python
from ocp_resources.exceptions import ExecOnPodError

# Method 1: Use ignore_rc=True
output = pod.execute(command=["grep", "ERROR", "/var/log/app.log"], ignore_rc=True)

# Method 2: Catch and inspect the return code
try:
    output = pod.execute(command=["test", "-f", "/tmp/lockfile"])
except ExecOnPodError as e:
    if e.rc == 1:
        print("Lock file does not exist — proceeding")
    else:
        raise  # Re-raise unexpected errors
```

### Validation Before Batch Deployment

```python
from ocp_resources.exceptions import ValidationError

resources = [pod1, pod2, deployment1, service1]

# Pre-validate all resources before deploying any
errors = []
for resource in resources:
    try:
        resource.validate()
    except ValidationError as e:
        errors.append((resource.name, str(e)))

if errors:
    for name, err in errors:
        print(f"  {name}: {err}")
    raise SystemExit("Fix validation errors before deploying")

for resource in resources:
    resource.deploy()
```

---

## Exception Hierarchy Summary

| Exception | Parent | Module |
|-----------|--------|--------|
| `ExecOnPodError` | `Exception` | `ocp_resources.exceptions` |
| `MissingRequiredArgumentError` | `Exception` | `ocp_resources.exceptions` |
| `ResourceTeardownError` | `Exception` | `ocp_resources.exceptions` |
| `ValidationError` | `Exception` | `ocp_resources.exceptions` |
| `ConditionError` | `Exception` | `ocp_resources.exceptions` |
| `NNCPConfigurationFailed` | `Exception` | `ocp_resources.exceptions` |
| `ClientWithBasicAuthError` | `Exception` | `ocp_resources.exceptions` |
| `MissingResourceError` | `Exception` | `ocp_resources.exceptions` |
| `MissingTemplateVariables` | `Exception` | `ocp_resources.exceptions` |

> **Warning:** `MissingResourceResError` is deprecated and will be removed in a future release. Use `MissingResourceError` instead.

## Related Pages

- [Creating and Managing Resources](creating-and-managing-resources.html)
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html)
- [Validating Resources Against OpenAPI Schemas](validating-resources.html)
- [Executing Commands in Pods and Retrieving Logs](pod-execution-and-logs.html)
- [Connecting to Clusters](connecting-to-clusters.html)
