from __future__ import annotations
from typing import Any
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReclaimSpaceJob(NamespacedResource):
    """
    https://github.com/csi-addons/kubernetes-csi-addons/blob/main/apis/csiaddons/v1alpha1/reclaimspacejob_types.go
    """

    api_group = NamespacedResource.ApiGroup.CSIADDONS_OPENSHIFT_IO

    def __init__(
        self,
        backoff_limit: int | None = None,
        target: dict[str, Any] = None,
        retry_deadline_seconds: int | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
         Args:
        backoff_limit (int, Optional): The number of retries for a reclaim space job.
        target (dict): Volume target on which the operation would be performed.
        retryDeadlineSeconds (int, Optional): Optional. Duration in seconds relative to the start time that the
            operation may beretried.
        timeout (int, Optional): specifies the timeout in seconds for the grpc request sent to the CSI driver
        """
        super().__init__(**kwargs)
        self.backoff_limit = backoff_limit
        self.target = target
        self.retry_deadline_seconds = retry_deadline_seconds
        self.timeout = timeout

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.target:
                raise MissingRequiredArgumentError(argument="target")
            spec_dict = {}
            spec_dict["target"] = self.target
            if self.retry_deadline_seconds:
                spec_dict["retryDeadlineSeconds"] = self.retry_deadline_seconds
            if self.timeout:
                spec_dict["timeout"] = self.timeout
            if self.backoff_limit:
                spec_dict["backOffLimit"] = self.backoff_limit

            self.res.update({"spec": spec_dict})
