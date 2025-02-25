from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class Task(NamespacedResource):
    """
    A collection of Steps for continuous integration flow, executed as a Pod on a Kubernetes cluster.
    API Reference: https://tekton.dev/docs/pipelines/tasks/#configuring-a-task
    """

    api_group: str = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        steps: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        params: Optional[List[Dict[str, str]]] = None,
        workspaces: Optional[List[Dict[str, Any]]] = None,
        results: Optional[List[Dict[str, Any]]] = None,
        volumes: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        step_template: Optional[Dict[str, Any]] = None,
        sidecars: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ):
        """
        Create and manage Task which specifies a sequence of steps to be executed.

        Args:
            steps (List[Dict[str, Any]]): Specifies one or more container images to run in the Task.
            description (Optional[str]): An informative description of the Task.
            params (Optional[List[Dict[str, str]]]): Specifies execution parameters for the Task.
            workspaces (Optional[List[Dict[str, Any]]]): Specifies paths to volumes required by the Task.
            results (Optional[List[Dict[str, Any]]]): Specifies the names under which Tasks write execution results.
            volumes (Optional[List[Dict[str, Dict[str, Any]]]]): Specifies one or more volumes that will be available to the Steps in the Task.
            step_template (Optional[Dict[str, Any]]): Specifies a Container step definition to use as the basis for all Steps in the Task.
            sidecars (Optional[List[Dict[str, Any]]]): Specifies Sidecar containers to run alongside the Steps in the Task.
        """
        super().__init__(**kwargs)
        self.steps = steps
        self.description = description
        self.params = params
        self.workspaces = workspaces
        self.results = results
        self.volumes = volumes
        self.step_template = step_template
        self.sidecars = sidecars

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.steps:
                raise MissingRequiredArgumentError(argument="steps")
            self.res["spec"] = {}
            _spec = self.res["spec"]
            _spec = {"steps": self.steps}

            if self.description:
                _spec["description"] = self.description

            if self.params:
                _spec["params"] = self.params

            if self.workspaces:
                _spec["workspaces"] = self.workspaces

            if self.results:
                _spec["results"] = self.results

            if self.volumes:
                _spec["volumes"] = self.volumes

            if self.step_template:
                _spec["stepTemplate"] = self.step_template

            if self.sidecars:
                _spec["sidecars"] = self.sidecars
