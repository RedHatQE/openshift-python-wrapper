# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Task(NamespacedResource):
    """
        Task represents a collection of sequential steps that are run as part of a
    Pipeline using a set of inputs and producing a set of outputs. Tasks execute
    when TaskRuns are created that provide the input parameters and resources and
    output resources the Task requires.
    """

    api_group: str = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        description: str | None = None,
        display_name: str | None = None,
        params: list[Any] | None = None,
        results: list[Any] | None = None,
        sidecars: list[Any] | None = None,
        step_template: dict[str, Any] | None = None,
        steps: list[Any] | None = None,
        volumes: Any | None = None,
        workspaces: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            description (str): Description is a user-facing description of the task that may be used
              to populate a UI.

            display_name (str): DisplayName is a user-facing name of the task that may be used to
              populate a UI.

            params (list[Any]): Params is a list of input parameters required to run the task. Params
              must be supplied as inputs in TaskRuns unless they declare a
              default value.

            results (list[Any]): Results are values that this Task can output

            sidecars (list[Any]): Sidecars are run alongside the Task's step containers. They begin
              before the steps start and end after the steps complete.

            step_template (dict[str, Any]): StepTemplate can be used as the basis for all step containers within
              the Task, so that the steps inherit settings on the base
              container.

            steps (list[Any]): Steps are the steps of the build; each step is run sequentially with
              the source mounted into /workspace.

            volumes (Any): Volumes is a collection of volumes that are available to mount into
              the steps of the build. See Pod.spec.volumes (API version: v1)

            workspaces (list[Any]): Workspaces are the volumes that this Task requires.

        """
        super().__init__(**kwargs)

        self.description = description
        self.display_name = display_name
        self.params = params
        self.results = results
        self.sidecars = sidecars
        self.step_template = step_template
        self.steps = steps
        self.volumes = volumes
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

            if self.params is not None:
                _spec["params"] = self.params

            if self.results is not None:
                _spec["results"] = self.results

            if self.sidecars is not None:
                _spec["sidecars"] = self.sidecars

            if self.step_template is not None:
                _spec["stepTemplate"] = self.step_template

            if self.steps is not None:
                _spec["steps"] = self.steps

            if self.volumes is not None:
                _spec["volumes"] = self.volumes

            if self.workspaces is not None:
                _spec["workspaces"] = self.workspaces

    # End of generated code
