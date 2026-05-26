# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, Resource


class VirtualMachineClusterInstancetype(Resource):
    """
    VirtualMachineClusterInstancetype is a cluster scoped version of VirtualMachineInstancetype resource.
    """

    api_group: str = Resource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO

    def __init__(
        self,
        spec_annotations: dict[str, Any] | None = None,
        cpu: dict[str, Any] | None = None,
        gpus: list[Any] | None = None,
        host_devices: list[Any] | None = None,
        io_threads_policy: str | None = None,
        launch_security: dict[str, Any] | None = None,
        memory: dict[str, Any] | None = None,
        node_selector: dict[str, Any] | None = None,
        scheduler_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            spec_annotations (dict[str, Any]): Optionally defines the required Annotations to be used by the instance
              type and applied to the VirtualMachineInstance

            cpu (dict[str, Any]): Required CPU related attributes of the instancetype.

            gpus (list[Any]): Optionally defines any GPU devices associated with the instancetype.

            host_devices (list[Any]): Optionally defines any HostDevices associated with the instancetype.

            io_threads_policy (str): Optionally defines the IOThreadsPolicy to be used by the instancetype.

            launch_security (dict[str, Any]): Optionally defines the LaunchSecurity to be used by the instancetype.

            memory (dict[str, Any]): Required Memory related attributes of the instancetype.

            node_selector (dict[str, Any]): NodeSelector is a selector which must be true for the vmi to fit on a
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
            if self.cpu is None:
                raise MissingRequiredArgumentError(argument="self.cpu")

            if self.memory is None:
                raise MissingRequiredArgumentError(argument="self.memory")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["cpu"] = self.cpu
            _spec["memory"] = self.memory

            if self.spec_annotations is not None:
                _spec["annotations"] = self.spec_annotations

            if self.gpus is not None:
                _spec["gpus"] = self.gpus

            if self.host_devices is not None:
                _spec["hostDevices"] = self.host_devices

            if self.io_threads_policy is not None:
                _spec["ioThreadsPolicy"] = self.io_threads_policy

            if self.launch_security is not None:
                _spec["launchSecurity"] = self.launch_security

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

            if self.scheduler_name is not None:
                _spec["schedulerName"] = self.scheduler_name

    # End of generated code
