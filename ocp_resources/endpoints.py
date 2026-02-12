from __future__ import annotations

from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource
from ocp_resources.utils.constants import TIMEOUT_4MINUTES


class Endpoints(NamespacedResource):
    """
    Endpoints object. API reference:
    https://docs.openshift.com/container-platform/4.12/rest_api/network_apis/endpoints-v1.html#endpoints-v1
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
        addresses: list[dict[str, Any]] | None = None,
        ports: list[dict[str, Any]] | None = None,
        teardown: bool = True,
        yaml_file: str | None = None,
        delete_timeout: int = TIMEOUT_4MINUTES,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            client (DynamicClient): DynamicClient for api calls
            name (str): Name of the endpoints resource
            namespace (str): Namespace of endpoints resource
            addresses (list): List of ip addresses which offers the related ports that are marked as ready
            ports (list): List of port numbers available on the related ip addresses
            teardown (bool): Indicates if the resource should be torn down at the end
            yaml_file (str): yaml file for the resource.
            delete_timeout (int): timeout associated with delete action
        """
        super().__init__(
            name=name,
            namespace=namespace,
            teardown=teardown,
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
