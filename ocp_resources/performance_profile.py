from ocp_resources.resource import MissingRequiredArgumentError, Resource


class PerformanceProfile(Resource):
    api_group = Resource.ApiGroup.PERFORMANCE_OPENSHIFT_IO

    def __init__(
        self,
        additional_kernel_args=None,
        cpu=None,
        globally_disable_irq_load_balancing=None,
        hugepages=None,
        machine_config_label=None,
        machine_config_pool_selector=None,
        net=None,
        numa=None,
        real_time_kernel=None,
        workload_hints=None,
        **kwargs,
    ):
        """
        PerformanceProfile object. API reference:
        https://docs.openshift.com/container-platform/4.14/rest_api/node_apis/performanceprofile-performance-openshift-io-v2.html#performanceprofile-performance-openshift-io-v2

        Args:
            additional_kernel_args (list, optional): Additional kernel arguments.
            cpu (dict, required): Set of CPU related parameters.
            globally_disable_irq_load_balancing (bool, optional): Toggles whether IRQ load balancing will be
                disabled for the Isolated CPU set.
            hugepages (dict, optional): Defines a set of huge pages related parameters.
            machine_config_label (str, optional): Defines the label to add to the MachineConfigs the operator creates.
            machine_config_pool_selector (str, optional): Defines the MachineConfigPool label to use in the
                MachineConfigPoolSelector of resources like KubeletConfigs created by the operator.
            net (dict, optional): Defines a set of network related features.
            node_selector (str, required): Defines the node label to use in the NodeSelectors of resources like Tuned created by the operator.
            numa (dict, optional): Defines options related to topology aware affinities.
            real_time_kernel (dict, optional):  Defines a set of real time kernel related parameters.
            workload_hints (dict, optional): Defines hints for different types of workloads.
        """

        super().__init__(**kwargs)
        self.additional_kernel_args = additional_kernel_args
        self.cpu = cpu
        self.globally_disable_irq_load_balancing = globally_disable_irq_load_balancing
        self.hugepages = hugepages
        self.machine_config_label = machine_config_label
        self.machine_config_pool_selector = machine_config_pool_selector
        self.net = net
        self.node_selector = kwargs.get("node_selector")
        self.numa = numa
        self.real_time_kernel = real_time_kernel
        self.workload_hints = workload_hints

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.cpu and not self.node_selector:
                raise MissingRequiredArgumentError(argument="'cpu' and 'node_selector'")

            manifest_spec = {
                "cpu": self.cpu,
                "nodeSelector": self.node_selector,
            }

            if self.additional_kernel_args:
                manifest_spec["additionalKernelArgs"] = self.additional_kernel_args

            if self.globally_disable_irq_load_balancing is not None:
                manifest_spec["globallyDisableIrqLoadBalancing"] = self.globally_disable_irq_load_balancing

            if self.hugepages:
                manifest_spec["hugepages"] = self.hugepages

            if self.machine_config_label:
                manifest_spec["machineConfigLabel"] = self.machine_config_label

            if self.machine_config_pool_selector:
                manifest_spec["machineConfigPoolSelector"] = self.machine_config_pool_selector

            if self.net:
                manifest_spec["net"] = self.net

            if self.numa:
                manifest_spec["numa"] = self.numa

            if self.real_time_kernel:
                manifest_spec["realTimeKernel"] = self.real_time_kernel

            if self.workload_hints:
                manifest_spec["workloadHints"] = self.workload_hints

            self.res["spec"] = manifest_spec
