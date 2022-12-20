# API reference: https://metallb.universe.tf/apis/#metallb.io/v1beta1.L2Advertisement

from ocp_resources.resource import NamespacedResource


class L2Advertisement(NamespacedResource):
    """
    L2Advertisement object.
    """

    api_group = NamespacedResource.ApiGroup.METALLB_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        interfaces=None,
        ip_address_pools=None,
        ip_address_pools_selectors=None,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the MetalLB or it's CR's.
            namespace (str): Namespace of the MetalLB
            client: (DynamicClient): DynamicClient to use.
            interfaces (list): List of interfaces.
            ip_address_pools (list): The list of IPAddressPools to advertise via this advertisement, selected by name.
            ip_address_pools_selectors (list): A selector for the IPAddressPools which would get advertised
                        via this advertisement.(if nothing mentioned then it will be applied to all the IPAddressPools)
        """
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            **kwargs,
        )
        self.interfaces = interfaces
        self.ip_address_pools = ip_address_pools
        self.ip_address_pools_selectors = ip_address_pools_selectors

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res["spec"] = {}
            if self.interfaces:
                self.res["spec"]["interfaces"] = self.interfaces

            if self.ip_address_pools:
                self.res["spec"]["ipAddressPools"] = self.ip_address_pools

            if self.ip_address_pools_selectors:
                self.res["spec"][
                    "ipAddressPoolSelectors"
                ] = self.ip_address_pools_selectors
