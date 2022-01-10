from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class Host(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) Host resource.
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        host_id=None,
        ip_address=None,
        provider_name=None,
        provider_namespace=None,
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
        self.host_id = host_id
        self.ip_address = ip_address
        self.provider_name = provider_name
        self.provider_namespace = provider_namespace
        self.secret_name = secret_name or f"{self.name}-secret"
        self.secret_namespace = secret_namespace or self.namespace
        self.condition_message_ready = self.ConditionMessage.HOST_READY

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res.update(
            {
                "spec": {
                    "id": self.host_id,
                    "ipAddress": self.ip_address,
                    "secret": {
                        "name": self.secret_name,
                        "namespace": self.secret_namespace,
                    },
                    "provider": {
                        "name": self.provider_name,
                        "namespace": self.provider_namespace,
                    },
                }
            }
        )

        return res
