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

- Running in normal mode with `--kind` and `--api-link` flags:

```bash
poetry run python scripts/resource/class_generator.py --kind <kind> --api-link <link to resource API or DOC>

```

Run in interactive mode:

```bash
poetry run python scripts/resource/class_generator.py --interactive
```

#### Adding tests

- Generate the resource file the debug file by adding `--debug` flag
- Replace `Pod` with the kind you want to test
- `--api-link` must be `https://debug.explain`

```bash
poetry run python scripts/resource/class_generator.py --api-link https://debug.explain --kind Pod --output-file /tmp/pod_res.py --debug
```

- Move the resource file under [tests manifests dir](scripts/resource/tests/manifests/)

```bash
mv /tmp/pod_res.py scripts/resource/tests/manifests/
```

- Move the debug file under [tests manifests dir](scripts/resource/tests/manifests/)
```bash
mv scripts/resource/debug/Pod_debug.json scripts/resource/tests/manifests/
```

## Reporting an issue

- Running with debug mode and `--debug` flag:

```bash
poetry run python scripts/resource/class_generator.py --kind <kind> --api-link <link to resource API or DOC> --debug
```

`<kind>-debug.json` will be located under `scripts/resource/debug`
Issue should include:

- The script executed command
- debug file from the above command
- oc/kubectl version
