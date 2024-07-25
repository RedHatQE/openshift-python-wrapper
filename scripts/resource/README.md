# Resource class generator

## prerequisites

- [poetry](https://python-poetry.org/)
- [oc](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/) or [kubectl](https://kubernetes.io/docs/tasks/tools/)
- Kubernetes/Openshift cluster

## Usage

###### Install poetry environment

```bash
poetry install
```

###### Call the script

```bash
poetry run python scripts/resource/class_generator.py --kind <kind> --api-link <link to resource API or DOC>

```

Run in interactive mode:

```bash
poetry run python scripts/resource/class_generator.py --interactive
```
