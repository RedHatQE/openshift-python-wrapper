from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class CronJob(NamespacedResource):
    """
    https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/cron-job-v1/
    """

    api_group = NamespacedResource.ApiGroup.BATCH

    def __init__(
        self,
        schedule=None,
        job_template=None,
        timezone=None,
        concurrency_policy=None,
        starting_deadline_seconds=None,
        suspend=None,
        successful_jobs_history_limit=None,
        failed_jobs_history_limit=None,
        **kwargs,
    ):
        """
        Args:
            schedule (str): schedule of the cron job
            job_template (dict): describes the job that would be created when a cronjob would be executed
                Example:
                    job_template: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/#JobSpec
            timezone (str, optional): timezone name for the given schedule
            concurrency_policy (str, optional): indicates how to treat concurrent execution of a job
            suspend (bool, optional): suspend subsequent executions
            successful_jobs_history_limit (int, optional): number of successful jobs to retain
            failed_jobs_history_limit (int, optional): number of failed jobs to retain
            starting_deadline_seconds (int, optional): deadline in seconds, for starting a job, in case it does not
            start at scheduled time
        """
        super().__init__(**kwargs)
        self.job_template = job_template
        self.schedule = schedule
        self.timezone = timezone
        self.concurrency_policy = concurrency_policy
        self.suspend = suspend
        self.successful_jobs_history_limit = successful_jobs_history_limit
        self.failed_jobs_history_limit = failed_jobs_history_limit
        self.starting_deadline_seconds = starting_deadline_seconds

    def to_dict(self) -> None:
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
            if self.timezone:
                self.res["spec"]["timezone"] = self.timezone
            if self.suspend:
                self.res["spec"]["suspend"] = self.suspend
            if self.successful_jobs_history_limit:
                self.res["spec"]["successfulJobsHistoryLimit"] = self.successful_jobs_history_limit
            if self.failed_jobs_history_limit:
                self.res["spec"]["failedJobsHistoryLimit"] = self.failed_jobs_history_limit
            if self.concurrency_policy:
                self.res["spec"]["concurrencyPolicy"] = self.concurrency_policy
