# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReplicaSet(NamespacedResource):
    """
    ReplicaSet ensures that a specified number of pod replicas are running at any given time.
    """

    api_group: str = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        min_ready_seconds: Optional[int] = None,
        replicas: Optional[int] = None,
        selector: Optional[Dict[str, Any]] = None,
        template: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            min_ready_seconds (int): Minimum number of seconds for which a newly created pod should be
              ready without any of its container crashing, for it to be
              considered available. Defaults to 0 (pod will be considered
              available as soon as it is ready)

            replicas (int): Replicas is the number of desired replicas. This is a pointer to
              distinguish between explicit zero and unspecified. Defaults to 1.
              More info: https://kubernetes.io/docs/concepts/workloads/controlle
              rs/replicationcontroller/#what-is-a-replicationcontroller

            selector (Dict[str, Any]): A label selector is a label query over a set of resources. The result
              of matchLabels and matchExpressions are ANDed. An empty label
              selector matches all objects. A null label selector matches no
              objects.

            template (Dict[str, Any]): PodTemplateSpec describes the data a pod should have when created from
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
            if not self.selector:
                raise MissingRequiredArgumentError(argument="self.selector")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["selector"] = self.selector

            if self.min_ready_seconds:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.template:
                _spec["template"] = self.template

    # End of generated code
