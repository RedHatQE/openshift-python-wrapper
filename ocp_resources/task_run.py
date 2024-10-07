# API reference: https://tekton.dev/docs/pipelines/taskruns/

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class TaskRun(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        task_ref=None,
        task_spec=None,
        params=None,
        service_account_name=None,
        taskrun_timeout=None,
        **kwargs,
    ):
        """
        Create and manage TaskRun which allows you to instantiate and execute a Task on cluster

        Args:
            task_ref (str): Base task to run taskrun. Mandatory if task_spec is not provided.
            task_spec (str): Base task to run taskrun. Mandatory if task_ref is not provided.
            params (dict, optional): Params to add during triggering a run.
                params can be set/changed based on task_ref.
                example : params={"param_name1":"param_value1", "param_name2":"param_value2"}
            service_account_name (str, optional): Provide service account
            taskrun_timeout (str, optional): Specifies the taskrun_timeout before the taskrun fails
        """
        super().__init__(
            **kwargs,
        )
        self.task_ref = task_ref
        self.task_spec = task_spec
        self.params = params
        self.service_account_name = service_account_name
        self.taskrun_timeout = taskrun_timeout

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not (self.task_ref or self.task_spec):
                raise MissingRequiredArgumentError(argument="'task_ref' or 'task_spec'")

            if self.task_ref and self.task_spec:
                raise ValueError("Validation failed: expected exactly one either task_ref or task_spec, got both")

            self.res["spec"] = {}
            if self.task_ref:
                self.res["spec"]["taskRef"] = {"name": self.task_ref}

            if self.task_spec:
                self.res["spec"]["taskSpec"] = {"name": self.task_spec}

            if self.params:
                self.res["spec"]["params"] = [
                    {"name": params_name, "value": params_value} for params_name, params_value in self.params.items()
                ]

            if self.taskrun_timeout:
                self.res["spec"]["taskrun_timeout"] = self.taskrun_timeout

            if self.service_account_name:
                self.res["spec"]["serviceAccountName"] = self.service_account_name
