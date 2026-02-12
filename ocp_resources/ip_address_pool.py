# API reference: https://metallb.universe.tf/apis/#metallb.io/v1beta1.IPAddressPool
from __future__ import annotations

from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class IPAddressPool(NamespacedResource):
    """
    IPAddressPool object.
    """

    api_group = NamespacedResource.ApiGroup.METALLB_IO

    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
        addresses: list[str] | None = None,
        auto_assign: bool = True,
        avoid_buggy_ips: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            name (str): Name of the MetalLB or it's CR's.
            namespace (str): Namespace of the MetalLB
            addresses (list): List of IP addresses.
            auto_assign (bool): IP address assignment. (default: True)
            avoid_buggy_ips (bool): Avoid buggy IP address (default: False)
        """
        super().__init__(
            name=name,
            namespace=namespace,
            **kwargs,
        )
        self.addresses = addresses
        self.auto_assign = auto_assign
        self.avoid_buggy_ips = avoid_buggy_ips

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.addresses:
                raise MissingRequiredArgumentError(argument="addresses")

            self.res["spec"] = {"addresses": self.addresses}

            if self.auto_assign:
                self.res["spec"]["autoAssign"] = self.auto_assign

            if self.avoid_buggy_ips:
                self.res["spec"]["avoidBuggyIPs"] = self.avoid_buggy_ips
