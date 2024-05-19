from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class ImageStream(NamespacedResource):
    """
    ImageStream object. API reference:
    https://docs.openshift.com/container-platform/4.11/rest_api/image_apis/imagestream-image-openshift-io-v1.html#imagestream-image-openshift-io-v1
    """

    api_group = NamespacedResource.ApiGroup.IMAGE_OPENSHIFT_IO

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

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            self.res.update({
                "spec": {
                    "lookupPolicy": {"local": self.lookup_policy},
                    "tags": self.tags,
                }
            })
