from ocp_resources.resource import NamespacedResource
from timeout_sampler import TimeoutExpiredError, TimeoutSampler, TimeoutWatch


class RHMI(NamespacedResource):
    """
    RHMI custom resource created by Red Hat Openshift API Management (RHOAM)
    https://github.com/integr8ly/integreatly-operator/blob/master/apis/v1alpha1/rhmi_types.go
    """

    api_group = NamespacedResource.ApiGroup.INTEGREATLY_ORG

    def wait_for_stage_status_complete(self, timeout):
        """
        Wait until RHMI stage status is complete.

        Args:
            timeout (int): Time in seconds to wait for installation status.

        Raises:
            TimeoutExpiredError: If stage status is not complete.

        """
        self.logger.info(f"Wait for {self.kind} {self.name} stage status to be {RHMI.Status.COMPLETE}")
        sample = None
        try:
            timeout_watcher = TimeoutWatch(timeout=timeout)
            self.wait(timeout=timeout_watcher.remaining_time())

            for sample in TimeoutSampler(
                wait_timeout=timeout_watcher.remaining_time(),
                sleep=1,
                func=lambda: self.instance.status.stage,
            ):
                if sample == RHMI.Status.COMPLETE:
                    return

        except TimeoutExpiredError:
            self.logger.error(f"after {timeout} seconds, {self.kind} {self.name} stage status is {sample}")
            raise
