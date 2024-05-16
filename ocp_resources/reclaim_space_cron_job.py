from __future__ import annotations
from typing import Any, Dict
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReclaimSpaceCronJob(NamespacedResource):
    """
    https://github.com/csi-addons/kubernetes-csi-addons/blob/main/apis/csiaddons/v1alpha1/reclaimspacecronjob_types.go
    """

    api_group = NamespacedResource.ApiGroup.CSIADDONS_OPENSHIFT_IO

    def __init__(
        self,
        schedule: str | None = None,
        job_template: Dict[str, Any] = None,
        concurrency_policy: str | None = None,
        successful_jobs_history_limit: int | None = None,
        failed_jobs_history_limit: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            schedule (str): schedule of the reclaim space cron job
            job_template (dict): describes the reclaim space job that would be created when a reclaim space cronjob
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
            spec_dict = {}
            spec_dict["jobTemplate"] = self.job_template
            spec_dict["schedule"] = self.schedule

            if self.successful_jobs_history_limit:
                spec_dict["successfulJobsHistoryLimit"] = self.successful_jobs_history_limit
            if self.failed_jobs_history_limit:
                spec_dict["failedJobsHistoryLimit"] = self.failed_jobs_history_limit
            if self.concurrency_policy:
                spec_dict["concurrencyPolicy"] = self.concurrency_policy

            self.res.update({"spec": spec_dict})
