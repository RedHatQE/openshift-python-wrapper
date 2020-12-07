from .resource import NamespacedResource


class SriovNetworkNodeState(NamespacedResource):
    """
    SriovNetworkNodeState object.
    """

    api_group = NamespacedResource.ApiGroup.SRIOVNETWORK_OPENSHIFT_IO

    def __init__(self, name, policy_namespace, client=None):
        super().__init__(name=name, namespace=policy_namespace, client=client)

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
