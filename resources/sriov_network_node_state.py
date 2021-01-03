import logging

from resources.utils import TimeoutExpiredError, TimeoutSampler

from .resource import NamespacedResource


LOGGER = logging.getLogger(__name__)


class SriovNetworkNodeState(NamespacedResource):
    """
    SriovNetworkNodeState object.
    """

    api_group = NamespacedResource.ApiGroup.SRIOVNETWORK_OPENSHIFT_IO

    def __init__(self, name, namespace, client=None, teardown=True):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )

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
        LOGGER.info(f"Wait for {self.kind} {self.name} status to be {wanted_status}")
        try:
            for sample in TimeoutSampler(
                timeout=timeout, sleep=3, func=lambda: self.instance.status.syncStatus
            ):
                if sample == wanted_status:
                    return
        except TimeoutExpiredError:
            LOGGER.error(
                f"after {timeout} seconds, {self.name} status is {self.instance.status.syncStatus}"
            )
            raise
