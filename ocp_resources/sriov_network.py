from ocp_resources.resource import NamespacedResource


class SriovNetwork(NamespacedResource):
    """
    SriovNetwork object.
    """

    api_group = NamespacedResource.ApiGroup.SRIOVNETWORK_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        network_namespace=None,
        client=None,
        resource_name=None,
        vlan=None,
        ipam=None,
        teardown=True,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.network_namespace = network_namespace
        self.resource_name = resource_name
        self.vlan = vlan
        self.ipam = ipam

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res["spec"] = {
            "ipam": self.ipam or "{}\n",
            "networkNamespace": self.network_namespace,
            "resourceName": self.resource_name,
        }
        if self.vlan:
            res["spec"]["vlan"] = self.vlan
        return res
