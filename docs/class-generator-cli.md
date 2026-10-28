I'll start by reading the knowledge graph and page manifest, then explore the class-generator source code in detail.

Now let me check the entry point configuration and any additional schema-related functions:

Now let me check the test files for CLI tests and the entry point:

Now let me check the parsers and any additional CLI-relevant components:

Now I have all the information I need. Let me compile the comprehensive CLI reference page.

# class-generator CLI Reference

The `class-generator` command generates Python wrapper classes for Kubernetes and OpenShift resources. It is installed as a console script entry point from the `openshift-python-wrapper` package.

```
class-generator = "class_generator.cli:main"
```

```bash
pip install openshift-python-wrapper
# or
uv tool install openshift-python-wrapper
```

> **Tip:** Enable shell completion by adding to `~/.bashrc` or `~/.zshrc`:
> ```bash
> if type class-generator > /dev/null; then eval "$(_CLASS_GENERATOR_COMPLETE=zsh_source class-generator)"; fi
> ```

## Synopsis

```
class-generator [OPTIONS]
```

At least one action option must be specified: `--kind`, `--update-schema`, `--update-schema-for`, `--discover-missing`, `--coverage-report`, `--generate-missing`, or `--regenerate-all`.

---

## Options Reference

### Kind Generation

#### `-k`, `--kind`

| Property | Value |
|----------|-------|
| **Type** | `STRING` |
| **Default** | `None` |
| **Required** | No (but at least one action must be specified) |
| **Requires** | Connected cluster with admin privileges |

Generate Python wrapper classes for the specified Kubernetes resource Kind(s). Multiple kinds can be comma-separated (no spaces).

When a kind is not found in the local schema mapping file, the CLI interactively prompts to run `--update-schema` (only in interactive CLI mode).

```bash
# Single kind
class-generator -k Pod

# Multiple kinds (processed in parallel)
class-generator -k Deployment,Pod,ConfigMap
```

When multiple kinds share the same Kind name but belong to different API groups (e.g., `DNS` from `config.openshift.io` and `operator.openshift.io`), separate files are generated with API group suffixes:

```
dns_config_openshift_io.py
dns_operator_openshift_io.py
```

---

#### `-o`, `--output-file`

| Property | Value |
|----------|-------|
| **Type** | `PATH` |
| **Default** | `ocp_resources/<snake_case_kind>.py` |
| **Required** | No |

Override the output file path for the generated Python module. If not provided, the filename is derived from the Kind using `convert_camel_case_to_snake_case`.

```bash
class-generator -k Pod -o my_custom_pod.py
```

> **Note:** When generating multiple comma-separated kinds, the `--output-file` value applies to all kinds. For independent output paths, run separate commands.

---

#### `--overwrite`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |

Overwrite an existing output file. Without this flag, if the target file already exists, a `_TEMP.py` suffixed file is created instead.

When overwriting, any user-added code blocks (code after the `# End of generated code` marker) and user imports are preserved in the regenerated file.

```bash
class-generator -k Pod --overwrite
```

---

#### `--dry-run`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |

Preview the generated output without writing any files. The generated Python code is printed to the console with syntax highlighting and line numbers using Rich.

```bash
class-generator -k Pod --dry-run
```

---

#### `--backup`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |
| **Requires** | `--regenerate-all` or `--overwrite` |

Create a timestamped backup of existing files before overwriting or regenerating. Backups are stored in `.backups/backup-YYYYMMDD-HHMMSS/` preserving the original directory structure.

```bash
class-generator -k Pod --overwrite --backup
```

> **Note:** Using `--backup` without either `--regenerate-all` or `--overwrite` results in a constraint error.

---

### Test Generation

#### `--add-tests`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |
| **Requires** | `-k`/`--kind` |

Generate test files for the specified Kind and run them. This performs two actions:

1. Generates a test manifest in `class_generator/tests/manifests/<Kind>/` and regenerates `class_generator/tests/test_class_generator.py` from the Jinja2 template.
2. Runs the generated test file using `uv run --group tests pytest class_generator/tests/test_class_generator.py`.

```bash
class-generator -k Pod --add-tests
```

> **Warning:** `--add-tests` cannot be used without `-k`/`--kind`. Running `class-generator --add-tests` alone exits with a non-zero status.

---

### Schema Management

#### `--update-schema`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |
| **Requires** | Connected cluster; `oc` or `kubectl` in PATH |
| **Mutually exclusive with** | `--update-schema-for` |

Fetch all resource schemas from the connected cluster's OpenAPI v3 endpoints and update the local schema files:

- `class_generator/schema/__resources-mappings.json` (compressed as `.json.gz`)
- `class_generator/schema/_definitions.json`

The update strategy depends on the cluster version:

| Cluster Version | Behavior |
|-----------------|----------|
| Same or newer than last update | Full update — fetches all schemas, updates existing resources |
| Older than last update | Incremental — only adds missing resources, preserves existing schemas |

When used alone, exits after updating. When combined with `--generate-missing`, continues to resource generation after the update.

```bash
# Update schema only
class-generator --update-schema

# Update schema then generate missing resources
class-generator --update-schema --generate-missing
```

> **Note:** When `--update-schema` is used without `--generate-missing`, it cannot be combined with `-k`, `--discover-missing`, `--coverage-report`, `--dry-run`, `--overwrite`, `-o`, `--add-tests`, or `--regenerate-all`.

---

#### `--update-schema-for`

| Property | Value |
|----------|-------|
| **Type** | `STRING` |
| **Default** | `None` |
| **Requires** | Connected cluster; `oc` or `kubectl` in PATH |
| **Mutually exclusive with** | `--update-schema` |

Update the schema for a single resource Kind without affecting other resources. The Kind name is **case-sensitive**.

This fetches only the API paths relevant to the specified Kind, updates (or adds) its schema in the mapping file, and exits.

```bash
class-generator --update-schema-for LlamaStackDistribution
```

Use cases:
- Connected to an older cluster but need to update a specific CRD
- A new operator was installed and you need its resource schema
- Refreshing just one resource without a full schema update

After updating, regenerate the class:

```bash
class-generator --update-schema-for LlamaStackDistribution
class-generator -k LlamaStackDistribution --overwrite
```

**Errors:**

| Error | Cause |
|-------|-------|
| `ResourceNotFoundError` | The Kind is not found on the cluster (CRD not installed or name misspelled) |
| `RuntimeError` | API paths not found or schema extraction failed |

> **Note:** Cannot be combined with `-k`, `--discover-missing`, `--coverage-report`, `--generate-missing`, or `--regenerate-all`.

---

### Coverage and Discovery

#### `--discover-missing`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |

Analyze resource coverage by comparing schema-mapped resources against implemented wrapper classes in `ocp_resources/`. Generates a console report showing coverage statistics and missing resources.

```bash
class-generator --discover-missing
```

---

#### `--coverage-report`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |

Generate a detailed coverage report showing:

| Metric | Description |
|--------|-------------|
| Total Resources in Schema | Number of resource Kinds in the schema mapping |
| Auto-Generated Resources | Wrapper classes with the generated marker |
| Coverage | Percentage of mapped resources with generated classes |
| Missing (Not Generated) | Resources in schema but without generated classes |
| Manual Implementations | Resource classes without the generated marker |

```bash
# Console output (default)
class-generator --coverage-report

# JSON output
class-generator --coverage-report --json
```

---

#### `--json`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |

Output reports in JSON format instead of Rich console tables. Applies to `--coverage-report`, `--discover-missing`, and `--generate-missing`.

The JSON output structure:

```json
{
  "generated_resources": ["ConfigMap", "Deployment", "Pod"],
  "manual_resources": ["VirtualMachine"],
  "missing_resources": [{"kind": "Binding"}, {"kind": "ComponentStatus"}],
  "coverage_stats": {
    "total_in_mapping": 400,
    "total_generated": 197,
    "total_manual": 25,
    "coverage_percentage": 49.25,
    "missing_count": 203
  }
}
```

```bash
class-generator --coverage-report --json
```

---

#### `--generate-missing`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |

Generate wrapper classes for all resources found in the schema mapping that do not yet have generated files. Each missing resource Kind is passed to `class_generator()` individually.

Can be combined with `--update-schema` to first refresh the schema, then generate all missing classes.

```bash
# Generate missing resources
class-generator --generate-missing

# Update schema first, then generate missing
class-generator --update-schema --generate-missing

# Dry run to preview
class-generator --generate-missing --dry-run
```

---

### Batch Regeneration

#### `--regenerate-all`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |

Regenerate all existing generated resource classes using the latest schemas. Only files containing the `# Generated using` marker in `ocp_resources/` are processed.

Regeneration runs in parallel (up to 10 workers). User-added code (below `# End of generated code`) is preserved during regeneration.

```bash
# Regenerate all resources
class-generator --regenerate-all

# With backup
class-generator --regenerate-all --backup

# Dry run
class-generator --regenerate-all --dry-run

# Filter to specific resources
class-generator --regenerate-all --filter "Pod*"
```

Output summary:

```
Regeneration complete: 195 succeeded, 2 failed
Backup files stored in: .backups/backup-20260705-143022
```

---

#### `--filter`

| Property | Value |
|----------|-------|
| **Type** | `STRING` |
| **Default** | `None` |
| **Requires** | `--regenerate-all` |

Filter which resources to regenerate using a glob pattern matched against the resource Kind name. Uses `fnmatch` semantics.

```bash
# Regenerate only Pod-related resources
class-generator --regenerate-all --filter "Pod*"

# Regenerate resources ending in "Service"
class-generator --regenerate-all --filter "*Service"

# Regenerate a specific resource
class-generator --regenerate-all --filter "VirtualMachine"
```

---

### Logging

#### `-v`, `--verbose`

| Property | Value |
|----------|-------|
| **Type** | Flag |
| **Default** | `False` |

Enable verbose output with debug-level logs. Sets `DEBUG` level on the following loggers:

- `class_generator.core.schema`
- `class_generator.core.generator`
- `class_generator.core.coverage`
- `class_generator.core.discovery`
- `class_generator.cli`
- `class_generator.utils`
- `ocp_resources`

```bash
class-generator -k Pod -v
```

---

## Constraint Rules

The CLI enforces the following option constraints:

| Constraint | Rule |
|------------|------|
| `--update-schema` ↔ `--update-schema-for` | Mutually exclusive |
| `--update-schema` (alone) | Cannot combine with `-k`, `--discover-missing`, `--coverage-report`, `--dry-run`, `--overwrite`, `-o`, `--add-tests`, `--regenerate-all` |
| `--update-schema-for` | Cannot combine with `-k`, `--discover-missing`, `--coverage-report`, `--generate-missing`, `--regenerate-all` |
| `--backup` | Requires `--regenerate-all` or `--overwrite` |
| `--filter` | Requires `--regenerate-all` |
| No options | Exits with error — at least one action required |

---

## Execution Order

When multiple compatible options are specified together, the CLI processes them in this fixed order:

1. `--update-schema-for` (exits after completion)
2. `--update-schema` (exits unless `--generate-missing` is also set)
3. `--coverage-report` / `--discover-missing` / `--generate-missing` (coverage analysis and reporting)
4. `--generate-missing` (generates classes for missing resources)
5. `--regenerate-all` (batch regeneration, exits after completion)
6. `-k`/`--kind` (normal kind generation)
7. `--add-tests` (test generation and execution)

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Generation failure, schema update failure, resource not found, or any kind in a batch failed |
| `2` | Invalid CLI arguments or constraint violation |

---

## Programmatic API

The generation logic can be invoked directly from Python. See [Generating New Resource Classes with class-generator](generating-resource-classes.html) for usage examples.

### `class_generator.core.generator.class_generator()`

```python
from class_generator.core.generator import class_generator

generated_files: list[str] = class_generator(
    kind="Pod",
    overwrite=False,
    dry_run=False,
    output_file="",
    output_dir="",
    add_tests=False,
    called_from_cli=True,
    update_schema_executed=False,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `kind` | `str` | *(required)* | Kubernetes resource Kind |
| `overwrite` | `bool` | `False` | Overwrite existing files |
| `dry_run` | `bool` | `False` | Preview output without writing files |
| `output_file` | `str` | `""` | Specific output file path |
| `output_dir` | `str` | `""` | Output directory (defaults to `ocp_resources`) |
| `add_tests` | `bool` | `False` | Generate test files |
| `called_from_cli` | `bool` | `True` | Enables interactive prompts when `True` |
| `update_schema_executed` | `bool` | `False` | Whether schema update was already performed |

**Returns:** `list[str]` — List of generated file paths. Empty list if the kind is not found in the schema mapping (when `called_from_cli=False`).

**Raises:**
- `RuntimeError` — Kind not found after schema update, or user declined schema update
- `ValueError` — Generated filename contains invalid patterns (single-letter segments)

---

### `class_generator.core.generator.generate_resource_file_from_dict()`

```python
from class_generator.core.generator import generate_resource_file_from_dict

orig_filename, generated_filename = generate_resource_file_from_dict(
    resource_dict={"kind": "Pod", ...},
    overwrite=False,
    dry_run=False,
    output_file="",
    add_tests=False,
    output_file_suffix="",
    output_dir="",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resource_dict` | `dict[str, Any]` | *(required)* | Dictionary containing parsed resource information |
| `overwrite` | `bool` | `False` | Overwrite existing files |
| `dry_run` | `bool` | `False` | Preview without writing |
| `output_file` | `str` | `""` | Specific output file path |
| `add_tests` | `bool` | `False` | Generate test files under `class_generator/tests/manifests/` |
| `output_file_suffix` | `str` | `""` | Suffix appended to filename (for API group disambiguation) |
| `output_dir` | `str` | `""` | Output directory (defaults to `ocp_resources`) |

**Returns:** `tuple[str, str]` — `(original_filename, generated_filename)`. These differ when a `_TEMP.py` file is created.

---

### `class_generator.core.schema.update_kind_schema()`

```python
from class_generator.core.schema import update_kind_schema

update_kind_schema(client=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `client` | `str \| None` | `None` | Path to `oc`/`kubectl` binary. Auto-detected if `None`. |

**Raises:**
- `ClusterVersionError` — Cannot determine cluster version
- `RuntimeError` — Failed to fetch OpenAPI v3 index
- `OSError` — Failed to write schema files

---

### `class_generator.core.schema.update_single_resource_schema()`

```python
from class_generator.core.schema import update_single_resource_schema

update_single_resource_schema(kind="LlamaStackDistribution", client=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `kind` | `str` | *(required)* | Resource Kind name (case-sensitive) |
| `client` | `str \| None` | `None` | Path to `oc`/`kubectl` binary. Auto-detected if `None`. |

**Raises:**
- `ResourceNotFoundError` — Kind not found on the cluster
- `RuntimeError` — Schema extraction or save failed

---

### `class_generator.core.coverage.analyze_coverage()`

```python
from class_generator.core.coverage import analyze_coverage

result: dict[str, Any] = analyze_coverage(resources_dir="ocp_resources")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resources_dir` | `str` | `"ocp_resources"` | Directory to scan for wrapper classes |

**Returns:** `dict[str, Any]` with keys:

| Key | Type | Description |
|-----|------|-------------|
| `generated_resources` | `list[str]` | Sorted list of auto-generated resource class names |
| `manual_resources` | `list[str]` | Sorted list of manually written resource class names |
| `missing_resources` | `list[dict]` | List of `{"kind": "..."}` for resources in schema but not generated |
| `coverage_stats` | `dict` | Statistics including `total_in_mapping`, `total_generated`, `total_manual`, `coverage_percentage`, `missing_count` |

---

### `class_generator.core.discovery.discover_generated_resources()`

```python
from class_generator.core.discovery import discover_generated_resources

resources: list[dict[str, Any]] = discover_generated_resources()
```

**Returns:** `list[dict[str, Any]]` — Each dict contains:

| Key | Type | Description |
|-----|------|-------------|
| `path` | `str` | Full path to the resource file |
| `kind` | `str` | Resource class name |
| `filename` | `str` | File name without extension |
| `has_user_code` | `bool` | Whether file contains user modifications below `# End of generated code` |

---

### `class_generator.core.discovery.discover_cluster_resources()`

```python
from class_generator.core.discovery import discover_cluster_resources

resources: dict[str, list[dict[str, Any]]] = discover_cluster_resources(
    client=None,
    api_group_filter=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `client` | `DynamicClient \| None` | `None` | Kubernetes dynamic client. Creates one if `None`. |
| `api_group_filter` | `str \| None` | `None` | Filter by API group name |

**Returns:** `dict[str, list[dict[str, Any]]]` — Mapping of API version to list of resource dicts (`name`, `kind`, `namespaced`).

**Raises:** `ValueError` — If client is not a `DynamicClient` instance.

---

## Exceptions

### `class_generator.exceptions.ResourceNotFoundError`

```python
from class_generator.exceptions import ResourceNotFoundError
```

Raised when a resource Kind is not found in the schema mapping or on the cluster.

| Attribute | Type | Description |
|-----------|------|-------------|
| `kind` | `str` | The Kind that was not found |

### `class_generator.core.schema.ClusterVersionError`

```python
from class_generator.core.schema import ClusterVersionError
```

Raised when the cluster version cannot be determined (client binary missing, cluster unreachable, or authentication failure).

---

## Schema Files

The CLI manages two schema files under `class_generator/schema/`:

| File | Purpose |
|------|---------|
| `__resources-mappings.json.gz` | Compressed JSON mapping of lowercase Kind → list of schemas with GVK metadata and namespaced status |
| `_definitions.json` | JSON Schema definitions for `$ref` resolution during validation |
| `__cluster_version__.txt` | Last cluster version used for schema generation |

See [Schema Validation and Code Generation Architecture](schema-validation-internals.html) for details on how these files are structured and consumed.

---

## Common Workflows

### Generate a new resource class

```bash
class-generator -k MyCustomResource
```

### Update schema and regenerate all classes

```bash
class-generator --update-schema
class-generator --regenerate-all --backup
```

### Add a new CRD to an older cluster

```bash
class-generator --update-schema-for MyNewCRD
class-generator -k MyNewCRD
```

### CI/CD coverage check

```bash
class-generator --coverage-report --json > coverage.json
```

### Preview changes before writing

```bash
class-generator -k Pod --dry-run
class-generator --regenerate-all --dry-run
```

---

## Related Pages

- [Generating New Resource Classes with class-generator](generating-resource-classes.html) — Step-by-step guide for scaffolding resource classes
- [Resource and NamespacedResource API](resource-api.html) — API reference for the base classes that generated code extends
- [Understanding the Resource Class Hierarchy](resource-class-hierarchy.html) — How generated subclasses fit into the class hierarchy
- [Schema Validation and Code Generation Architecture](schema-validation-internals.html) — Internals of schema fetching, caching, and code generation
- [Environment Variables and Configuration](environment-variables.html) — Environment variables that affect runtime behavior

## Related Pages

- [Generating New Resource Classes with class-generator](generating-resource-classes.html)
- [Schema Validation and Code Generation Architecture](schema-validation-internals.html)
- [Understanding the Resource Class Hierarchy](resource-class-hierarchy.html)
- [Resource and NamespacedResource API](resource-api.html)
- [Environment Variables and Configuration](environment-variables.html)
