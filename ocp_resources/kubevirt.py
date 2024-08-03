# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class KubeVirt(NamespacedResource):
    """
    KubeVirt represents the object deploying all KubeVirt resources
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        certificate_rotate_strategy: Optional[Dict[str, Any]] = None,
        configuration: Optional[Dict[str, Any]] = None,
        customize_components: Optional[Dict[str, Any]] = None,
        image_pull_policy: Optional[str] = "",
        image_pull_secrets: Optional[List[Any]] = None,
        image_registry: Optional[str] = "",
        image_tag: Optional[str] = "",
        infra: Optional[Dict[str, Any]] = None,
        monitor_account: Optional[str] = "",
        monitor_namespace: Optional[str] = "",
        product_component: Optional[str] = "",
        product_name: Optional[str] = "",
        product_version: Optional[str] = "",
        service_monitor_namespace: Optional[str] = "",
        uninstall_strategy: Optional[str] = "",
        workload_update_strategy: Optional[Dict[str, Any]] = None,
        workloads: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            certificate_rotate_strategy(Dict[Any, Any]): <empty>
              FIELDS:
                selfSigned	<Object>
                  <no description>

            configuration(Dict[Any, Any]): holds kubevirt configurations.
              same as the virt-configMap

              FIELDS:
                additionalGuestMemoryOverheadRatio	<string>
                  AdditionalGuestMemoryOverheadRatio can be used to increase the
                  virtualization infrastructure
                  overhead. This is useful, since the calculation of this overhead is not
                  accurate and cannot
                  be entirely known in advance. The ratio that is being set determines by
                  which factor to increase
                  the overhead calculated by Kubevirt. A higher ratio means that the VMs would
                  be less compromised
                  by node pressures, but would mean that fewer VMs could be scheduled to a
                  node.
                  If not set, the default is 1.

                apiConfiguration	<Object>
                  ReloadableComponentConfiguration holds all generic k8s configuration options
                  which can
                  be reloaded by components without requiring a restart.

                architectureConfiguration	<Object>
                  <no description>

                autoCPULimitNamespaceLabelSelector	<Object>
                  When set, AutoCPULimitNamespaceLabelSelector will set a CPU limit on
                  virt-launcher for VMIs running inside
                  namespaces that match the label selector.
                  The CPU limit will equal the number of requested vCPUs.
                  This setting does not apply to VMIs with dedicated CPUs.

                controllerConfiguration	<Object>
                  ReloadableComponentConfiguration holds all generic k8s configuration options
                  which can
                  be reloaded by components without requiring a restart.

                cpuModel	<string>
                  <no description>

                cpuRequest	<Object>
                  <no description>

                defaultRuntimeClass	<string>
                  <no description>

                developerConfiguration	<Object>
                  DeveloperConfiguration holds developer options

                emulatedMachines	<[]string>
                  Deprecated. Use architectureConfiguration instead.

                evictionStrategy	<string>
                  EvictionStrategy defines at the cluster level if the VirtualMachineInstance
                  should be
                  migrated instead of shut-off in case of a node drain. If the
                  VirtualMachineInstance specific
                  field is set it overrides the cluster level one.

                handlerConfiguration	<Object>
                  ReloadableComponentConfiguration holds all generic k8s configuration options
                  which can
                  be reloaded by components without requiring a restart.

                imagePullPolicy	<string>
                  PullPolicy describes a policy for if/when to pull a container image

                ksmConfiguration	<Object>
                  KSMConfiguration holds the information regarding the enabling the KSM in the
                  nodes (if available).

                liveUpdateConfiguration	<Object>
                  LiveUpdateConfiguration holds defaults for live update features

                machineType	<string>
                  Deprecated. Use architectureConfiguration instead.

                mediatedDevicesConfiguration	<Object>
                  MediatedDevicesConfiguration holds information about MDEV types to be
                  defined, if available

                memBalloonStatsPeriod	<integer>
                  <no description>

                migrations	<Object>
                  MigrationConfiguration holds migration options.
                  Can be overridden for specific groups of VMs though migration policies.
                  Visit https://kubevirt.io/user-guide/operations/migration_policies/ for more
                  information.

                minCPUModel	<string>
                  <no description>

                network	<Object>
                  NetworkConfiguration holds network options

                obsoleteCPUModels	<map[string]boolean>
                  <no description>

                ovmfPath	<string>
                  Deprecated. Use architectureConfiguration instead.

                permittedHostDevices	<Object>
                  PermittedHostDevices holds information about devices allowed for passthrough

                seccompConfiguration	<Object>
                  SeccompConfiguration holds Seccomp configuration for Kubevirt components

                selinuxLauncherType	<string>
                  <no description>

                smbios	<Object>
                  <no description>

                supportContainerResources	<[]Object>
                  SupportContainerResources specifies the resource requirements for various
                  types of supporting containers such as container disks/virtiofs/sidecars and
                  hotplug attachment pods. If omitted a sensible default will be supplied.

                supportedGuestAgentVersions	<[]string>
                  deprecated

                tlsConfiguration	<Object>
                  TLSConfiguration holds TLS options

                virtualMachineInstancesPerNode	<integer>
                  <no description>

                virtualMachineOptions	<Object>
                  VirtualMachineOptions holds the cluster level information regarding the
                  virtual machine.

                vmRolloutStrategy	<string>
                  VMRolloutStrategy defines how changes to a VM object propagate to its VMI

                vmStateStorageClass	<string>
                  VMStateStorageClass is the name of the storage class to use for the PVCs
                  created to preserve VM state, like TPM.
                  The storage class must support RWX in filesystem mode.

                webhookConfiguration	<Object>
                  ReloadableComponentConfiguration holds all generic k8s configuration options
                  which can
                  be reloaded by components without requiring a restart.

            customize_components(Dict[Any, Any]): <empty>
              FIELDS:
                flags	<Object>
                  Configure the value used for deployment and daemonset resources

                patches	<[]Object>
                  <no description>

            image_pull_policy(str): The ImagePullPolicy to use.

            image_pull_secrets(List[Any]): The imagePullSecrets to pull the container images from
              Defaults to none
              LocalObjectReference contains enough information to let you locate the
              referenced object inside the same namespace.

              FIELDS:
                name	<string>
                  Name of the referent.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
                  TODO: Add other useful fields. apiVersion, kind, uid?

            image_registry(str): The image registry to pull the container images from
              Defaults to the same registry the operator's container image is pulled from.

            image_tag(str): The image tag to use for the continer images installed.
              Defaults to the same tag as the operator's container image.

            infra(Dict[Any, Any]): selectors and tolerations that should apply to KubeVirt infrastructure
              components

              FIELDS:
                nodePlacement	<Object>
                  nodePlacement describes scheduling configuration for specific
                  KubeVirt components

                replicas	<integer>
                  replicas indicates how many replicas should be created for each KubeVirt
                  infrastructure
                  component (like virt-api or virt-controller). Defaults to 2.
                  WARNING: this is an advanced feature that prevents auto-scaling for core
                  kubevirt components. Please use with caution!

            monitor_account(str): The name of the Prometheus service account that needs read-access to
              KubeVirt endpoints
              Defaults to prometheus-k8s

            monitor_namespace(str): The namespace Prometheus is deployed in
              Defaults to openshift-monitor

            product_component(str): Designate the apps.kubevirt.io/component label for KubeVirt components.
              Useful if KubeVirt is included as part of a product.
              If ProductComponent is not specified, the component label default value is
              kubevirt.

            product_name(str): Designate the apps.kubevirt.io/part-of label for KubeVirt components.
              Useful if KubeVirt is included as part of a product.
              If ProductName is not specified, the part-of label will be omitted.

            product_version(str): Designate the apps.kubevirt.io/version label for KubeVirt components.
              Useful if KubeVirt is included as part of a product.
              If ProductVersion is not specified, KubeVirt's version will be used.

            service_monitor_namespace(str): The namespace the service monitor will be deployed
               When ServiceMonitorNamespace is set, then we'll install the service monitor
              object in that namespace
              otherwise we will use the monitoring namespace.

            uninstall_strategy(str): Specifies if kubevirt can be deleted if workloads are still present.
              This is mainly a precaution to avoid accidental data loss

            workload_update_strategy(Dict[Any, Any]): WorkloadUpdateStrategy defines at the cluster level how to handle
              automated workload updates

              FIELDS:
                batchEvictionInterval	<string>
                  BatchEvictionInterval Represents the interval to wait before issuing the
                  next
                  batch of shutdowns


                  Defaults to 1 minute

                batchEvictionSize	<integer>
                  BatchEvictionSize Represents the number of VMIs that can be forced updated
                  per
                  the BatchShutdownInteral interval


                  Defaults to 10

                workloadUpdateMethods	<[]string>
                  WorkloadUpdateMethods defines the methods that can be used to disrupt
                  workloads
                  during automated workload updates.
                  When multiple methods are present, the least disruptive method takes
                  precedence over more disruptive methods. For example if both LiveMigrate and
                  Shutdown
                  methods are listed, only VMs which are not live migratable will be
                  restarted/shutdown


                  An empty list defaults to no automated workload updating

            workloads(Dict[Any, Any]): selectors and tolerations that should apply to KubeVirt workloads

              FIELDS:
                nodePlacement	<Object>
                  nodePlacement describes scheduling configuration for specific
                  KubeVirt components

                replicas	<integer>
                  replicas indicates how many replicas should be created for each KubeVirt
                  infrastructure
                  component (like virt-api or virt-controller). Defaults to 2.
                  WARNING: this is an advanced feature that prevents auto-scaling for core
                  kubevirt components. Please use with caution!

        """
        super().__init__(**kwargs)

        self.certificate_rotate_strategy = certificate_rotate_strategy
        self.configuration = configuration
        self.customize_components = customize_components
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.image_registry = image_registry
        self.image_tag = image_tag
        self.infra = infra
        self.monitor_account = monitor_account
        self.monitor_namespace = monitor_namespace
        self.product_component = product_component
        self.product_name = product_name
        self.product_version = product_version
        self.service_monitor_namespace = service_monitor_namespace
        self.uninstall_strategy = uninstall_strategy
        self.workload_update_strategy = workload_update_strategy
        self.workloads = workloads

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.certificate_rotate_strategy:
                _spec["certificateRotateStrategy"] = self.certificate_rotate_strategy

            if self.configuration:
                _spec["configuration"] = self.configuration

            if self.customize_components:
                _spec["customizeComponents"] = self.customize_components

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.image_pull_secrets:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.image_registry:
                _spec["imageRegistry"] = self.image_registry

            if self.image_tag:
                _spec["imageTag"] = self.image_tag

            if self.infra:
                _spec["infra"] = self.infra

            if self.monitor_account:
                _spec["monitorAccount"] = self.monitor_account

            if self.monitor_namespace:
                _spec["monitorNamespace"] = self.monitor_namespace

            if self.product_component:
                _spec["productComponent"] = self.product_component

            if self.product_name:
                _spec["productName"] = self.product_name

            if self.product_version:
                _spec["productVersion"] = self.product_version

            if self.service_monitor_namespace:
                _spec["serviceMonitorNamespace"] = self.service_monitor_namespace

            if self.uninstall_strategy:
                _spec["uninstallStrategy"] = self.uninstall_strategy

            if self.workload_update_strategy:
                _spec["workloadUpdateStrategy"] = self.workload_update_strategy

            if self.workloads:
                _spec["workloads"] = self.workloads
