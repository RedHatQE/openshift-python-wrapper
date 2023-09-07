from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class CronJob(NamespacedResource):
    """
    CronJob object. API reference:
    https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/cron-job-v1/
    """

    api_group = NamespacedResource.ApiGroup.BATCH

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        schedule=None,
        job_template=None,
        timezone=None,
        concurrency_policy=None,
        starting_deadline_seconds=None,
        suspend=None,
        successful_jobs_history_limit=None,
        failed_jobs_history_limit=None,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the CronJob resource
            namespace (str): Namespace of CronJob resource
            client: (DynamicClient): DynamicClient for api calls
            teardown (bool): Indicates if the resource should be torn down at the end
            privileged_client (DynamicClient): Privileged client for api calls
            yaml_file (str): yaml file for the resource.
            delete_timeout (int, optional): timeout associated with delete action
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
        self.timezone = timezone
        self.concurrency_policy = concurrency_policy
        self.suspend = suspend
        self.successful_jobs_history_limit = successful_jobs_history_limit
        self.failed_jobs_history_limit = failed_jobs_history_limit
        self.starting_deadline_seconds = starting_deadline_seconds

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if not (self.job_template and self.schedule):
                raise ValueError(
                    "yaml_file or parameters 'job_template' and 'schedule' are"
                    " required."
                )
            self.res.update(
                {
                    "spec": {
                        "jobTemplate": self.job_template,
                        "schedule": self.schedule,
                    }
                }
            )
            if self.timezone:
                self.res["spec"]["timezone"] = self.timezone
            if self.suspend:
                self.res["spec"]["suspend"] = self.suspend
            if self.successful_jobs_history_limit:
                self.res["spec"][
                    "successfulJobsHistoryLimit"
                ] = self.successful_jobs_history_limit
            if self.failed_jobs_history_limit:
                self.res["spec"][
                    "failedJobsHistoryLimit"
                ] = self.failed_jobs_history_limit
            if self.concurrency_policy:
                self.res["spec"]["concurrencyPolicy"] = self.concurrency_policy
