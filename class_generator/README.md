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

- Running in normal mode with `--kind` flags:
  - `--kind` can process multiple kinds at the same command, pass `--kind <kind1>,<kind2>,<kind3>`

```bash
class-generator --kind <kind>

```

- Review the resource file; make sure that the filename and attribute names are named correctly. For example:
  - `OATH` -> `oath`
  - `CDIConfig` -> `cdi_config`

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
  - [openapi2jsonschema](https://github.com/instrumenta/openapi2jsonschema)
  - [uv](https://github.com/astral-sh/uv)

```bash
uv tool install --python python3.9 openapi2jsonschema
```

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
