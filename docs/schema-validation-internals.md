Let me start by reading the knowledge graph and the pages manifest, then explore the relevant source files.

Now let me look at some more key files - the explain parser, resource base class validation, archive utils, and some test files:

Now let me look at the exceptions module for validation:

Now let me check the CI/CD configuration to understand how schemas are updated:

Let me look at a few generated resource files to understand the output of the code generation:

Let me also check the parsers for status schema generation:

Now let me check what data is actually in the schema file to understand the structure:

Now I have enough information. Let me write the documentation page.

# Schema Validation and Code Generation Architecture

The openshift-python-wrapper uses OpenAPI schemas as the single source of truth for two critical capabilities: **validating resource definitions** before they reach the cluster, and **generating Python wrapper classes** for any Kubernetes or OpenShift resource type. Understanding this architecture helps you diagnose validation errors, generate classes for custom resources, and keep your schemas up to date as clusters evolve.

## The Big Picture

OpenAPI schemas flow through the system in two directions: they are fetched from a live cluster and stored locally, then consumed by the validation engine at runtime and by the code generator at development time.

| Component | Location | Purpose |
|---|---|---|
| **Schema Fetcher** | `class_generator/core/schema.py` | Connects to a cluster, downloads OpenAPI v3 schemas, and writes them to disk |
| **Resource Mappings** | `class_generator/schema/__resources-mappings.json.gz` | Compressed archive mapping each resource kind (lowercase) to its schema(s) |
| **Definitions File** | `class_generator/schema/_definitions.json` | JSON file containing detailed schema definitions with `$ref` targets for nested types |
| **Schema Validator** | `ocp_resources/utils/schema_validator.py` | Runtime engine that loads schemas, resolves `$ref` references, and validates resource dicts |
| **Code Generator** | `class_generator/core/generator.py` | Reads schemas and generates Python class files from a Jinja2 template |
| **Explain Parser** | `class_generator/parsers/explain_parser.py` | Parses the resource mapping to extract fields, types, and group-version-kind metadata |
| **Cluster Version Tracker** | `class_generator/schema/__cluster_version__.txt` | Tracks the cluster version that last produced the schema, controlling update strategy |

### Data Flow: Schema Fetch and Storage

1. **Detect client binary** — The system finds `oc` or falls back to `kubectl` via `get_client_binary()`.
2. **Check cluster version** — `check_and_update_cluster_version()` compares the connected cluster's version against the stored version in `__cluster_version__.txt`.
3. **Determine update strategy** — If the cluster is the same version or newer, all schemas are fetched and existing entries are updated. If older, only missing resources are fetched and existing schemas are preserved.
4. **Fetch OpenAPI v3 index** — `GET /openapi/v3` returns an index of all API group paths (e.g., `api/v1`, `apis/apps/v1`).
5. **Fetch schemas in parallel** — `fetch_all_api_schemas()` downloads schemas from each API path using a thread pool (up to 10 workers).
6. **Build namespacing dictionary** — `build_namespacing_dict()` queries `api-resources` to determine which kinds are namespaced vs. cluster-scoped.
7. **Process definitions** — `process_schema_definitions()` extracts `x-kubernetes-group-version-kind` metadata, builds schema entries, and merges them into the resource mappings. Existing resources are **never deleted** — only added or updated.
8. **Supplement with `oc explain`** — Missing field descriptions, required-field markers, and `$ref` definitions are filled in by running `oc explain` commands in parallel.
9. **Write to disk** — The resource mappings are saved as a gzip-compressed JSON archive (`__resources-mappings.json.gz`), and definitions are written to `_definitions.json`.

### Data Flow: Validation at Runtime

1. **Load on first use** — `SchemaValidator.load_mappings_data()` decompresses and loads the mappings archive and definitions file into class-level caches.
2. **Look up by kind** — `SchemaValidator.load_schema(kind, api_group)` finds the schema for a resource kind (case-insensitive). When multiple API groups define the same kind (e.g., `Ingress` in `networking.k8s.io` and `config.openshift.io`), the `api_group` parameter disambiguates.
3. **Resolve `$ref` references** — The validator recursively resolves all `$ref` pointers against the definitions data, producing a self-contained schema.
4. **Cache resolved schemas** — Resolved schemas are stored in `_schema_cache` keyed by `api_group:kind`, so subsequent validations are fast.
5. **Validate with jsonschema** — `jsonschema.validate()` checks the resource dictionary against the resolved schema.
6. **Format errors** — If validation fails, `format_validation_error()` produces a human-readable message including the field path, error details, and schema context.

### Data Flow: Code Generation

1. **Read resource mappings** — `parse_explain()` loads the mapping file and finds all schema entries for the requested kind.
2. **Select latest API version** — When multiple versions exist within an API group, the latest version is selected using a priority ranking (`v2 > v1 > v1beta2 > v1beta1 > v1alpha2 > v1alpha1`).
3. **Extract fields and types** — The `type_parser` module converts OpenAPI types to Python type annotations and builds parameter dictionaries for the class constructor.
4. **Render Jinja2 template** — `render_jinja_template()` processes `class_generator_template.j2` with the extracted data, producing a complete Python class.
5. **Preserve user code** — If the target file already exists, `parse_user_code_from_file()` extracts any user-added code below the `# End of generated code` marker and re-inserts it after regeneration.
6. **Format and write** — `write_and_format_rendered()` writes the file, then runs `prek` (pre-commit hooks) or falls back to `ruff` for formatting.

## Key Concepts

### The Resource Mappings File

The resource mappings file (`__resources-mappings.json.gz`) is the central schema store. It maps lowercase kind names to arrays of schema objects:

```json
{
  "pod": [
    {
      "description": "Pod is a collection of containers...",
      "properties": { ... },
      "required": [],
      "type": "object",
      "x-kubernetes-group-version-kind": [
        { "group": "", "kind": "Pod", "version": "v1" }
      ],
      "namespaced": true
    }
  ],
  "ingress": [
    { "x-kubernetes-group-version-kind": [{ "group": "networking.k8s.io", ... }], ... },
    { "x-kubernetes-group-version-kind": [{ "group": "config.openshift.io", ... }], ... }
  ]
}
```

Resources with the same kind but different API groups (like `Ingress` above) are stored as separate entries in the array. This structure allows the validator and generator to handle API group disambiguation correctly.

> **Note:** The mappings file is compressed with gzip to reduce repository size. The `archive_utils` module handles transparent compression and decompression via `save_json_archive()` and `load_json_archive()`.

### The Definitions File

The definitions file (`_definitions.json`) contains detailed schema definitions keyed by `group/version/Kind` paths (e.g., `apps/v1/Deployment`, `v1/Pod`). It also stores referenced sub-schemas like `io.k8s.api.core.v1.PodSpec` that are targets of `$ref` pointers. During validation, the `SchemaValidator` uses this file as the reference store for resolving nested types.

### SchemaValidator

`SchemaValidator` is a class with only class-level methods and caches — you never need to instantiate it. It serves as the shared validation engine used by both `Resource.validate()` and `Resource.validate_dict()`.

```python
from ocp_resources.utils.schema_validator import SchemaValidator
```

| Method | Signature | Description |
|---|---|---|
| `load_mappings_data` | `(skip_cache: bool = False) -> bool` | Loads the mappings archive and definitions file. Returns `True` on success. |
| `get_mappings_data` | `(skip_cache: bool = False) -> dict[str, Any] \| None` | Returns loaded mappings data, loading first if needed. |
| `get_definitions_data` | `() -> dict[str, Any] \| None` | Returns loaded definitions data, loading first if needed. |
| `load_schema` | `(kind: str, api_group: str \| None = None) -> dict[str, Any] \| None` | Loads and resolves a complete schema for a kind. Handles API group disambiguation and caching. |
| `validate` | `(resource_dict: dict[str, Any], kind: str, api_group: str \| None = None) -> None` | Validates a resource dict. Raises `jsonschema.ValidationError` on failure. |
| `format_validation_error` | `(error, kind, name, api_group=None) -> str` | Formats a validation error into a user-friendly message with field path and context. |
| `clear_cache` | `() -> None` | Clears the resolved schema cache (not the raw mappings/definitions data). |

> **Tip:** The `load_schema` method resolves `$ref` references recursively. For core Kubernetes types like `ObjectMeta` or `TypeMeta` that may be missing from definitions, it falls back to a permissive `{"type": "object", "additionalProperties": true}` schema rather than failing outright.

### Resource Validation Methods

The `Resource` base class exposes two validation methods that delegate to `SchemaValidator`:

```python
from ocp_resources.resource import Resource

# Instance-level validation — validates self.res
resource.validate()

# Class-level validation — validates any dict against the class's schema
MyResource.validate_dict(resource_dict)
```

Both raise `ocp_resources.exceptions.ValidationError` (not the raw `jsonschema.ValidationError`) with formatted error messages that include the resource identifier, field path, and details.

**Auto-validation** can be enabled per-instance by passing `schema_validation_enabled=True` to the constructor:

```python
from ocp_resources.pod import Pod

pod = Pod(
    name="my-pod",
    namespace="default",
    containers=[{"name": "app", "image": "nginx"}],
    client=client,
    schema_validation_enabled=True,
)
# validation runs automatically before create() and update_replace()
pod.deploy()
```

When auto-validation is enabled:
- `create()` calls `self.validate()` after `to_dict()` builds the resource dictionary
- `update_replace()` calls `validate_dict()` on the replacement resource dictionary
- `update()` (patch operations) does **not** trigger validation because patches are partial documents that may not pass full schema validation

### Schema Update Strategies

The `update_kind_schema()` function employs a version-aware update strategy:

| Cluster Version | Behavior |
|---|---|
| **Same or newer** than last recorded | Fetches **all** API schemas, updates existing resources, supplements with `oc explain` data |
| **Older** than last recorded | Identifies only **missing** resources via `identify_missing_resources()`, fetches only relevant API paths, does **not** modify existing schemas |

This strategy prevents an older cluster from overwriting schemas that contain richer data from a newer cluster.

> **Warning:** If you connect to an older cluster and need to update a specific CRD's schema (for example, after installing a new operator), use `update_single_resource_schema(kind)` or the CLI flag `--update-schema-for <Kind>`. This bypasses the version guard for that one resource.

### Single-Resource Schema Updates

The `update_single_resource_schema()` function fetches the schema for exactly one resource kind without affecting other resources in the mapping:

```python
from class_generator.core.schema import update_single_resource_schema

update_single_resource_schema(kind="LlamaStackDistribution")
```

| Parameter | Type | Description |
|---|---|---|
| `kind` | `str` | The resource Kind (case-sensitive, e.g., `"LlamaStackDistribution"`) |
| `client` | `str \| None` | Client binary path. Auto-detected if `None`. |

**Raises:**
- `ResourceNotFoundError` — if the kind is not found on the cluster
- `RuntimeError` — if schema fetching fails

### Code Generation Pipeline

The `class_generator()` function orchestrates the full generation pipeline:

```python
from class_generator.core.generator import class_generator

generated_files = class_generator(kind="Deployment", overwrite=True)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `kind` | `str` | (required) | Kubernetes resource kind |
| `overwrite` | `bool` | `False` | Overwrite existing files |
| `dry_run` | `bool` | `False` | Print output without writing |
| `output_file` | `str` | `""` | Specific output file path |
| `output_dir` | `str` | `""` | Output directory (defaults to `ocp_resources`) |
| `add_tests` | `bool` | `False` | Generate test files in `class_generator/tests/manifests/` |

**Returns:** `list[str]` — paths of generated files.

**Raises:**
- `RuntimeError` — if the kind is not found in schema mappings
- `ValueError` — if the generated filename contains invalid patterns

When a kind exists in multiple API groups (e.g., `Ingress` in both `networking.k8s.io` and `config.openshift.io`), the generator produces **separate files** with a group-based suffix (e.g., `ingress_networking_k8s_io.py`, `ingress_config_openshift_io.py`).

### Generated Class Structure

Every generated file follows a consistent structure produced by the Jinja2 template:

```python
# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md

from typing import Any
from ocp_resources.resource import NamespacedResource

class Pod(NamespacedResource):
    """Pod is a collection of containers that can run on a host."""

    api_version: str = NamespacedResource.ApiVersion.V1

    def __init__(self, containers: list[Any] | None = None, ..., **kwargs: Any) -> None:
        """Args:
            containers (list[Any]): List of containers belonging to the pod.
            ...
        """
        super().__init__(**kwargs)
        self.containers = containers
        ...

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            # Required fields raise MissingRequiredArgumentError
            # Optional fields added only if not None
            ...
    # End of generated code
```

User-added code placed **after** the `# End of generated code` marker is preserved across regenerations.

### `$ref` Resolution

OpenAPI schemas extensively use `$ref` pointers to reference shared type definitions (e.g., `"$ref": "#/components/schemas/io.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta"`). The `SchemaValidator._resolve_refs()` method handles this by:

1. Parsing the reference path to extract the definition name
2. Looking up the definition in `_definitions_data` using multiple key formats (full dotted path, short name, or `version/Kind` format)
3. Recursively resolving any `$ref` pointers within the resolved definition
4. Falling back to a permissive object schema for well-known core types that may be missing

### Schema Supplementation via `oc explain`

The raw OpenAPI v3 schemas from the cluster sometimes lack field descriptions and required-field markers. The system supplements these gaps by:

- Running `oc explain <resource>.<field>` commands **in parallel** for critical resource types (Pod, Deployment, Service, etc.)
- Parsing the explain output to extract field descriptions, types, and required-field markers
- Merging descriptions into existing schema properties where they are missing
- Detecting missing `$ref` targets and fetching their definitions via `oc explain --recursive`

This supplementation only runs during a **full update** (same or newer cluster version), not when only fetching missing resources.

## How It Affects You

| What you do | What happens under the hood |
|---|---|
| Call `resource.validate()` | `SchemaValidator` loads schemas from the compressed archive, resolves `$ref` references, validates with jsonschema, and raises `ValidationError` with a formatted message |
| Pass `schema_validation_enabled=True` | `create()` and `update_replace()` automatically validate before sending to the API server |
| Run `class-generator --update-schema` | Full schema fetch from cluster, version check, parallel API downloads, `oc explain` supplementation, and compressed archive write |
| Run `class-generator -k Pod` | Reads the mapping for `pod`, parses fields/types, renders Jinja2 template, preserves user code, writes and formats the Python file |
| Run `class-generator --update-schema-for MyResource` | Single-resource fetch that bypasses the cluster version guard |
| Run `class-generator --regenerate-all` | Discovers all generated files (by marker comment), regenerates each in parallel, preserving user code |
| Validation reports "No schema found" | The resource kind is not in the mappings archive — run `--update-schema` to fetch it |
| Multiple files generated for one kind | The kind exists in multiple API groups — each group gets its own file with a suffix |

## Related Pages

- See [Validating Resources Against OpenAPI Schemas](validating-resources.html) for a hands-on guide to enabling and using validation.
- See [Generating New Resource Classes with class-generator](generating-resource-classes.html) for step-by-step class generation instructions.
- See [class-generator CLI Reference](class-generator-cli.html) for all CLI options including `--update-schema`, `--update-schema-for`, `--regenerate-all`, and `--coverage-report`.
- See [Understanding the Resource Class Hierarchy](resource-class-hierarchy.html) to learn how generated classes fit into the `Resource` / `NamespacedResource` inheritance tree.
- See [Resource and NamespacedResource API](resource-api.html) for complete documentation of the `validate()` and `validate_dict()` methods.
- See [Testing Without a Cluster Using the Fake Client](testing-without-cluster.html) for how the fake client uses schema-based status templates.

## Related Pages

- [Validating Resources Against OpenAPI Schemas](validating-resources.html)
- [Generating New Resource Classes with class-generator](generating-resource-classes.html)
- [class-generator CLI Reference](class-generator-cli.html)
- [Understanding the Resource Class Hierarchy](resource-class-hierarchy.html)
- [Resource and NamespacedResource API](resource-api.html)
