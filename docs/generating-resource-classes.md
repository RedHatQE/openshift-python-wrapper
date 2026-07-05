Let me start by exploring the repository structure and the knowledge graph.

Now let me check the generated output example and the test generation flow:

Now let me look at a generated file with a spec section, and check one with duplicate kinds:

Let me also check the `--help` output structure and look at a few more details:

Now let me check a dry-run example and verify what shell completion setup looks like:

Now I have a thorough understanding of the codebase. Let me write the documentation:

# Generating New Resource Classes with class-generator

Scaffold Python wrapper classes for any Kubernetes or OpenShift custom resource definition (CRD) so you can manage those resources using the same patterns as built-in resources. The `class-generator` CLI introspects your cluster's OpenAPI schemas and produces ready-to-use Python files complete with typed constructors, docstrings, and `to_dict()` serialization.

## Prerequisites

- **openshift-python-wrapper** installed (see [Installing and Creating Your First Resource](quickstart.html))
- `oc` or `kubectl` CLI available on your `PATH`
- An active connection to a Kubernetes or OpenShift cluster with admin privileges (for `--kind` generation and schema updates)

## Quick Example

Generate a wrapper class for the `Deployment` resource:

```bash
class-generator -k Deployment
```

This creates a Python file in `ocp_resources/` with a fully typed class you can import and use immediately:

```python
from ocp_resources.deployment import Deployment

dep = Deployment(
    name="my-app",
    namespace="default",
    replicas=3,
    selector={"matchLabels": {"app": "my-app"}},
    template={...},
)
dep.deploy()
```

## Step-by-Step: Generating a Resource Class

### 1. Generate the class file

Pass the CRD's `Kind` (case-sensitive) to `--kind` / `-k`:

```bash
class-generator -k StorageCluster
```

The output file is automatically named using snake_case — `ocp_resources/storage_cluster.py`.

### 2. Preview without writing (dry run)

See exactly what would be generated without touching the filesystem:

```bash
class-generator -k StorageCluster --dry-run
```

The rendered Python code is printed to the console with syntax highlighting.

### 3. Review the generated file

Every generated file contains:

- A class inheriting from `Resource` (cluster-scoped) or `NamespacedResource` (namespace-scoped)
- Typed `__init__` parameters extracted from the OpenAPI spec and `status` fields
- A `to_dict()` method that serializes required and optional fields
- A `# End of generated code` marker — any code you add **below** this line is preserved on regeneration

Example generated output for `ConfigMap`:

```python
from typing import Any
from ocp_resources.resource import NamespacedResource

class ConfigMap(NamespacedResource):
    """
    ConfigMap holds configuration data for pods to consume.
    """

    api_version: str = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        binary_data: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        immutable: bool | None = None,
        **kwargs: Any,
    ) -> None:
        ...
```

### 4. Generate multiple kinds at once

Pass a comma-separated list (no spaces):

```bash
class-generator -k Pod,Service,ConfigMap
```

Multiple kinds are generated in parallel for speed.

### 5. Overwrite an existing file

By default, existing files are not overwritten. Pass `--overwrite` to replace them:

```bash
class-generator -k Deployment --overwrite
```

To create a timestamped backup before overwriting:

```bash
class-generator -k Deployment --overwrite --backup
```

Backups are stored in `.backups/backup-YYYYMMDD-HHMMSS/` preserving the original directory structure.

### 6. Write to a custom output path

```bash
class-generator -k MyCustomResource -o my_package/custom_resource.py
```

## Handling Duplicate Kinds

Some Kubernetes kinds exist in multiple API groups. For example, `DNS` exists in both `config.openshift.io` and `operator.openshift.io`. When this happens, the generator automatically creates separate files with group-based suffixes:

| Kind | API Group | Generated File |
|------|-----------|----------------|
| `DNS` | `config.openshift.io` | `dns_config_openshift_io.py` |
| `DNS` | `operator.openshift.io` | `dns_operator_openshift_io.py` |

Both files define a class named `DNS` but with different `api_group` attributes. Import the one matching the API group you need.

## Adding User Code to Generated Files

Any code you add **below** the `# End of generated code` marker is preserved when you regenerate the file with `--overwrite`. This is how built-in resources like `ConfigMap` include custom properties:

```python
    # End of generated code

    @property
    def keys_to_hash(self):
        return ["data", "binaryData"]
```

Custom imports you add at the top of the file are also preserved during regeneration.

## Updating Schemas

The generator uses a local schema cache to resolve resource definitions. If a CRD is missing (e.g., you just installed a new operator), update the cache first.

### Full schema update

Fetch all schemas from the connected cluster:

```bash
class-generator --update-schema
```

> **Note:** If connected to an older cluster, existing schemas are preserved. Only new or missing resources are added.

### Single-resource schema update

Update just one resource without touching the rest:

```bash
class-generator --update-schema-for LlamaStackDistribution
```

Then generate the class:

```bash
class-generator -k LlamaStackDistribution --overwrite
```

> **Warning:** `--update-schema` and `--update-schema-for` are mutually exclusive. Use one or the other.

## Discovering Missing Resources

Find resources on your cluster that don't have wrapper classes yet:

```bash
class-generator --discover-missing
```

### Coverage report

Get a summary of how many resources have wrapper classes:

```bash
class-generator --coverage-report
```

Output in JSON for CI/CD pipelines:

```bash
class-generator --coverage-report --json
```

### Auto-generate all missing resources

Update schemas and generate classes for every resource that's missing:

```bash
class-generator --update-schema --generate-missing
```

> **Tip:** Use `--dry-run` with `--generate-missing` to preview what would be generated without writing any files.

## Advanced Usage

### Batch regeneration

Regenerate all existing generated resource classes to pick up schema changes:

```bash
class-generator --regenerate-all
```

With backups:

```bash
class-generator --regenerate-all --backup
```

Filter to a subset of resources using glob patterns:

```bash
class-generator --regenerate-all --filter "Pod*"
class-generator --regenerate-all --filter "*Service"
```

### Adding tests

Generate test files alongside the resource class:

```bash
class-generator -k Pod --add-tests
```

This creates test manifests and runs them automatically with `pytest`. Tests are placed under the test manifests directory and validate that the generated class can be parsed correctly.

### Shell completion

Add this to your `~/.bashrc` or `~/.zshrc` for tab completion:

```bash
# For zsh
if type class-generator > /dev/null; then eval "$(_CLASS_GENERATOR_COMPLETE=zsh_source class-generator)"; fi

# For bash
if type class-generator > /dev/null; then eval "$(_CLASS_GENERATOR_COMPLETE=bash_source class-generator)"; fi
```

### Verbose output

Enable debug logging to see exactly what the generator is doing:

```bash
class-generator -k Deployment -v
```

### When a kind is missing from the schema

If the kind you request is not in the local schema cache, the CLI prompts you:

```
deployment not found in schema mapping, Do you want to run --update-schema and retry? [Y/N]:
```

Answering `y` triggers a schema update and retries generation automatically.

> **Note:** The prompt only appears in interactive mode. When generating multiple kinds or running in batch mode, missing kinds are skipped with a warning. Run `--update-schema` separately beforehand in CI environments.

### API group and version warnings

If a generated resource uses an API group or version that hasn't been registered in the base `Resource` class, the generator logs a warning like:

```
Missing API Group in Resource
Please add `Resource.ApiGroup.MY_GROUP_IO = my-group.io` manually into
ocp_resources/resource.py under Resource class > ApiGroup class.
```

Follow the instructions to register the API group so the resource can connect to the correct API endpoint. See [Understanding the Resource Class Hierarchy](resource-class-hierarchy.html) for details on how `ApiGroup` and `ApiVersion` are used.

## CLI Options Reference

| Option | Description |
|--------|-------------|
| `-k`, `--kind` | Kind(s) to generate (comma-separated) |
| `-o`, `--output-file` | Custom output file path |
| `--overwrite` | Overwrite existing files |
| `--dry-run` | Preview output without writing files |
| `--add-tests` | Generate test files for the kind |
| `--update-schema` | Update all schema files from cluster |
| `--update-schema-for` | Update schema for a single kind |
| `--discover-missing` | Find resources without wrapper classes |
| `--coverage-report` | Show coverage statistics |
| `--json` | Output reports in JSON format |
| `--generate-missing` | Generate classes for all missing resources |
| `--regenerate-all` | Regenerate all existing generated classes |
| `--backup` | Create backup before overwriting/regenerating |
| `--filter` | Glob pattern to filter `--regenerate-all` |
| `-v`, `--verbose` | Enable debug logging |

For the full CLI reference, see [class-generator CLI Reference](class-generator-cli.html).

## Troubleshooting

**"Neither 'oc' nor 'kubectl' binary found in PATH"**
Install `oc` from the [OpenShift mirror](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/) or `kubectl` from the [Kubernetes docs](https://kubernetes.io/docs/tasks/tools/). Ensure the binary is on your `PATH`.

**"Resource kind 'X' not found"**
The kind is not in the local schema cache. Run `class-generator --update-schema` while connected to a cluster that has the CRD installed, then retry.

**Generated filename looks wrong (e.g., `c_d_i_config.py`)**
Single-letter segments in snake_case names indicate the camelCase-to-snake_case converter doesn't recognize an acronym. The generator raises an error with instructions to add the acronym to the converter.

**"Failed to fetch OpenAPI v3 index"**
Ensure you are logged in to the cluster with sufficient privileges. The generator needs to access the `/openapi/v3` endpoint, which typically requires cluster-admin access.

## Related Pages

- [class-generator CLI Reference](class-generator-cli.html)
- [Schema Validation and Code Generation Architecture](schema-validation-internals.html)
- [Understanding the Resource Class Hierarchy](resource-class-hierarchy.html)
- [Resource and NamespacedResource API](resource-api.html)
- [Validating Resources Against OpenAPI Schemas](validating-resources.html)
