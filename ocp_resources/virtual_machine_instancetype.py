# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class VirtualMachineInstancetype(NamespacedResource):
    """
        VirtualMachineInstancetype resource contains quantitative and resource related VirtualMachine configuration
    that can be used by multiple VirtualMachine resources.
    """

    api_group: str = NamespacedResource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO

    def __init__(
        self,
        spec_annotations: Optional[Dict[str, Any]] = None,
        cpu: Optional[Dict[str, Any]] = None,
        gpus: Optional[List[Any]] = None,
        host_devices: Optional[List[Any]] = None,
        io_threads_policy: Optional[str] = "",
        launch_security: Optional[Dict[str, Any]] = None,
        memory: Optional[Dict[str, Any]] = None,
        node_selector: Optional[Dict[str, Any]] = None,
        scheduler_name: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            spec_annotations (Dict[str, Any]): Optionally defines the required Annotations to be used by the instance
              type and applied to the VirtualMachineInstance

            cpu (Dict[str, Any]): Required CPU related attributes of the instancetype.

            gpus (List[Any]): Optionally defines any GPU devices associated with the instancetype.

            host_devices (List[Any]): Optionally defines any HostDevices associated with the instancetype.

            io_threads_policy (str): Optionally defines the IOThreadsPolicy to be used by the instancetype.

            launch_security (Dict[str, Any]): Optionally defines the LaunchSecurity to be used by the instancetype.

            memory (Dict[str, Any]): Required Memory related attributes of the instancetype.

            node_selector (Dict[str, Any]): NodeSelector is a selector which must be true for the vmi to fit on a
              node. Selector which must match a node's labels for the vmi to be
              scheduled on that node. More info:
              https://kubernetes.io/docs/concepts/configuration/assign-pod-node/
              NodeSelector is the name of the custom node selector for the
              instancetype.

            scheduler_name (str): If specified, the VMI will be dispatched by specified scheduler. If
              not specified, the VMI will be dispatched by default scheduler.
              SchedulerName is the name of the custom K8s scheduler for the
              instancetype.

        """
        super().__init__(**kwargs)

        self.spec_annotations = spec_annotations
        self.cpu = cpu
        self.gpus = gpus
        self.host_devices = host_devices
        self.io_threads_policy = io_threads_policy
        self.launch_security = launch_security
        self.memory = memory
        self.node_selector = node_selector
        self.scheduler_name = scheduler_name

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.cpu:
                raise MissingRequiredArgumentError(argument="self.cpu")

            if not self.memory:
                raise MissingRequiredArgumentError(argument="self.memory")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["cpu"] = self.cpu
            _spec["memory"] = self.memory

            if self.spec_annotations:
                _spec["annotations"] = self.spec_annotations

            if self.gpus:
                _spec["gpus"] = self.gpus

            if self.host_devices:
                _spec["hostDevices"] = self.host_devices

            if self.io_threads_policy:
                _spec["ioThreadsPolicy"] = self.io_threads_policy

            if self.launch_security:
                _spec["launchSecurity"] = self.launch_security

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.scheduler_name:
                _spec["schedulerName"] = self.scheduler_name

    # End of generated code
