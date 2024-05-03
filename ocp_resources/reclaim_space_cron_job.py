from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReclaimSpaceCronJob(NamespacedResource):
    """
    https://github.com/csi-addons/kubernetes-csi-addons/blob/main/docs/reclaimspace.md
    """

    api_group = NamespacedResource.ApiGroup.CSIADDONS_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        schedule=None,
        job_template=None,
        concurrency_policy=None,
        successful_jobs_history_limit=None,
        failed_jobs_history_limit=None,
        **kwargs,
    ):
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
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.job_template = job_template
        self.schedule = schedule
        self.concurrency_policy = concurrency_policy
        self.successful_jobs_history_limit = successful_jobs_history_limit
        self.failed_jobs_history_limit = failed_jobs_history_limit

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if not (self.job_template and self.schedule):
                raise MissingRequiredArgumentError(argument="'job_template' and 'schedule'")
            self.res.update({
                "spec": {
                    "jobTemplate": self.job_template,
                    "schedule": self.schedule,
                }
            })
            if self.successful_jobs_history_limit:
                self.res["spec"]["successfulJobsHistoryLimit"] = self.successful_jobs_history_limit
            if self.failed_jobs_history_limit:
                self.res["spec"]["failedJobsHistoryLimit"] = self.failed_jobs_history_limit
            if self.concurrency_policy:
                self.res["spec"]["concurrencyPolicy"] = self.concurrency_policy
