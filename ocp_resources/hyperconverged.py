# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class HyperConverged(NamespacedResource):
    """
    HyperConverged is the Schema for the hyperconvergeds API
    """

    api_group: str = NamespacedResource.ApiGroup.HCO_KUBEVIRT_IO

    def __init__(
        self,
        deployment: dict[str, Any] | None = None,
        feature_gates: list[Any] | None = None,
        networking: dict[str, Any] | None = None,
        security: dict[str, Any] | None = None,
        storage: dict[str, Any] | None = None,
        virtualization: dict[str, Any] | None = None,
        workload_sources: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            deployment (dict[str, Any]): Deployment contains all the configurations related to deployment of
              KubeVirt components

            feature_gates (list[Any]): FeatureGates is a set of optional feature gates to enable or disable
              new features that are not generally available yet. Add a new
              FeatureGate Object to this set, to enable a feature that is
              disabled by default, or to disable a feature that is enabled by
              default.  A feature gate may be in the following phases: * alpha:
              the feature is in dev-preview. It is disabled by default, but can
              be enabled. * beta: the feature gate is in tech-preview. It is
              enabled by default, but   can be disabled. * GA: the feature is
              graduated and is always enabled. There is no way to   disable it.
              * deprecated: the feature is deprecated. The feature gate will be
              removed in a future release.  Feature-Gate list: *
              decentralizedLiveMigration:   DecentralizedLiveMigration enables
              the decentralized live migration   (cross-cluster migration)
              feature. This feature allows live migration of
              VirtualMachineInstances between different clusters. This feature
              is in   Developer Preview.   Phase: beta  *
              declarativeHotplugVolumes:   DeclarativeHotplugVolumes enables the
              use of the declarative volume   hotplug feature in KubeVirt. When
              set to true or nil, the   "DeclarativeHotplugVolumes" feature gate
              is enabled and the   "HotplugVolumes" feature gate is not (default
              behavior). When set to   false, the "HotplugVolumes" featuregate
              is enabled in KubeVirt. This   feature is in Technical Preview.
              Phase: beta  * template:   VirtualMachine Templates provide a
              native, in-cluster VM templating for   KubeVirt. They allow you to
              define reusable VM blueprints with   parameterized values that can
              be processed to create virtual machine. the   "template" feature
              gate enables this feature. Note: this feature is in   Tech
              Preview.   Phase: beta  * alignCPUs:   Enable KubeVirt to request
              up to two additional dedicated CPUs in order to   complete the
              total CPU count to an even parity when using emulator thread
              isolation. Note: this feature is in Developer Preview.   Phase:
              alpha  * containerPathVolumes:   ContainerPathVolumes enables the
              use of container paths as volumes in   KubeVirt. This allows VMs
              to access files and directories from the   virt-launcher pod's
              filesystem via virtiofs.   Phase: alpha  * deployKubeSecondaryDNS:
              Deploy KubeSecondaryDNS by CNAO   Phase: alpha  *
              deployObservabilityController:   Deploy the virt-observability-
              controller component. When enabled, the   controller exposes
              KubeVirt metrics and manages PrometheusRule resources
              independently from the KubeVirt control plane.   Phase: alpha  *
              downwardMetrics:   Allow to expose a limited set of host metrics
              to guests.   Phase: alpha  * enableMultiArchBootImageImport:
              EnableMultiArchBootImageImport allows the HCO to run on
              heterogeneous   clusters with different CPU architectures. Setting
              this field to true will   allow the HCO to create Golden Images
              for different CPU architectures.   This feature is in Developer
              Preview.   Phase: alpha  * incrementalBackup:   IncrementalBackup
              enables changed block tracking backups and incremental   backups
              using QEMU capabilities in KubeVirt. When enabled, this also
              enables the UtilityVolumes feature gate in the KubeVirt CR. Note:
              This   feature is in Tech Preview.   Phase: alpha  * objectGraph:
              ObjectGraph enables the ObjectGraph VM and VMI subresource in
              KubeVirt.   This subresource returns a structured list of k8s
              objects that are related   to the specified VM or VMI, enabling
              better dependency tracking. Note:   This feature is in Developer
              Preview.   Phase: alpha  * disableMDevConfiguration:   Deprecated:
              use spec.virtualization.mediatedDevicesConfiguration.enabled
              instead. This feature gate is deprecated and will be removed in a
              future   release.   Phase: deprecated  * persistentReservation:
              This feature gate has graduated to a dedicated configuration
              field. Use
              spec.storage.persistentReservationConfiguration.enabled instead.
              This   feature gate is deprecated and will be removed in a future
              release.   Phase: deprecated

            networking (dict[str, Any]): Networking contains all the configurations for networking

            security (dict[str, Any]): Security contains all the security configurations

            storage (dict[str, Any]): Storage contains all the configurations for storage

            virtualization (dict[str, Any]): Virtualization contains all the configurations for virtualization

            workload_sources (dict[str, Any]): WorkloadSources contains all the configurations for workload sources

        """
        super().__init__(**kwargs)

        self.deployment = deployment
        self.feature_gates = feature_gates
        self.networking = networking
        self.security = security
        self.storage = storage
        self.virtualization = virtualization
        self.workload_sources = workload_sources

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.deployment is not None:
                _spec["deployment"] = self.deployment

            if self.feature_gates is not None:
                _spec["featureGates"] = self.feature_gates

            if self.networking is not None:
                _spec["networking"] = self.networking

            if self.security is not None:
                _spec["security"] = self.security

            if self.storage is not None:
                _spec["storage"] = self.storage

            if self.virtualization is not None:
                _spec["virtualization"] = self.virtualization

            if self.workload_sources is not None:
                _spec["workloadSources"] = self.workload_sources

    # End of generated code
