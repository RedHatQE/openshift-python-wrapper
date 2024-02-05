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
            timeout (int): Time in seconds to wait for stage status.

        Raises:
            TimeoutExpiredError: If stage status is not complete.

        """
        self.logger.info(f"Wait for {self.kind} {self.name} stage status to be {self.Status.COMPLETE}")
        sample = None
        try:
            timeout_watcher = TimeoutWatch(timeout=timeout)
            timeout_remain = timeout_watcher.remaining_time()
            self.wait(timeout=timeout_remain)

            for sample in TimeoutSampler(
                wait_timeout=timeout_remain,
                sleep=1,
                func=lambda: self.instance.status.stage,
            ):
                if sample == self.Status.COMPLETE:
                    return

        except TimeoutExpiredError:
            self.logger.error(f"after {timeout} seconds, {self.kind} {self.name} stage status is {sample}")
            raise
