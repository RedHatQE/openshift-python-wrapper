# Welcome to openshift-python-wrapper contributing guide

Thank you for contributing to our project!  
[Project maintainers](https://github.com/RedHatQE/openshift-python-wrapper/blob/main/OWNERS)

## New contributor guide

To get an overview of the project, read the [README](README.md).

## Issues

### Create a new issue

If you find a problem with the code, [search if an issue already exists](https://github.com/RedHatQE/openshift-python-wrapper/issues).  
If you open a pull request to fix the problem, an issue will ba automatically created.  
If a related issue doesn't exist, you can open a new issue using a relevant [issue form](https://github.com/RedHatQE/openshift-python-wrapper/issues/new/choose).

## Pull requests

To contribute code to the project:

- Fork the project and work on your forked repository
- Before submitting a new pull request, make sure you have `pre-commit` installed

```bash
pre-commit install
```

- When submitting a pull request, make sure to fill all the required, relevant fields for your PR.  
  Make sure the title is descriptive and short.
- If the fix is needed in a released version, once your pull request is merged, cherry-pick it to the relevant branch(s).  
  Add `/cherry-pick <target branch to cherry-pick to>` to the PR comment.

## General

- Add typing to new code; typing is enforced using [mypy](https://mypy-lang.org/)

## Adding a new module (resource)

##### Using generator script

- [class_generator](class_generator/README.md)

##### Manual

A new resource must follow rules:

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

Check [ConfigMap](ocp_resources/configmap.py) and [Backup](ocp_resources/backup.py) for reference.
