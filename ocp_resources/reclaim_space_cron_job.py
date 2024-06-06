from __future__ import annotations
from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReclaimSpaceCronJob(NamespacedResource):
    """
    https://github.com/csi-addons/kubernetes-csi-addons/blob/main/apis/csiaddons/v1alpha1/reclaimspacecronjob_types.go
    """

    api_group = NamespacedResource.ApiGroup.CSIADDONS_OPENSHIFT_IO

    def __init__(
        self,
        schedule: Optional[str] = "",
        job_template: Optional[Dict[str, Any]] = None,
        concurrency_policy: Optional[str] = "",
        successful_jobs_history_limit: Optional[int] = None,
        failed_jobs_history_limit: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            schedule (Optional, str): schedule of the reclaim space cron job
            job_template (Optional, dict): describes the reclaim space job that would be created when a reclaim space cronjob
                would be executed
                Example: https://github.com/csi-addons/kubernetes-csi-addons/blob/main/docs/reclaimspace.md
            concurrency_policy (str, optional): indicates how to treat concurrent execution of a job
            successful_jobs_history_limit (int, optional): number of successful jobs to retain
            failed_jobs_history_limit (int, optional): number of failed jobs to retain start at scheduled time
        """
        super().__init__(
            **kwargs,
        )
        self.job_template = job_template
        self.schedule = schedule
        self.concurrency_policy = concurrency_policy
        self.successful_jobs_history_limit = successful_jobs_history_limit
        self.failed_jobs_history_limit = failed_jobs_history_limit

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not (self.job_template and self.schedule):
                raise MissingRequiredArgumentError(argument="'job_template' and 'schedule'")
            self.res["spec"] = {"jobTemplate": self.job_template, "schedule": self.schedule}
            spec_dict = self.res["spec"]
            if self.successful_jobs_history_limit:
                spec_dict["successfulJobsHistoryLimit"] = self.successful_jobs_history_limit
            if self.failed_jobs_history_limit:
                spec_dict["failedJobsHistoryLimit"] = self.failed_jobs_history_limit
            if self.concurrency_policy:
                spec_dict["concurrencyPolicy"] = self.concurrency_policy
