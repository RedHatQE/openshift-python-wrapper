# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class Deployment(NamespacedResource):
    """
    Deployment enables declarative updates for Pods and ReplicaSets.

    API Link: https://example.explain
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
            min_ready_seconds(int): <please add description>
            paused(bool): <please add description>
            progress_deadline_seconds(int): <please add description>
            replicas(int): <please add description>
            revision_history_limit(int): <please add description>
            selector(Dict[Any, Any]): <please add description>
            strategy(Dict[Any, Any]): <please add description>
            template(Dict[Any, Any]): <please add description>
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

        if not self.yaml_file:
            if not all([
                self.selector,
                self.template,
            ]):
                raise MissingRequiredArgumentError(argument="selector, template")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            self.res["selector"] = self.selector
            self.res["template"] = self.template

            if self.min_ready_seconds:
                self.res["minReadySeconds"] = self.min_ready_seconds

            if self.paused is not None:
                self.res["paused"] = self.paused

            if self.progress_deadline_seconds:
                self.res["progressDeadlineSeconds"] = self.progress_deadline_seconds

            if self.replicas:
                self.res["replicas"] = self.replicas

            if self.revision_history_limit:
                self.res["revisionHistoryLimit"] = self.revision_history_limit

            if self.strategy:
                self.res["strategy"] = self.strategy
