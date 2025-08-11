# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any
from ocp_resources.resource import NamespacedResource


class Deployment(NamespacedResource):
    """
    Deployment enables declarative updates for Pods and ReplicaSets.
    """

    api_group: str = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        min_ready_seconds: int | None = None,
        paused: bool | None = None,
        progress_deadline_seconds: int | None = None,
        replicas: int | None = None,
        revision_history_limit: int | None = None,
        selector: dict[str, Any] | None = None,
        strategy: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            min_ready_seconds (int): No field description from API

            paused (bool): No field description from API

            progress_deadline_seconds (int): No field description from API

            replicas (int): No field description from API

            revision_history_limit (int): No field description from API

            selector (dict[str, Any]): No field description from API

            strategy (dict[str, Any]): No field description from API

            template (dict[str, Any]): No field description from API

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
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.min_ready_seconds is not None:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.paused is not None:
                _spec["paused"] = self.paused

            if self.progress_deadline_seconds is not None:
                _spec["progressDeadlineSeconds"] = self.progress_deadline_seconds

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.revision_history_limit is not None:
                _spec["revisionHistoryLimit"] = self.revision_history_limit

            if self.selector is not None:
                _spec["selector"] = self.selector

            if self.strategy is not None:
                _spec["strategy"] = self.strategy

            if self.template is not None:
                _spec["template"] = self.template

    # End of generated code
