# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class VirtualMachineInstanceReplicaSet(NamespacedResource):
    """
    VirtualMachineInstance is *the* VirtualMachineInstance Definition. It represents a virtual machine in the runtime environment of kubernetes.
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        paused: bool | None = None,
        replicas: int | None = None,
        selector: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            paused (bool): Indicates that the replica set is paused.

            replicas (int): Number of desired pods. This is a pointer to distinguish between
              explicit zero and not specified. Defaults to 1.

            selector (dict[str, Any]): Label selector for pods. Existing ReplicaSets whose pods are selected
              by this will be the ones affected by this deployment.

            template (dict[str, Any]): Template describes the pods that will be created.

        """
        super().__init__(**kwargs)

        self.paused = paused
        self.replicas = replicas
        self.selector = selector
        self.template = template

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.selector is None:
                raise MissingRequiredArgumentError(argument="self.selector")

            if self.template is None:
                raise MissingRequiredArgumentError(argument="self.template")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["selector"] = self.selector
            _spec["template"] = self.template

            if self.paused is not None:
                _spec["paused"] = self.paused

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

    # End of generated code
