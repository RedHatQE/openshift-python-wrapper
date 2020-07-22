from .resource import NamespacedResource


class SriovNetworkNodeState(NamespacedResource):
    """
    SriovNetworkNodeState object.
    """

    api_group = "sriovnetwork.openshift.io"

    def __init__(self, name, policy_namespace):
        super().__init__(name=name, namespace=policy_namespace)

    @property
    def interfaces(self):
        return self.instance.status.interfaces

    @staticmethod
    def iface_name(iface):
        return iface.name

    @staticmethod
    def pciaddress(iface):
        return iface.pciAddress

    @staticmethod
    def totalvfs(iface):
        return iface.totalvfs
