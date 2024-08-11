# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class VirtualMachineInstancetype(NamespacedResource):
    """
    VirtualMachineInstancetype resource contains quantitative and resource
    related VirtualMachine configuration that can be used by multiple
    VirtualMachine resources.
    """

    api_group: str = NamespacedResource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO

    def __init__(
        self,
        annotations: Optional[Dict[str, Any]] = None,
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
            annotations(Dict[Any, Any]): Optionally defines the required Annotations to be used by the instance type
              and applied to the VirtualMachineInstance

            cpu(Dict[Any, Any]): Required CPU related attributes of the instancetype.

              FIELDS:
                dedicatedCPUPlacement	<boolean>
                  DedicatedCPUPlacement requests the scheduler to place the
                  VirtualMachineInstance on a node with enough dedicated pCPUs and pin the
                  vCPUs to it.

                guest	<integer> -required-
                  Required number of vCPUs to expose to the guest.
                   The resulting CPU topology being derived from the optional
                  PreferredCPUTopology attribute of CPUPreferences that itself defaults to
                  PreferSockets.

                isolateEmulatorThread	<boolean>
                  IsolateEmulatorThread requests one more dedicated pCPU to be allocated for
                  the VMI to place the emulator thread on it.

                model	<string>
                  Model specifies the CPU model inside the VMI. List of available models
                  https://github.com/libvirt/libvirt/tree/master/src/cpu_map. It is possible
                  to specify special cases like "host-passthrough" to get the same CPU as the
                  node and "host-model" to get CPU closest to the node one. Defaults to
                  host-model.

                numa	<Object>
                  NUMA allows specifying settings for the guest NUMA topology

                realtime	<Object>
                  Realtime instructs the virt-launcher to tune the VMI for lower latency,
                  optional for real time workloads

            gpus(List[Any]): Optionally defines any GPU devices associated with the instancetype.

              FIELDS:
                deviceName	<string> -required-
                  <no description>

                name	<string> -required-
                  Name of the GPU device as exposed by a device plugin

                tag	<string>
                  If specified, the virtual network interface address and its tag will be
                  provided to the guest via config drive

                virtualGPUOptions	<Object>
                  <no description>

            host_devices(List[Any]): Optionally defines any HostDevices associated with the instancetype.

              FIELDS:
                deviceName	<string> -required-
                  DeviceName is the resource name of the host device exposed by a device
                  plugin

                name	<string> -required-
                  <no description>

                tag	<string>
                  If specified, the virtual network interface address and its tag will be
                  provided to the guest via config drive

            io_threads_policy(str): Optionally defines the IOThreadsPolicy to be used by the instancetype.

            launch_security(Dict[Any, Any]): Optionally defines the LaunchSecurity to be used by the instancetype.

              FIELDS:
                sev	<Object>
                  AMD Secure Encrypted Virtualization (SEV).

            memory(Dict[Any, Any]): Required Memory related attributes of the instancetype.

              FIELDS:
                guest	<Object> -required-
                  Required amount of memory which is visible inside the guest OS.

                hugepages	<Object>
                  Optionally enables the use of hugepages for the VirtualMachineInstance
                  instead of regular memory.

                overcommitPercent	<integer>
                  OvercommitPercent is the percentage of the guest memory which will be
                  overcommitted. This means that the VMIs parent pod (virt-launcher) will
                  request less physical memory by a factor specified by the OvercommitPercent.
                  Overcommits can lead to memory exhaustion, which in turn can lead to
                  crashes. Use carefully. Defaults to 0

            node_selector(Dict[Any, Any]): NodeSelector is a selector which must be true for the vmi to fit on a node.
              Selector which must match a node's labels for the vmi to be scheduled on
              that node. More info:
              https://kubernetes.io/docs/concepts/configuration/assign-pod-node/
               NodeSelector is the name of the custom node selector for the instancetype.

            scheduler_name(str): If specified, the VMI will be dispatched by specified scheduler. If not
              specified, the VMI will be dispatched by default scheduler.
               SchedulerName is the name of the custom K8s scheduler for the instancetype.

        """
        super().__init__(**kwargs)

        self.annotations = annotations
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

        if not self.yaml_file:
            if not all([
                self.cpu,
                self.memory,
            ]):
                raise MissingRequiredArgumentError(argument="cpu, memory")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            self.res["cpu"] = self.cpu
            self.res["memory"] = self.memory

            if self.annotations:
                _spec["annotations"] = self.annotations

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
