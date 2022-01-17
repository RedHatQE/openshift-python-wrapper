from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class Provider(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) Provider object.
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        provider_type=None,
        url=None,
        secret_name=None,
        secret_namespace=None,
        client=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.provider_type = provider_type
        self.url = url
        self.secret_name = secret_name
        self.secret_namespace = secret_namespace
        self.condition_message_ready = self.ConditionMessage.PROVIDER_READY

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

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
