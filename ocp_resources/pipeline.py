# API reference: https://tekton.dev/docs/pipelines/pipelines/

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class Pipeline(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        tasks=None,
        params=None,
        final_parallel_tasks=None,
        **kwargs,
    ):
        """
        Args:
            tasks (str, optional): actions to perform in pipeline
            params (dict, optional):  params to support pipelines.
            params can be set/changed based on tasks.
            example: 'spec': {'params': [{'name': 'sourceTemplateName','type': 'string','default':'openshift'},
            {'name': 'sourceTemplateNamespace', 'type':'string', 'description': 'Namespace pf template'}]}
            final_parallel_tasks (list, optional):  a list of one or more to be executed in parallel after all other
            tasks have completed in parallel.
            spec section can't be empty. It requires at least one optional field.
        """
        super().__init__(**kwargs)
        # TODO: Add a check for tasks when bug https://issues.redhat.com/browse/SRVKP-3019 is resolved.
        self.tasks = tasks
        self.params = params
        self.final_parallel_tasks = final_parallel_tasks

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not (self.tasks or self.params or self.final_parallel_tasks):
                raise MissingRequiredArgumentError(argument="'tasks' or 'params' or 'final_parallel_tasks'")

            self.res["spec"] = {}
            if self.params:
                self.res["spec"]["params"] = self.params
            if self.tasks:
                self.res["spec"]["tasks"] = self.tasks
            if self.final_parallel_tasks:
                self.res["spec"]["finally"] = self.final_parallel_tasks
