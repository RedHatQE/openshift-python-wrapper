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

###### Call the script

- Running in normal mode with `--kind` flags:

```bash
poetry run python scripts/resource/class_generator.py --kind <kind>

```

Run in interactive mode:

```bash
poetry run python scripts/resource/class_generator.py --interactive
```

#### Adding tests

- Add a new test for the provided `kind` by passing `--add-tests` flag
- Replace `Pod` with the kind you want to add to the tests

```bash
poetry run python scripts/resource/class_generator.py --kind Pod --add-tests
```

## Reporting an issue

- Running with debug mode and `--debug` flag:

```bash
poetry run python scripts/resource/class_generator.py --kind <kind> --debug
```

`<kind>-debug.json` will be located under `scripts/resource/debug`
Issue should include:

- The script executed command
- debug file from the above command
- oc/kubectl version
