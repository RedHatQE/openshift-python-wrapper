from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class Job(NamespacedResource):
    """
    Job object.
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

    def to_dict(self):
        self.res = super().to_dict()
        self.res.setdefault("spec", {})

        if self.backoff_limit is not None:
            self.res["spec"]["backoffLimit"] = self.backoff_limit

        if self.containers:
            self.res["spec"].setdefault("template", {}).setdefault("spec", {})
            self.res["spec"]["template"]["spec"]["containers"] = self.containers

            if self.service_account:
                self.res["spec"]["template"]["spec"][
                    "serviceAccount"
                ] = self.service_account

            if self.restart_policy:
                self.res["spec"]["template"]["spec"][
                    "restartPolicy"
                ] = self.restart_policy

        return self.res
