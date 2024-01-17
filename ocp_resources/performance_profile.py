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
        https://docs.openshift.com/container-platform/4.14/rest_api/node_apis/performanceprofile-performance-openshift-io-v2.html#performanceprofile-performance-openshift-io-v2

        Args:
            additional_kernel_args (list): Additional kernel arguments.
            cpu (dict, required): Set of CPU related parameters. Expected key-values for dict are:
                    balanceIsolated (bool, default: True): Defines whether Isolated CPU set is eligible for load balancing workloads.
                    isolated (str, required): set of CPUs to be provided to application threads for most execution time as possible.
                    offlined (str): set of CPUs that will be unused and set offline.
                    reserved (str, required): set of CPUs that will not be used for any container workloads initiated by kubelet.
            globally_disable_irq_load_balancing (bool, default: False): Toggles whether IRQ load balancing will be
                disabled for the Isolated CPU set.
            hugepages (dict): Defines a set of huge pages related parameters. Expected key-values for dict are:
                defaultHugepagesSize (str): huge pages default size.
                pages (dict): Expected key-values for dic are:
                    count (int): amount of huge pages.
                    node (int): Defines the NUMA node where hugepages will be allocated.
                    size (str): huge page size.
            machine_config_label (str): Defines the label to add to the MachineConfigs the operator creates.
            machine_config_pool_selector (str): Defines the MachineConfigPool label to use in the
                MachineConfigPoolSelector of resources like KubeletConfigs created by the operator.
            net (dict): Defines a set of network related features. Expected key-values are:
                devices: (dict). Expected key-values are:
                    deviceID (str): Network device ID represented by 16 digit hexadecimal number.
                    interfaceName (str): Network device name to be matched.
                    vendorID (str): Network device vendor ID represented by 16 digit hexadecimal number.
                userLevelNetworking (boolean, default: False): when enabled sets either all or specified network devices queue size to the amount of reserved CPUs.
            node_selector (str, required): Defines the node label to use in the NodeSelectors of resources like Tuned created by the operator.
            numa (dict): Defines options related to topology aware affinities. Expected key-values are:
                topologyPolicy (str): Name of the policy when TopologyManager is enabled.
            real_time_kernel (dict):  Defines a set of real time kernel related parameters. Expected key-values are:
                enabled (boolean, default: False): Defines if the real time kernel packages should be installed.
            workload_hints (dict): Defines hints for different types of workloads. Expected key-values are:
                highPowerConsumption (boolean, default: False): Defines if the node should be configured for high power consumption.
                mixedCpus (boolean, default: False): Enables mixed-cpu-node-plugin on the node if set.
                perPodPowerManagement (boolean, default: False): Defines if the node should be configured for per pod power management.
                realTime (boolean, default: True): Defines if the node should be configured for real time workload.
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
                manifest_spec["globallyDisableIrqLoadBalancing"] = self.globally_disable_irq_load_balancing

            if self.hugepages:
                manifest_spec["hugepages"] = self.hugepages

            if self.machine_config_label:
                manifest_spec["machineConfigLabel"] = self.machine_config_label

            if self.machine_config_pool_selector:
                manifest_spec["machineConfigPoolSelector"] = self.machine_config_pool_selector

            if self.net:
                manifest_spec["net"] = self.net

            if self.node_selector:
                manifest_spec["nodeSelector"] = self.node_selector

            if self.numa:
                manifest_spec["numa"] = self.numa

            if self.real_time_kernel:
                manifest_spec["realTimeKernel"] = self.real_time_kernel

            if self.workload_hints:
                manifest_spec["workloadHints"] = self.workload_hints

            self.res.update({"spec": manifest_spec})
