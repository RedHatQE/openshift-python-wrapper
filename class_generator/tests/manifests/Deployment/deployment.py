# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class Deployment(NamespacedResource):
    """
    Deployment enables declarative updates for Pods and ReplicaSets.
    """

    api_group: str = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        min_ready_seconds: Optional[int] = None,
        paused: Optional[bool] = None,
        progress_deadline_seconds: Optional[int] = None,
        replicas: Optional[int] = None,
        revision_history_limit: Optional[int] = None,
        selector: Optional[Dict[str, Any]] = None,
        strategy: Optional[Dict[str, Any]] = None,
        template: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            min_ready_seconds (int): Minimum number of seconds for which a newly created pod should be
              ready without any of its container crashing, for it to be
              considered available. Defaults to 0 (pod will be considered
              available as soon as it is ready)

            paused (bool): Indicates that the deployment is paused.

            progress_deadline_seconds (int): The maximum time in seconds for a deployment to make progress before
              it is considered to be failed. The deployment controller will
              continue to process failed deployments and a condition with a
              ProgressDeadlineExceeded reason will be surfaced in the deployment
              status. Note that progress will not be estimated during the time a
              deployment is paused. Defaults to 600s.

            replicas (int): Number of desired pods. This is a pointer to distinguish between
              explicit zero and not specified. Defaults to 1.

            revision_history_limit (int): The number of old ReplicaSets to retain to allow rollback. This is a
              pointer to distinguish between explicit zero and not specified.
              Defaults to 10.

            selector (Dict[str, Any]): A label selector is a label query over a set of resources. The result
              of matchLabels and matchExpressions are ANDed. An empty label
              selector matches all objects. A null label selector matches no
              objects.

            strategy (Dict[str, Any]): DeploymentStrategy describes how to replace existing pods with new
              ones.

            template (Dict[str, Any]): PodTemplateSpec describes the data a pod should have when created from
              a template

        """
        super().__init__(**kwargs)

        self.min_ready_seconds = min_ready_seconds
        self.paused = paused
        self.progress_deadline_seconds = progress_deadline_seconds
        self.replicas = replicas
        self.revision_history_limit = revision_history_limit
        self.selector = selector
        self.strategy = strategy
        self.template = template

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.selector:
                raise MissingRequiredArgumentError(argument="self.selector")

            if not self.template:
                raise MissingRequiredArgumentError(argument="self.template")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["selector"] = self.selector
            _spec["template"] = self.template

            if self.min_ready_seconds:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.paused is not None:
                _spec["paused"] = self.paused

            if self.progress_deadline_seconds:
                _spec["progressDeadlineSeconds"] = self.progress_deadline_seconds

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.revision_history_limit:
                _spec["revisionHistoryLimit"] = self.revision_history_limit

            if self.strategy:
                _spec["strategy"] = self.strategy

    # End of generated code
