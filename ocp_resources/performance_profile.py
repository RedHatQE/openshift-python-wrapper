from ocp_resources.resource import Resource


class PerformanceProfile(Resource):
    api_group = Resource.ApiGroup.PERFORMANCE_OPENSHIFT_IO

    def __init__(
        self,
        additional_kernel_args=None,
        cpu=None,
        globally_disable_irq_load_balancing=False,
        hugepages=None,
        machine_config_label=None,
        machine_config_pool_selector=None,
        net=None,
        node_selector=None,
        numa=None,
        real_time_kernel=None,
        workload_hints=None,
        **kwargs,
    ):
        """
        PerformanceProfile object. API reference:
        https://docs.openshift.com/container-platform/4.13/rest_api/node_apis/performanceprofile-performance-openshift-io-v2.html#performanceprofile-performance-openshift-io-v2

        Args (in .spec):
            additional_kernel_args (array of strings): Additional kernel arguments.
            cpu (dict): Set of CPU related parameters. For example:
                {
                    "isolated": "4-39,44-79",
                    "reserved": "0-3,40-43",
                }
            globally_disable_irq_load_balancing (bool, default: False): Toggles whether IRQ load balancing will be
                disabled for the Isolated CPU set.
            hugepages (dict): Defines a set of huge pages related parameters. It is possible to set huge pages with
                multiple size values at the same time.
            machine_config_label (dict): Defines the label to add to the MachineConfigs the operator creates.
                It has to be used in the MachineConfigSelector of the MachineConfigPool which targets this performance
                profile.
            machine_config_pool_selector (dict): Defines the MachineConfigPool label to use in the
                MachineConfigPoolSelector of resources like KubeletConfigs created by the operator.
            net (dict): Defines a set of network related features.
            numa (dict): Defines options related to topology aware affinities.
            real_time_kernel (dict):  Defines a set of real time kernel related parameters. RT kernel won’t be
                installed when not set.
            workload_hints (dict): Defines hints for different types of workloads.
        """

        super().__init__(**kwargs)
        self.additional_kernel_args = additional_kernel_args
        self.cpu = cpu
        self.globally_disable_irq_load_balancing = globally_disable_irq_load_balancing
        self.hugepages = hugepages
        self.machine_config_label = machine_config_label
        self.machine_config_pool_selector = machine_config_pool_selector
        self.net = net
        self.node_selector = node_selector
        self.numa = numa
        self.real_time_kernel = real_time_kernel
        self.workload_hints = workload_hints

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            manifest_spec = {}
            if self.additional_kernel_args:
                manifest_spec["additionalKernelArgs"] = self.additional_kernel_args

            if self.cpu:
                manifest_spec["cpu"] = self.cpu

            if self.globally_disable_irq_load_balancing:
                manifest_spec[
                    "globallyDisableIrqLoadBalancing"
                ] = self.globally_disable_irq_load_balancing

            if self.hugepages:
                manifest_spec["hugepages"] = self.hugepages

            if self.machine_config_label:
                manifest_spec["machineConfigLabel"] = self.machine_config_label

            if self.machine_config_pool_selector:
                manifest_spec[
                    "machineConfigPoolSelector"
                ] = self.machine_config_pool_selector

            if self.net:
                manifest_spec["net"] = self.net

            if self.numa:
                manifest_spec["numa"] = self.numa

            if self.real_time_kernel:
                manifest_spec["realTimeKernel"] = self.real_time_kernel

            if self.workload_hints:
                manifest_spec["workloadHints"] = self.workload_hints

            if self.node_selector:
                manifest_spec["nodeSelector"] = self.node_selector

            self.res.update({"spec": manifest_spec})
