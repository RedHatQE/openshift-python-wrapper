import kubernetes

from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class Job(NamespacedResource):
    """
    Job object.

    Args:
        name (str): Job name.
        namespace (str): Namespace name.
        client (DynamicClient): Dynamic client for connecting to a remote cluster.
        teardown (bool): Indicates if this resource would need to be deleted.
        privileged_client (DynamicClient): Instance of Dynamic client.
        yaml_file (str): Yaml file for the resource.
        delete_timeout (int): Timeout associated with delete action.
        backoff_limit (int): The number of retries for a job.
        restart_policy (str): The restart policy of the pod.
        service_account (str): Optional. Service account name.
        containers (list): List of containers belonging to the pod that the job will create.
        background_propagation_policy (str): Control how object dependents will be deleted when an object is
                deleted (for example the pods left behind when you delete a Job). Options are: "Background",
                "Foreground" and "Orphan". Read more here:
                    https://kubernetes.io/docs/concepts/architecture/garbage-collection/#cascading-deletion
    """

    api_group = NamespacedResource.ApiGroup.BATCH

    class Condition(NamespacedResource.Condition):
        COMPLETE = "Complete"

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        backoff_limit=None,
        restart_policy=None,
        service_account=None,
        containers=None,
        background_propagation_policy=None,
        **kwargs,
    ):
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
        self.restart_policy = restart_policy
        self.backoff_limit = backoff_limit
        self.service_account = service_account
        self.containers = containers
        self.background_propagation_policy = background_propagation_policy

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            self.res.setdefault("spec", {})

            if self.backoff_limit is not None:
                self.res["spec"]["backoffLimit"] = self.backoff_limit

            if self.containers:
                self.res["spec"].setdefault("template", {}).setdefault("spec", {})
                self.res["spec"]["template"]["spec"]["containers"] = self.containers

                if self.service_account:
                    self.res["spec"]["template"]["spec"]["serviceAccount"] = self.service_account

                if self.restart_policy:
                    self.res["spec"]["template"]["spec"]["restartPolicy"] = self.restart_policy

    def delete(self, wait=False, timeout=TIMEOUT_4MINUTES, body=None):
        """
        Delete Job object

        Args:
            wait (bool): True to wait for Job to be deleted.
            timeout (int): Time to wait for resource deletion.
            body (dict): Content to send to delete().

        Returns:
            bool: True if delete succeeded, False otherwise.
        """
        if not body and self.background_propagation_policy:
            body = kubernetes.client.V1DeleteOptions(propagation_policy=self.background_propagation_policy)
        return super().delete(wait=wait, timeout=timeout, body=body)
