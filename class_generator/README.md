# Resource class generator

## Usage

### Installation

- Using [pipx](https://github.com/pypa/pipx) (recommended)

```bash
 pipx install openshift-python-wrapper
```

- Using `pip`

```bash
python3 -m pip install openshift-python-wrapper
```

- Using [poetry](https://python-poetry.org/) (For development)

```bash
pipx install poetry
poetry install
```

For shell completion Add this to ~/.bashrc or ~/.zshrc:

```bash
if type class-generator > /dev/null; then eval "$(_CLASS_GENERATOR_COMPLETE=zsh_source class-generator)"; fi
```

#### Usage

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

#### Adding tests

- Add a new test for the provided `kind` by passing `--add-tests` flag
- Replace `Pod` with the kind you want to add to the tests

```bash
class-generator --kind Pod --add-tests
```

#### Update schema files

- Dependencies
  - Kubernetes/Openshift cluster
  - [oc](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/) or [kubectl](https://kubernetes.io/docs/tasks/tools/) (latest version)
  - [openapi2jsonschema](https://github.com/instrumenta/openapi2jsonschema)
  - [poetry](https://python-poetry.org/)

```bash
pipx install poetry
pipx install --python python3.9 openapi2jsonschema
```

- Clone this repository

```bash
git clone https://github.com/RedHatQE/openshift-python-wrapper.git
cd openshift-python-wrapper
```

- Install dependencies

```bash
poetry install
```

- Login to the cluster use admin user and password.

```bash
oc login <clster api URL> -u <username> -p <password>
```

- Execute the command:

```bash
poetry run python class_generator/class-generator --update-schema
```
