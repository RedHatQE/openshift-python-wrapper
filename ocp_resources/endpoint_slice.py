from __future__ import annotations

from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource
from ocp_resources.utils.constants import TIMEOUT_4MINUTES


class EndpointSlice(NamespacedResource):
    """
    EndpointSlice object. API reference:
    https://kubernetes.io/docs/reference/kubernetes-api/service-resources/endpoint-slice-v1/
    """

    api_group = NamespacedResource.ApiGroup.DISCOVERY_K8S_IO

    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
        address_type: str | None = None,
        endpoints: list[dict[str, Any]] | None = None,
        ports: list[dict[str, Any]] | None = None,
        teardown: bool = True,
        yaml_file: str | None = None,
        delete_timeout: int = TIMEOUT_4MINUTES,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            client (DynamicClient): DynamicClient for api calls
            name (str): Name of the EndpointSlice resource
            namespace (str): Namespace of EndpointSlice resource
            address_type (string): Type of address carried by this endpoint
            endpoints (list): List of unique endpoints in this slice
            ports (list, optional): List of port numbers available on the related ip addresses
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
        self.address_type = address_type
        self.endpoints = endpoints
        self.ports = ports

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not (self.address_type and self.endpoints):
                raise MissingRequiredArgumentError(argument="'address_type' and 'endpoints'")

            self.res.update({
                "addressTypes": self.address_type,
                "endpoints": self.endpoints,
            })
            if self.ports:
                self.res["ports"] = self.ports
