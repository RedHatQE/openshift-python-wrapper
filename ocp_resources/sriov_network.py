from ocp_resources.resource import NamespacedResource


class SriovNetwork(NamespacedResource):
    """
    SriovNetwork object.
    """

    api_group = NamespacedResource.ApiGroup.SRIOVNETWORK_OPENSHIFT_IO

    def __init__(
        self,
        name,
        namespace,
        network_namespace,
        client=None,
        resource_name=None,
        vlan=None,
        ipam=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.network_namespace = network_namespace
        self.resource_name = resource_name
        self.vlan = vlan
        self.ipam = ipam

    def to_dict(self):
        res = super().to_dict()
        res["spec"] = {
            "ipam": self.ipam or "{}\n",
            "networkNamespace": self.network_namespace,
            "resourceName": self.resource_name,
        }
        if self.vlan:
            res["spec"]["vlan"] = self.vlan
        return res
