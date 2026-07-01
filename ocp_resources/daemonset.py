from datetime import datetime, timezone

import kubernetes
from timeout_sampler import TimeoutSampler

from ocp_resources.resource import NamespacedResource
from ocp_resources.utils.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES


class DaemonSet(NamespacedResource):
    """
    DaemonSet object.
    """

    api_group = NamespacedResource.ApiGroup.APPS

    def wait_until_deployed(self, timeout=TIMEOUT_4MINUTES):
        """
        Wait until all Pods are deployed and ready.

        Args:
            timeout (int): Time to wait for the Daemonset.

        Raises:
            TimeoutExpiredError: If not all the pods are deployed.
        """
        self.logger.info(f"Wait for {self.kind} {self.name} to deploy all desired pods")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.api.get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        for sample in samples:
            if sample.items:
                status = sample.items[0].status
                desired_number_scheduled = status.desiredNumberScheduled
                number_ready = status.numberReady
                if desired_number_scheduled > 0 and desired_number_scheduled == number_ready:
                    return

    def restart(self) -> None:
        """
        Restart the DaemonSet by patching the pod template with a restartedAt annotation.
        """
        self.logger.info(f"Restarting {self.kind} {self.name}")
        self.update(
            resource_dict={
                "metadata": {"name": self.name},
                "spec": {
                    "template": {
                        "metadata": {
                            "annotations": {
                                "kubectl.kubernetes.io/restartedAt": datetime.now(tz=timezone.utc).isoformat()
                            }
                        }
                    }
                },
            }
        )

    def wait_for_rollout(self, timeout: int = TIMEOUT_4MINUTES) -> None:
        """
        Wait until the DaemonSet rollout is complete.

        Checks that the controller has observed the latest generation, all pods have been
        updated, and all updated pods are available.

        Args:
            timeout (int): Time to wait for the rollout to complete.

        Raises:
            TimeoutExpiredError: If the rollout does not complete within the timeout.
        """
        self.logger.info(f"Wait for {self.kind} {self.name} rollout to complete")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.api.get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        for sample in samples:
            if sample.items:
                item = sample.items[0]
                status = item.status
                if not status:
                    continue

                desired_number_scheduled = status.desiredNumberScheduled or 0
                if desired_number_scheduled == 0 and status.observedGeneration == item.metadata.generation:
                    return

                if (
                    desired_number_scheduled > 0
                    and status.observedGeneration == item.metadata.generation
                    and (status.updatedNumberScheduled or 0) == desired_number_scheduled
                    and (status.numberAvailable or 0) == desired_number_scheduled
                ):
                    return

    def delete(self, wait=False, timeout=TIMEOUT_4MINUTES, _body=None):
        """
        Delete Daemonset

        Args:
            wait (bool): True to wait for Daemonset to be deleted.
            timeout (int): Time to wait for resource deletion
            _body (dict): Content to send for delete()

        Returns:
            bool: True if delete succeeded, False otherwise.
        """
        return super().delete(
            wait=wait,
            timeout=timeout,
            body=kubernetes.client.V1DeleteOptions(propagation_policy="Foreground"),
        )
