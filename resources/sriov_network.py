from .resource import NamespacedResource


class SriovNetwork(NamespacedResource):
    """
    SriovNetwork object.
    """

    api_group = "sriovnetwork.openshift.io"

    def __init__(
        self,
        name,
        policy_namespace,
        network_namespace,
        resource_name=None,
        vlan=None,
        ipam=None,
        teardown=True,
    ):
        self.policy_namespace = policy_namespace
        super().__init__(name=name, namespace=policy_namespace, teardown=teardown)
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
