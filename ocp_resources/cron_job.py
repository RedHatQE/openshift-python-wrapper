from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class CronJob(NamespacedResource):
    """
    CronJob object. API reference:
    https://docs.openshift.com/container-platform/4.12/rest_api/workloads_apis/cronjob-batch-v1.html
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
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the endpoints resource
            namespace (str): Namespace of endpoints resource
            client: (DynamicClient): DynamicClient for api calls
            teardown (bool): Indicates if the resource should be torn down at the end
            privileged_client (DynamicClient): Privileged client for api calls
            yaml_file (str): yaml file for the resource.
            delete_timeout (int): timeout associated with delete action
            schedule (str): schedule of the cron job
            jobTemplate (object): describes data a job should have when created from a template
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

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "jobTemplate": self.job_template,
                        "schedule": self.schedule,
                    }
                }
            )
