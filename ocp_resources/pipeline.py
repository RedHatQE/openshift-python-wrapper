# API reference: https://tekton.dev/docs/pipelines/pipelines/

from ocp_resources.resource import NamespacedResource


class Pipeline(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        name=None,
        namespace=None,
        tasks=None,
        params=None,
        final_parallel_tasks=None,
        client=None,
        yaml_file=None,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the pipeline
            namespace (str): Namespace of the pipeline
            tasks (str, optional): actions to perform in pipeline
            client: (DynamicClient): DynamicClient to use.
            params (dict, optional):  params to support pipelines.
            params can be set/changed based on tasks.
            example: 'spec': {'params': [{'name': 'sourceTemplateName','type': 'string','default':'openshift'},
            {'name': 'sourceTemplateNamespace', 'type':'string', 'description': 'Namespace pf template'}]}
            final_parallel_tasks (list, optional):  a list of one or more to be executed in parallel after all other
            tasks have completed in parallel.
            spec section can't be empty. It requires at least one optional field.
        """
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            **kwargs,
        )
        # TODO: Add a check for tasks when bug https://issues.redhat.com/browse/SRVKP-3019 is resolved.
        self.tasks = tasks
        self.params = params
        self.final_parallel_tasks = final_parallel_tasks

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if not (self.tasks or self.params or self.final_parallel_tasks):
                raise ValueError(
                    "spec is expected to have at least one of the optional fields, got none"
                )
            self.res["spec"] = {}
            if self.params:
                self.res["spec"]["params"] = self.params
            if self.tasks:
                self.res["spec"]["tasks"] = self.tasks
            if self.final_parallel_tasks:
                self.res["spec"]["finally"] = self.final_parallel_tasks
