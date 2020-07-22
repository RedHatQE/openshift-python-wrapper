import logging

import kubernetes
from openshift.dynamic.exceptions import NotFoundError
from resources.utils import TimeoutSampler
from urllib3.exceptions import ProtocolError

from .resource import TIMEOUT, NamespacedResource


LOGGER = logging.getLogger(__name__)


class DaemonSet(NamespacedResource):
    """
    DaemonSet object.
    """

    api_group = "apps"

    def wait_until_deployed(self, timeout=TIMEOUT):
        """
        Wait until all Pods are deployed and ready.

        Args:
            timeout (int): Time to wait for the Daemonset.

        Raises:
            TimeoutExpiredError: If not all the pods are deployed.
        """
        LOGGER.info(f"Wait for {self.kind} {self.name} to deploy all desired pods")
        samples = TimeoutSampler(
            timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        for sample in samples:
            if sample.items:
                status = sample.items[0].status
                desired_number_scheduled = status.desiredNumberScheduled
                number_ready = status.numberReady
                if (
                    desired_number_scheduled > 0
                    and desired_number_scheduled == number_ready
                ):
                    return

    def delete(self, wait=False):
        """
        Delete Daemonset

        Args:
            wait (bool): True to wait for Daemonset to be deleted.

        Returns:
            bool: True if delete succeeded, False otherwise.
        """
        try:
            res = self.api().delete(
                name=self.name,
                namespace=self.namespace,
                body=kubernetes.client.V1DeleteOptions(propagation_policy="Foreground"),
            )
        except NotFoundError:
            return False

        LOGGER.info(f"Delete {self.name}")
        if wait and res:
            return self.wait_deleted()
        return res
