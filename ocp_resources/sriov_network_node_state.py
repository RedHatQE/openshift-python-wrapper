from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


class SriovNetworkNodeState(NamespacedResource):
    """
    SriovNetworkNodeState object.
    """

    api_group = NamespacedResource.ApiGroup.SRIOVNETWORK_OPENSHIFT_IO

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

    def wait_for_status_sync(self, wanted_status, timeout=1000):
        self.logger.info(
            f"Wait for {self.kind} {self.name} status to be {wanted_status}"
        )
        try:
            for sample in TimeoutSampler(
                wait_timeout=timeout,
                sleep=3,
                func=lambda: self.instance.status.syncStatus,
            ):
                if sample == wanted_status:
                    return
        except TimeoutExpiredError:
            self.logger.error(
                f"after {timeout} seconds, {self.name} status is {self.instance.status.syncStatus}"
            )
            raise
