# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReplicaSet(NamespacedResource):
    """
    ReplicaSet ensures that a specified number of pod replicas are running at any given time.
    """

    api_group: str = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        min_ready_seconds: int | None = None,
        replicas: int | None = None,
        selector: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            min_ready_seconds (int): Minimum number of seconds for which a newly created pod should be
              ready without any of its container crashing, for it to be
              considered available. Defaults to 0 (pod will be considered
              available as soon as it is ready)

            replicas (int): Replicas is the number of desired replicas. This is a pointer to
              distinguish between explicit zero and unspecified. Defaults to 1.
              More info: https://kubernetes.io/docs/concepts/workloads/controlle
              rs/replicationcontroller/#what-is-a-replicationcontroller

            selector (dict[str, Any]): A label selector is a label query over a set of resources. The result
              of matchLabels and matchExpressions are ANDed. An empty label
              selector matches all objects. A null label selector matches no
              objects.

            template (dict[str, Any]): PodTemplateSpec describes the data a pod should have when created from
              a template

        """
        super().__init__(**kwargs)

        self.min_ready_seconds = min_ready_seconds
        self.replicas = replicas
        self.selector = selector
        self.template = template

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.selector is None:
                raise MissingRequiredArgumentError(argument="self.selector")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["selector"] = self.selector

            if self.min_ready_seconds is not None:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.template is not None:
                _spec["template"] = self.template

    # End of generated code
