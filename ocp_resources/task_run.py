# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class TaskRun(NamespacedResource):
    """
        TaskRun represents a single execution of a Task. TaskRuns are how the steps
    specified in a Task are executed; they specify the parameters and resources
    used to run the steps in a Task.
    """

    api_group: str = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        compute_resources: dict[str, Any] | None = None,
        debug: dict[str, Any] | None = None,
        params: list[Any] | None = None,
        pod_template: dict[str, Any] | None = None,
        retries: int | None = None,
        service_account_name: str | None = None,
        sidecar_specs: list[Any] | None = None,
        status_message: str | None = None,
        step_specs: list[Any] | None = None,
        task_ref: dict[str, Any] | None = None,
        task_spec: Any | None = None,
        timeout: str | None = None,
        workspaces: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            compute_resources (dict[str, Any]): Compute resources to use for this TaskRun

            debug (dict[str, Any]): TaskRunDebug defines the breakpoint config for a particular TaskRun

            params (list[Any]): Params is a list of Param

            pod_template (dict[str, Any]): PodTemplate holds pod specific configuration

            retries (int): Retries represents how many times this TaskRun should be retried in
              the event of task failure.

            service_account_name (str): No field description from API

            sidecar_specs (list[Any]): Specs to apply to Sidecars in this TaskRun. If a field is specified in
              both a Sidecar and a SidecarSpec, the value from the SidecarSpec
              will be used. This field is only supported when the alpha feature
              gate is enabled.

            status_message (str): Status message for cancellation.

            step_specs (list[Any]): Specs to apply to Steps in this TaskRun. If a field is specified in
              both a Step and a StepSpec, the value from the StepSpec will be
              used. This field is only supported when the alpha feature gate is
              enabled.

            task_ref (dict[str, Any]): no more than one of the TaskRef and TaskSpec may be specified.

            task_spec (Any): Specifying TaskSpec can be disabled by setting `disable-inline-spec`
              feature flag. See Task.spec (API version: tekton.dev/v1)

            timeout (str): Time after which one retry attempt times out. Defaults to 1 hour.
              Refer Go's ParseDuration documentation for expected format:
              https://golang.org/pkg/time/#ParseDuration

            workspaces (list[Any]): Workspaces is a list of WorkspaceBindings from volumes to workspaces.

        """
        super().__init__(**kwargs)

        self.compute_resources = compute_resources
        self.debug = debug
        self.params = params
        self.pod_template = pod_template
        self.retries = retries
        self.service_account_name = service_account_name
        self.sidecar_specs = sidecar_specs
        self.status_message = status_message
        self.step_specs = step_specs
        self.task_ref = task_ref
        self.task_spec = task_spec
        self.timeout = timeout
        self.workspaces = workspaces

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.compute_resources is not None:
                _spec["computeResources"] = self.compute_resources

            if self.debug is not None:
                _spec["debug"] = self.debug

            if self.params is not None:
                _spec["params"] = self.params

            if self.pod_template is not None:
                _spec["podTemplate"] = self.pod_template

            if self.retries is not None:
                _spec["retries"] = self.retries

            if self.service_account_name is not None:
                _spec["serviceAccountName"] = self.service_account_name

            if self.sidecar_specs is not None:
                _spec["sidecarSpecs"] = self.sidecar_specs

            if self.status_message is not None:
                _spec["statusMessage"] = self.status_message

            if self.step_specs is not None:
                _spec["stepSpecs"] = self.step_specs

            if self.task_ref is not None:
                _spec["taskRef"] = self.task_ref

            if self.task_spec is not None:
                _spec["taskSpec"] = self.task_spec

            if self.timeout is not None:
                _spec["timeout"] = self.timeout

            if self.workspaces is not None:
                _spec["workspaces"] = self.workspaces

    # End of generated code
