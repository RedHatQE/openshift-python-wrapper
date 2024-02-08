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
        # TODO: Replace complete_status_str with self.Status.COMPLETE once RHMI `complete` status starts with uppercase
        complete_status_str = "complete"
        self.logger.info(f"Wait for {self.kind} {self.name} stage status to be {complete_status_str}")
        sample = None
        try:
            timeout_watcher = TimeoutWatch(timeout=timeout)
            self.wait(timeout=timeout_watcher.remaining_time())
            timeout_remain = timeout_watcher.remaining_time()

            for sample in TimeoutSampler(
                wait_timeout=timeout_remain,
                sleep=1,
                func=lambda: self.instance.status.stage,
            ):
                if sample == complete_status_str:
                    return

        except TimeoutExpiredError:
            self.logger.error(f"after {timeout} seconds, {self.kind} {self.name} stage status is {sample}")
            raise
