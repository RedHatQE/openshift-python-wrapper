from .resource import NamespacedResource


class SriovNetworkNodePolicy(NamespacedResource):
    """
    SriovNetworkNodePolicy object.
    """

    api_group = "sriovnetwork.openshift.io"

    def __init__(
        self,
        name,
        policy_namespace,
        pf_names,
        root_devices,
        num_vfs,
        resource_name,
        priority=None,
        mtu=None,
        node_selector=None,
        teardown=True,
    ):
        self.policy_namespace = policy_namespace
        super().__init__(name=name, namespace=policy_namespace, teardown=teardown)
        self.pf_names = pf_names
        self.root_devices = root_devices
        self.num_vfs = num_vfs
        self.priority = priority
        self.resource_name = resource_name
        self.mtu = mtu
        self.node_selector = node_selector

    def to_dict(self):
        res = super().to_dict()
        res["spec"] = {
            "deviceType": "vfio-pci",
            "nicSelector": {
                "pfNames": [self.pf_names],
                "rootDevices": [self.root_devices],
            },
            "numVfs": self.num_vfs,
            "resourceName": self.resource_name,
        }
        if self.mtu:
            res["spec"]["mtu"] = self.mtu
        if self.priority:
            res["spec"]["priority"] = self.priority
        if self.node_selector:
            res["spec"]["nodeSelector"] = self.node_selector
        else:
            res["spec"]["nodeSelector"] = {
                "feature.node.kubernetes.io/network-sriov.capable": "true"
            }
        return res
