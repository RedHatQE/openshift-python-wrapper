# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Pipeline(NamespacedResource):
    """
        Pipeline describes a list of Tasks to execute. It expresses how outputs
    of tasks feed into inputs of subsequent tasks.
    """

    api_group: str = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        description: str | None = None,
        display_name: str | None = None,
        finally_: list[Any] | None = None,
        params: list[Any] | None = None,
        results: list[Any] | None = None,
        tasks: list[Any] | None = None,
        workspaces: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            description (str): Description is a user-facing description of the pipeline that may be
              used to populate a UI.

            display_name (str): DisplayName is a user-facing name of the pipeline that may be used to
              populate a UI.

            finally_ (list[Any]): Finally declares the list of Tasks that execute just before leaving
              the Pipeline i.e. either after all Tasks are finished executing
              successfully or after a failure which would result in ending the
              Pipeline

                Note: Parameter renamed from &#39;finally&#39; to avoid Python keyword conflict.
            params (list[Any]): Params declares a list of input parameters that must be supplied when
              this Pipeline is run.

            results (list[Any]): Results are values that this pipeline can output once run

            tasks (list[Any]): Tasks declares the graph of Tasks that execute when this Pipeline is
              run.

            workspaces (list[Any]): Workspaces declares a set of named workspaces that are expected to be
              provided by a PipelineRun.

        """
        super().__init__(**kwargs)

        self.description = description
        self.display_name = display_name
        self.finally_ = finally_
        self.params = params
        self.results = results
        self.tasks = tasks
        self.workspaces = workspaces

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.description is not None:
                _spec["description"] = self.description

            if self.display_name is not None:
                _spec["displayName"] = self.display_name

            if self.finally_ is not None:
                _spec["finally"] = self.finally_

            if self.params is not None:
                _spec["params"] = self.params

            if self.results is not None:
                _spec["results"] = self.results

            if self.tasks is not None:
                _spec["tasks"] = self.tasks

            if self.workspaces is not None:
                _spec["workspaces"] = self.workspaces

    # End of generated code
