from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class Endpoints(NamespacedResource):
    """
    Endpoints object. API reference:
    https://docs.openshift.com/container-platform/4.12/rest_api/network_apis/endpoints-v1.html#endpoints-v1
    """

    api_version = NamespacedResource.ApiVersion.V1

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
        """
        Args:
            name (str): Name of the endpoints resource
            namespace (str): Namespace of endpoints resource
            client: (DynamicClient): DynamicClient for api calls
            addresses (list): List of ip addresses which offers the related ports that are marked as ready
            ports (list): List of port numbers available on the related ip addresses
            teardown (bool): Indicates if the resource should be torn down at the end
            privileged_client (DynamicClient): Privileged client for api calls
            yaml_file (str): yaml file for the resource.
            delete_timeout (int): timeout associated with delete action
        """
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

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not (self.addresses and self.ports):
                raise MissingRequiredArgumentError(argument="'addresses' and 'ports")

            self.res.update({
                "subsets": {
                    "addresses": self.addresses,
                    "ports": self.ports,
                }
            })
