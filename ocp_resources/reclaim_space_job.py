from __future__ import annotations
from typing import Any, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReclaimSpaceJob(NamespacedResource):
    """
    https://github.com/csi-addons/kubernetes-csi-addons/blob/main/apis/csiaddons/v1alpha1/reclaimspacejob_types.go
    """

    api_group = NamespacedResource.ApiGroup.CSIADDONS_OPENSHIFT_IO

    def __init__(
        self,
        backoff_limit: Optional[int] = None,
        target: Optional[dict[str, Any]] = None,
        retry_deadline_seconds: Optional[int] = None,
        timeout_seconds_reclaim_job: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            backoff_limit (int, Optional): The number of retries for a reclaim space job.
            target (Optional, dict): Volume target on which the operation would be performed.
            retryDeadlineSeconds (int, Optional): Duration in seconds relative to the start time that the
                operation may be retried.
            timeout_seconds_reclaim_job (int, Optional): Specifies the timeout in seconds for the grpc request sent to
                the CSI driver.
        """
        super().__init__(
            **kwargs,
        )
        self.backoff_limit = backoff_limit
        self.target = target
        self.retry_deadline_seconds = retry_deadline_seconds
        self.timeout_seconds_reclaim_job = timeout_seconds_reclaim_job

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.target:
                raise MissingRequiredArgumentError(argument="target")
            self.res["spec"] = {"target": self.target}
            spec_dict = self.res["spec"]
            if self.retry_deadline_seconds:
                spec_dict["retryDeadlineSeconds"] = self.retry_deadline_seconds
            if self.timeout_seconds_reclaim_job:
                spec_dict["timeout"] = self.timeout_seconds_reclaim_job
            if self.backoff_limit:
                spec_dict["backOffLimit"] = self.backoff_limit
