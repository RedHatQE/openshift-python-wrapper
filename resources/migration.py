import logging

from .resource import NamespacedResource


LOGGER = logging.getLogger(__name__)


class Migration(NamespacedResource):
    """
    Migration object.
    """

    api_version = f"{NamespacedResource.ApiGroup.VIRT_KONVEYOR_IO}/{NamespacedResource.ApiVersion.V1ALPHA1}"

    def __init__(
        self, name, namespace, type, url, secret_name, secret_namespace, teardown=True
    ):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.type = type
        self.url = url
        self.secret_name = secret_name
        self.secret_namespace = secret_namespace

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "plan": {
                        "name": self.secret_name,
                        "namespace": self.secret_namespace,
                    },
                }
            }
        )
        return res
