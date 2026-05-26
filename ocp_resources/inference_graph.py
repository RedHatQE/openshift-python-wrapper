# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class InferenceGraph(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.SERVING_KSERVE_IO

    def __init__(
        self,
        affinity: dict[str, Any] | None = None,
        max_replicas: int | None = None,
        min_replicas: int | None = None,
        nodes: dict[str, Any] | None = None,
        resources: dict[str, Any] | None = None,
        scale_metric: str | None = None,
        scale_target: int | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            affinity (dict[str, Any]): No field description from API

            max_replicas (int): No field description from API

            min_replicas (int): No field description from API

            nodes (dict[str, Any]): No field description from API

            resources (dict[str, Any]): No field description from API

            scale_metric (str): No field description from API

            scale_target (int): No field description from API

            timeout (int): No field description from API

        """
        super().__init__(**kwargs)

        self.affinity = affinity
        self.max_replicas = max_replicas
        self.min_replicas = min_replicas
        self.nodes = nodes
        self.resources = resources
        self.scale_metric = scale_metric
        self.scale_target = scale_target
        self.timeout = timeout

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.nodes is None:
                raise MissingRequiredArgumentError(argument="self.nodes")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["nodes"] = self.nodes

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.max_replicas is not None:
                _spec["maxReplicas"] = self.max_replicas

            if self.min_replicas is not None:
                _spec["minReplicas"] = self.min_replicas

            if self.resources is not None:
                _spec["resources"] = self.resources

            if self.scale_metric is not None:
                _spec["scaleMetric"] = self.scale_metric

            if self.scale_target is not None:
                _spec["scaleTarget"] = self.scale_target

            if self.timeout is not None:
                _spec["timeout"] = self.timeout

    # End of generated code
