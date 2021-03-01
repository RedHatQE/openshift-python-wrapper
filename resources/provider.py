import logging

from .resource import NamespacedResource
from .utils import wait_for_mtv_resource_status


LOGGER = logging.getLogger(__name__)


class Provider(NamespacedResource):
    """
    Provider object.
    Used to define A Source Or Destination Provider Such as Vsphere and OCP.
    https://github.com/konveyor/forklift-controller/tree/main/config/crds
    """

    class ProviderTypes:
        VSPHERE = "vsphere"

    class StatusConditions:
        class MESSAGE:
            READY = "The provider is ready."

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name,
        namespace,
        provider_type,
        url,
        secret_name,
        secret_namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.provider_type = provider_type
        self.url = url
        self.secret_name = secret_name
        self.secret_namespace = secret_namespace

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "type": self.provider_type,
                    "url": self.url,
                    "secret": {
                        "name": self.secret_name,
                        "namespace": self.secret_namespace,
                    },
                }
            }
        )

        return res

    def wait_for_ready(self, timeout=600):
        wait_for_mtv_resource_status(
            mtv_resource=self,
            timeout=timeout,
            condition_message=self.StatusConditions.MESSAGE.READY,
            condition_status=NamespacedResource.Condition.Status.TRUE,
            condition_type=NamespacedResource.Condition.READY,
        )
