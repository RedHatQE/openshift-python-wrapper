from ocp_resources.resource import NamespacedResource
from timeout_sampler import TimeoutExpiredError, TimeoutSampler, TimeoutWatch


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
        self.logger.info(f"Wait for {self.kind} {self.name} status to be {wanted_status}")
        try:
            timeout_watcher = TimeoutWatch(timeout=timeout)
            for sample in TimeoutSampler(
                wait_timeout=timeout,
                sleep=1,
                func=lambda: self.exists,
            ):
                if sample:
                    break

            for sample in TimeoutSampler(
                wait_timeout=timeout_watcher.remaining_time(),
                sleep=3,
                func=lambda: self.instance.status.syncStatus,
            ):
                if sample == wanted_status:
                    return
        except TimeoutExpiredError:
            self.logger.error(f"after {timeout} seconds, {self.name} status is" f" {self.instance.status.syncStatus}")
            raise
