# API reference: https://metallb.universe.tf/apis/#metallb.io/v1beta1.IPAddressPool

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class IPAddressPool(NamespacedResource):
    """
    IPAddressPool object.
    """

    api_group = NamespacedResource.ApiGroup.METALLB_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        addresses=None,
        auto_assign=True,
        avoid_buggy_ips=False,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the MetalLB or it's CR's.
            namespace (str): Namespace of the MetalLB
            client: (DynamicClient): DynamicClient to use.
            addresses (list): List of IP addresses.
            auto_assign (bool): IP address assignment. (default: True)
            avoid_buggy_ips (bool): Avoid buggy IP address (default: False)
        """
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            **kwargs,
        )
        self.addresses = addresses
        self.auto_assign = auto_assign
        self.avoid_buggy_ips = avoid_buggy_ips

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.addresses:
                raise MissingRequiredArgumentError(argument="addresses")

            self.res["spec"] = {"addresses": self.addresses}

            if self.auto_assign:
                self.res["spec"]["autoAssign"] = self.auto_assign

            if self.avoid_buggy_ips:
                self.res["spec"]["avoidBuggyIPs"] = self.avoid_buggy_ips
