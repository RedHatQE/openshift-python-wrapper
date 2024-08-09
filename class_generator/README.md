# Resource class generator

## prerequisites

- [poetry](https://python-poetry.org/)
- [oc](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/) or [kubectl](https://kubernetes.io/docs/tasks/tools/) (latest version)
- Kubernetes/Openshift cluster

## Usage

###### Install poetry environment

```bash
poetry install
```

For shell completion Add this to ~/.bashrc or ~/.zshrc:

```bash
if type class-generator > /dev/null; then eval "$(_CLASS_GENERATOR_COMPLETE=zsh_source class-generator)"; fi
```

###### Call the script

- Calling the script with poetry

```bash
poetry run class-generator --kind <kind>
```

- Running in normal mode with `--kind` flags:

```bash
class-generator --kind <kind>

```

- Review the resource file; make sure that the filename and attribute names are named correctly. For example:
  - `OATH` -> `oath`
  - `CDIConfig` -> `cdi_config`

Run in interactive mode:

```bash
class-generator --interactive
```

#### Adding tests

- Add a new test for the provided `kind` by passing `--add-tests` flag
- Replace `Pod` with the kind you want to add to the tests

```bash
class-generator --kind Pod --add-tests
```

## Reporting an issue

- Running with debug mode and `--debug` flag:

```bash
class-generator --kind <kind> --debug
```

`<kind>-debug.json` will be located under `scripts/resource/debug`
Issue should include:

- The script executed command
- debug file from the above command
- oc/kubectl version
