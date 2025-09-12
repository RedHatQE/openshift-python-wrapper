# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any

from timeout_sampler import TimeoutExpiredError, TimeoutSampler

from ocp_resources.resource import NamespacedResource


class BGPSessionState(NamespacedResource):
    """
    BGPSessionState exposes the status of a BGP Session from the FRR instance running on the node.
    """

    api_group: str = NamespacedResource.ApiGroup.FRRK8S_METALLB_IO

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    # End of generated code

    def wait_for_session_established(self, timeout: int = 300, sleep: int = 5) -> None:
        """Waits until the BGP session status is 'Established'.

        Args:
            timeout (int): Maximum time to wait for the BGP session to be established, in seconds.
            sleep (int): Time to wait between status checks, in seconds.

        Raises:
            TimeoutExpiredError: If the BGP session does not reach 'Established' status within the timeout period.
        """
        bgp_status = None
        try:
            for sample in TimeoutSampler(wait_timeout=timeout, sleep=sleep, func=lambda: self.instance):
                if sample:
                    bgp_status = sample.get("status", {}).get("bgpStatus")
                    if bgp_status == self.Status.ESTABLISHED:
                        self.logger.info(f"{self.kind} {self.name} bgpStatus is now Established")
                        return
        except TimeoutExpiredError:
            self.logger.error(
                f"{self.kind} {self.name} did not reach bgpStatus=Established within {timeout}s. "
                f"Last bgpStatus: {bgp_status}"
            )
            raise
