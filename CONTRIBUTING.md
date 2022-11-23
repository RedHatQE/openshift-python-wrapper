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
Add `!cherry-pick <target branch to cherry-pick to>` to the PR comment.

## Adding a new module (resource)
To support working with a new (or missing) resource:
- Add a new file under `ocp_resources`, names as the resource.  
If the resource name is composed of multiple words, separate them with an underscore.  
For example: `ImageStream` filename is `image_stream.py`
- Create a class named as the resource kind.  
For example: `ImageStream` -> `class ImageStream`
- Inherit from the relevant class.  
If the resource is cluster-scoped, inherit from `Resource` else from `NamespacedResource`.  
For example: `class ImageStream(NamespacedResource):`
- Add the resource's apiGroup (`apiVersion` prefix) as `api_group`.
For example: `image.openshift.io`
- Add a link to the resource's API reference.  
For example: [ImageStream API reference](https://docs.openshift.com/container-platform/4.11/rest_api/image_apis/imagestream-image-openshift-io-v1.html#imagestream-image-openshift-io-v1)
- Add an `__init__` function.  
Define all the required arguments that are **required** to instantiate a new resource.  
Optional parameters may be added as well.  
For example:
```
    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        lookup_policy=False,
        tags=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.tags = tags
        self.lookup_policy = lookup_policy
```
- Use `to_dict` to set the values in the resource body. Make sure you call `super().to_dict()` first.  
For example:
```
    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "lookupPolicy": {"local": self.lookup_policy},
                        "tags": self.tags,
                    }
                }
            )
```
- Check [imageStreams](ocp_resources/image_stream.py) for reference.
