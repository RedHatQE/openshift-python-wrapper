from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class ImageStream(NamespacedResource):
    """
    ImageStream object.
    """

    api_group = NamespacedResource.ApiGroup.IMAGE_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        image_repository=None,
        scheduled=None,
        lookup_policy=False,
        tag=None,
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
        self.image_repository = image_repository
        self.scheduled = scheduled
        self.tag = tag
        self.lookup_policy = lookup_policy

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res
        res.update(
            {
                "spec": {
                    "lookupPolicy": {"local": self.lookup_policy},
                    "tags": {
                        "from": {"kind": "DockerImage", "name": self.image_repository},
                        "name": self.tag,
                        "referencePolicy": {"type": "Source"},
                    },
                }
            }
        )
        if self.scheduled:
            res["spec"]["tags"]["importPolicy"] = self.scheduled
        return res
