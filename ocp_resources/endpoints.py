from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class Endpoints(NamespacedResource):
    """
    Endpoints object. API reference:
    https://docs.openshift.com/container-platform/4.12/rest_api/network_apis/endpoints-v1.html#endpoints-v1
    """

    api_version = "v1"

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        addresses=None,
        ports=None,
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
        self.addresses = addresses
        self.ports = ports

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "subsets": {
                        "addresses": self.addresses,
                        "ports": self.ports,
                    }
                }
            )
