# Resource class generator

Utility to add a python module with class resources to openshift-python-wrapper based on `kind`

Some resources have the same kind, in this case the script will create two files.
For example `DNS` kind have two CRDs, one from `config.openshift.io` and one from `operator.openshift.io`
The output will be:

- dns_operator_openshift_io.py
- dns_config_openshift_io.py

## Installation

Install [uv](https://github.com/astral-sh/uv)

```bash
 uv tool install openshift-python-wrapper
```

- Using `pip`

```bash
python3 -m pip install openshift-python-wrapper
```

For shell completion Add this to ~/.bashrc or ~/.zshrc:

```bash
if type class-generator > /dev/null; then eval "$(_CLASS_GENERATOR_COMPLETE=zsh_source class-generator)"; fi
```

## Usage

- All available options:

```bash
class-generator --help
```

### Generating classes for specific resources

- Running in normal mode with `--kind` flags:
  - `--kind` can process multiple kinds at the same command, pass `--kind <kind1>,<kind2>,<kind3>`

```bash
class-generator --kind <kind>
```

- Review the resource file; make sure that the filename and attribute names are named correctly. For example:
  - `OATH` -> `oath`
  - `CDIConfig` -> `cdi_config`

### Discovering missing resources

The class-generator can automatically discover resources in your cluster that don't have wrapper classes yet. Resource discovery runs in parallel for improved performance, typically reducing discovery time by 3-5x compared to sequential discovery.

- Discover missing resources and generate a coverage report:

```bash
class-generator --discover-missing
```

- Generate JSON output for CI/CD integration:

```bash
class-generator --discover-missing --json
```

- Disable caching to force fresh discovery:

```bash
class-generator --discover-missing --no-cache
```

Discovery results are cached for 24 hours in `~/.cache/openshift-python-wrapper/` to improve performance.

### Coverage Report Options

The coverage report provides detailed information about resource implementation status:

- **Total Discovered Resources**: All resources found in the cluster (including CRDs)
- **Total Implemented**: Number of Python wrapper classes in `ocp_resources/`
- **Covered Resources**: Resources that have corresponding wrapper classes
- **Total Missing**: Resources without wrapper implementations
- **Coverage Percentage**: Percentage of discovered resources that have implementations

Resources are prioritized as:
- **CORE**: Essential Kubernetes resources (v1 API group)
- **HIGH**: Common workload resources (apps/v1, batch/v1)
- **MEDIUM**: Platform-specific resources (OpenShift, operators)
- **LOW**: Custom resources and less common APIs

### Example output

```text
Resource Coverage Report

╭─────────────────────────── Coverage Statistics ────────────────────────────╮
│ Total Discovered Resources: 397                                             │
│ Total Implemented: 197                                                      │
│ Covered Resources: 172                                                      │
│ Total Missing: 225                                                          │
│ Coverage Percentage: 43.32%                                                 │
╰─────────────────────────────────────────────────────────────────────────────╯

Missing Resources (sorted by priority)

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Priority   ┃ Kind                          ┃ API Version                   ┃ Namespaced ┃ Command                                         ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ CORE       │ Binding                       │ v1                            │ Yes        │ class-generator -k Binding                      │
│ CORE       │ ComponentStatus               │ v1                            │ No         │ class-generator -k ComponentStatus              │
│ HIGH       │ ControllerRevision            │ apps/v1                       │ Yes        │ class-generator -k ControllerRevision           │
│ HIGH       │ PodTemplate                   │ v1                            │ Yes        │ class-generator -k PodTemplate                  │
│ MEDIUM     │ ClusterResourceQuota          │ quota.openshift.io/v1         │ No         │ class-generator -k ClusterResourceQuota         │
└────────────┴───────────────────────────────┴───────────────────────────────┴────────────┴─────────────────────────────────────────────────┘

Tip: You can generate multiple resources at once:

  class-generator -k Binding,ComponentStatus,ControllerRevision
```

### Caching

Discovery results are cached for 24 hours to improve performance. Cache location: `~/.cache/openshift-python-wrapper/discovery_cache.json`

## Adding tests

- Add a new test for the provided `kind` by passing `--add-tests` flag
- Replace `Pod` with the kind you want to add to the tests

```bash
class-generator --kind Pod --add-tests
```

## Update schema files

- Dependencies
  - Kubernetes/Openshift cluster
  - [oc](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/) or [kubectl](https://kubernetes.io/docs/tasks/tools/) (latest version)
  - [uv](https://github.com/astral-sh/uv)

- Clone this repository

```bash
git clone https://github.com/RedHatQE/openshift-python-wrapper.git
cd openshift-python-wrapper
```

- Login to the cluster use admin user and password.

```bash
oc login <clster api URL> -u <username> -p <password>
```

- Execute the command:

```bash
class-generator --update-schema
```

The schema update process:
- Fetches schemas directly from the OpenAPI v3 endpoint
- Runs in parallel for improved performance
- Stores schemas in `class_generator/schema/__resources-mappings.json` and `class_generator/schema/_definitions.json`

## Version Selection

When multiple API versions exist for the same resource within an API group, the class generator automatically selects the latest stable version according to this precedence:

`v2` > `v1` > `v1beta2` > `v1beta1` > `v1alpha2` > `v1alpha1`

For example:
- If both `v1` and `v1beta1` exist, `v1` will be used
- Resources from different API groups are treated as separate resources

## Python Keyword Handling

Fields that conflict with Python reserved keywords are automatically renamed by appending an underscore. The original field name is preserved in the API calls.

Example:
- CRD field `finally` → Python parameter `finally_`
- The generated `to_dict()` method correctly maps back to `finally` for API operations
