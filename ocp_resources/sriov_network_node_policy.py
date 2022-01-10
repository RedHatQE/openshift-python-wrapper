from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class SriovNetworkNodePolicy(NamespacedResource):
    """
    SriovNetworkNodePolicy object.
    """

    api_group = NamespacedResource.ApiGroup.SRIOVNETWORK_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        pf_names=None,
        root_devices=None,
        num_vfs=None,
        resource_name=None,
        client=None,
        priority=None,
        mtu=None,
        node_selector=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.pf_names = pf_names
        self.root_devices = root_devices
        self.num_vfs = num_vfs
        self.priority = priority
        self.resource_name = resource_name
        self.mtu = mtu
        self.node_selector = node_selector

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

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
