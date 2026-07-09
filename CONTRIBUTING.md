# Welcome to openshift-python-wrapper contributing guide

Thank you for contributing to our project!  
[Project maintainers](https://github.com/RedHatQE/openshift-python-wrapper/blob/main/OWNERS)

## New contributor guide

To get an overview of the project, read the [README](README.md).

## Issues

### Create a new issue

If you find a problem with the code, [search if an issue already exists](https://github.com/RedHatQE/openshift-python-wrapper/issues).  
If you open a pull request to fix the problem, an issue will be automatically created.  
If a related issue doesn't exist, you can open a new issue using a relevant [issue form](https://github.com/RedHatQE/openshift-python-wrapper/issues/new/choose).

## Pull requests

To contribute code to the project:

- Fork the project and work on your forked repository
- Before submitting a new pull request, make sure you have `prek` installed

```bash
prek install
```

- When submitting a pull request, make sure to fill all the required, relevant fields for your PR.  
  Make sure the title is descriptive and short.
- If the fix is needed in a released version, once your pull request is merged, cherry-pick it to the relevant branch(s).  
  Add `/cherry-pick <target branch to cherry-pick to>` to the PR comment.

## General

- Add typing to new code; typing is enforced using [mypy](https://mypy-lang.org/)

## Adding a new module (resource)

##### Using generator script (REQUIRED)

New resources MUST be added via the class generator — manual creation is not allowed.

- [class_generator](class_generator/README.md)

##### Manual code (below `# End of generated code` only)

Custom helper methods can be added below the end marker. The generated class structure must follow these rules:

- A new file named as the resource under `ocp_resources`; If the resource name is composed of multiple words, separate them with an underscore.
- A class named as the resource kind.
- Inherit from the relevant class; If the resource is cluster-scoped, inherit from `Resource` else from `NamespacedResource`.
- API group:
  - Under `ocp_resources.resource.Resource.ApiGroup`
  - Resource's apiGroup (`apiVersion` prefix) as `api_group`
- A link to the resource's API reference.
- Implement `__init__` function;  
  Define all the required arguments that are **required** to instantiate the new resource. Optional parameters may be added as well.
- Implement `to_dict` function.

Check [ConfigMap](ocp_resources/config_map.py) and [Backup](ocp_resources/backup.py) for reference.

### Generated code markers

Resource files created by `class-generator` use markers to separate generated from manual code:

- **Start marker** (line 1): `# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md`
- **End marker** (inside class): `# End of generated code`

Code between these markers is **auto-generated and must NOT be modified manually**.
To update generated code, use `class-generator --kind <Kind> --overwrite --backup`.
Custom code (helper methods, overrides) goes **below** the `# End of generated code` marker.

### No client-side validation on resource creation

When building resource payloads (`to_dict()`), do NOT validate or block at code level (e.g., mutual exclusivity of fields).
If a payload can be sent to the API, send it — let the Kubernetes/OpenShift API server return the error.
Helper functions in resource classes (e.g., `wait_for_rollout()`, `restart()`) CAN perform validation and guarding as needed.
