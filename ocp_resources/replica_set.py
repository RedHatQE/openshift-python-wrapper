# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReplicaSet(NamespacedResource):
    """
    ReplicaSet ensures that a specified number of pod replicas are running at
    any given time.
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
            min_ready_seconds(int): Minimum number of seconds for which a newly created pod should be ready
              without any of its container crashing, for it to be considered available.
              Defaults to 0 (pod will be considered available as soon as it is ready)

            replicas(int): Replicas is the number of desired replicas. This is a pointer to distinguish
              between explicit zero and unspecified. Defaults to 1. More info:
              https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller

            selector(Dict[Any, Any]): Selector is a label query over pods that should match the replica count.
              Label keys and values that must match in order to be controlled by this
              replica set. It must match the pod template's labels. More info:
              https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
              A label selector is a label query over a set of resources. The result of
              matchLabels and matchExpressions are ANDed. An empty label selector matches
              all objects. A null label selector matches no objects.

              FIELDS:
                matchExpressions	<[]LabelSelectorRequirement>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            template(Dict[Any, Any]): Template is the object that describes the pod that will be created if
              insufficient replicas are detected. More info:
              https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template
              PodTemplateSpec describes the data a pod should have when created from a
              template

              FIELDS:
                metadata	<ObjectMeta>
                  Standard object's metadata. More info:
                  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

                spec	<PodSpec>
                  Specification of the desired behavior of the pod. More info:
                  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

        """
        super().__init__(**kwargs)

        self.min_ready_seconds = min_ready_seconds
        self.replicas = replicas
        self.selector = selector
        self.template = template

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            if not all([
                self.selector,
            ]):
                raise MissingRequiredArgumentError(argument="selector")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["selector"] = self.selector

            if self.min_ready_seconds:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.template:
                _spec["template"] = self.template
