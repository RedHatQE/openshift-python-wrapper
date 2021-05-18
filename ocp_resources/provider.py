from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class Provider(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) Provider object.
    """

    class StatusConditions:
        class CATEGORY:
            REQUIRED = "Required"

        class MESSAGE:
            READY = "The provider is ready."

    class ProviderType:
        VSPHERE = "vsphere"

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name,
        namespace,
        provider_type=None,
        url=None,
        secret_name=None,
        secret_namespace=None,
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
        res = super().to_dict()
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

    def wait_for_condition_ready(self):
        self.wait_for_resource_status(
            condition_message=Provider.StatusConditions.MESSAGE.READY,
            condition_status=NamespacedResource.Condition.Status.TRUE,
            condition_type=NamespacedResource.Condition.READY,
        )
