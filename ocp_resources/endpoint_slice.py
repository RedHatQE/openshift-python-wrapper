from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class EndpointSlice(NamespacedResource):
    """
    EndpointSlice object. API reference:
    https://github.com/kubernetes/metrics/blob/master/pkg/client/clientset/versioned/typed/metrics/v1beta1/podmetrics.go
    """

    api_group = NamespacedResource.ApiGroup.DISCOVERY_K8S_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        address_type=None,
        endpoints=None,
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
            address_type (string): Type of address carried by this endpoint
            endpoints (list): List of unique endpoints in this slice
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
        self.address_type = address_type
        self.endpoints = endpoints
        self.ports = ports

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if not (self.address_type and self.endpoints):
                raise ValueError(
                    "yaml_file or parameters 'address_type' and 'endpoints' are required."
                )
            self.res.update(
                {
                    "addressTypes": self.address_type,
                    "endpoints": self.endpoints,
                    "ports": self.ports,
                }
            )
