# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class PipelineRun(NamespacedResource):
    """
        PipelineRun represents a single execution of a Pipeline. PipelineRuns are how
    the graph of Tasks declared in a Pipeline are executed; they specify inputs
    to Pipelines such as parameter values and capture operational aspects of the
    Tasks execution such as service account and tolerations. Creating a
    PipelineRun creates TaskRuns for Tasks in the referenced Pipeline.
    """

    api_group: str = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        params: list[Any] | None = None,
        pipeline_ref: dict[str, Any] | None = None,
        pipeline_spec: Any | None = None,
        task_run_specs: list[Any] | None = None,
        task_run_template: dict[str, Any] | None = None,
        timeouts: dict[str, Any] | None = None,
        workspaces: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            params (list[Any]): Params is a list of parameter names and values.

            pipeline_ref (dict[str, Any]): PipelineRef can be used to refer to a specific instance of a Pipeline.

            pipeline_spec (Any): Specifying PipelineSpec can be disabled by setting `disable-inline-
              spec` feature flag. See Pipeline.spec (API version: tekton.dev/v1)

            task_run_specs (list[Any]): TaskRunSpecs holds a set of runtime specs

            task_run_template (dict[str, Any]): TaskRunTemplate represent template of taskrun

            timeouts (dict[str, Any]): Time after which the Pipeline times out. Currently three keys are
              accepted in the map pipeline, tasks and finally with
              Timeouts.pipeline >= Timeouts.tasks + Timeouts.finally

            workspaces (list[Any]): Workspaces holds a set of workspace bindings that must match names
              with those declared in the pipeline.

        """
        super().__init__(**kwargs)

        self.params = params
        self.pipeline_ref = pipeline_ref
        self.pipeline_spec = pipeline_spec
        self.task_run_specs = task_run_specs
        self.task_run_template = task_run_template
        self.timeouts = timeouts
        self.workspaces = workspaces

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.params is not None:
                _spec["params"] = self.params

            if self.pipeline_ref is not None:
                _spec["pipelineRef"] = self.pipeline_ref

            if self.pipeline_spec is not None:
                _spec["pipelineSpec"] = self.pipeline_spec

            if self.task_run_specs is not None:
                _spec["taskRunSpecs"] = self.task_run_specs

            if self.task_run_template is not None:
                _spec["taskRunTemplate"] = self.task_run_template

            if self.timeouts is not None:
                _spec["timeouts"] = self.timeouts

            if self.workspaces is not None:
                _spec["workspaces"] = self.workspaces

    # End of generated code
