# Resource class generator

## prerequisites

- [poetry](https://python-poetry.org/)
- [oc](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/) or [kubectl](https://kubernetes.io/docs/tasks/tools/)
- Kubernetes/Openshift cluster

## Preparation

###### Generate explain file

```bash
oc explain deployment --recursive > deployment.txt # Where deployment can be any KIND in the cluster

```

###### Check if the resource is namespaced or not

```bash
oc api-resources --namespaced | grep -w deployment | wc -l # Where deployment is the same KIND from `oc explain` command

```

- If the output of the above command return 1 the resource is namespaced, otherwise not.

## Usage

###### Install poetry environment

```bash
poetry install
```

###### Call the script

```bash
poetry run python scripts/resource/class_generator.py --file deployment.txt --namespaced --api-link <link to resource API or DOC>
```

- Pass --namespaced only if the resource is a namespaced resource
