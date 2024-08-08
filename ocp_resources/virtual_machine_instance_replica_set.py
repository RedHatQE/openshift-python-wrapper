# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class VirtualMachineInstanceReplicaSet(NamespacedResource):
    """
    VirtualMachineInstance is *the* VirtualMachineInstance Definition. It
    represents a virtual machine in the runtime environment of kubernetes.
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        paused: Optional[bool] = None,
        replicas: Optional[int] = None,
        selector: Optional[Dict[str, Any]] = None,
        template: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            paused(bool): Indicates that the replica set is paused.

            replicas(int): Number of desired pods. This is a pointer to distinguish between explicit
              zero and not specified. Defaults to 1.

            selector(Dict[Any, Any]): Label selector for pods. Existing ReplicaSets whose pods are selected by
              this will be the ones affected by this deployment.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            template(Dict[Any, Any]): Template describes the pods that will be created.

              FIELDS:
                metadata	<Object>
                  <no description>

                spec	<Object>
                  VirtualMachineInstance Spec contains the VirtualMachineInstance
                  specification.

        """
        super().__init__(**kwargs)

        self.paused = paused
        self.replicas = replicas
        self.selector = selector
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

            if self.paused is not None:
                _spec["paused"] = self.paused

            if self.replicas:
                _spec["replicas"] = self.replicas
