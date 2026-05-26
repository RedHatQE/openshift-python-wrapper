# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class StorageCluster(NamespacedResource):
    """
    StorageCluster represents a cluster including Ceph Cluster, NooBaa and all the storage and compute resources required.
    """

    api_group: str = NamespacedResource.ApiGroup.OCS_OPENSHIFT_IO

    def __init__(
        self,
        allow_remote_storage_consumers: bool | None = None,
        arbiter: dict[str, Any] | None = None,
        backing_storage_classes: list[Any] | None = None,
        csi: dict[str, Any] | None = None,
        enable_ceph_tools: bool | None = None,
        encryption: dict[str, Any] | None = None,
        external_storage: dict[str, Any] | None = None,
        flexible_scaling: bool | None = None,
        host_network: bool | None = None,
        instance_type: str | None = None,
        label_selector: dict[str, Any] | None = None,
        log_collector: Any | None = None,
        manage_nodes: bool | None = None,
        managed_resources: dict[str, Any] | None = None,
        mgr: dict[str, Any] | None = None,
        mirroring: dict[str, Any] | None = None,
        mon_data_dir_host_path: str | None = None,
        mon_pvc_template: dict[str, Any] | None = None,
        monitoring: dict[str, Any] | None = None,
        multi_cloud_gateway: dict[str, Any] | None = None,
        network: dict[str, Any] | None = None,
        nfs: dict[str, Any] | None = None,
        node_topologies: dict[str, Any] | None = None,
        overprovision_control: list[Any] | None = None,
        placement: dict[str, Any] | None = None,
        provider_api_server_service_type: str | None = None,
        resource_profile: str | None = None,
        resources: dict[str, Any] | None = None,
        storage_device_sets: list[Any] | None = None,
        version: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            allow_remote_storage_consumers (bool): AllowRemoteStorageConsumers Indicates that the OCS cluster should
              deploy the needed components to enable connections from remote
              consumers.

            arbiter (dict[str, Any]): ArbiterSpec specifies the storage cluster options related to arbiter.
              If Arbiter is enabled, ArbiterLocation in the NodeTopologies must
              be specified.

            backing_storage_classes (list[Any]): BackingStorageClasses is a list of storage classes that will be
              provisioned by the storagecluster controller to be used in
              storageDeviceSets section of the CR.

            csi (dict[str, Any]): CSIDriverSpec defines the CSI driver settings for the StorageCluster.

            enable_ceph_tools (bool): EnableCephTools toggles on whether or not the ceph tools pod should be
              deployed. Defaults to false

            encryption (dict[str, Any]): EncryptionSpec defines if encryption should be enabled for the Storage
              Cluster It is optional and defaults to false.

            external_storage (dict[str, Any]): ExternalStorage is optional and defaults to false. When set to true,
              OCS will connect to an external OCS Storage Cluster instead of
              provisioning one locally.

            flexible_scaling (bool): If enabled, sets the failureDomain to host, allowing devices to be
              distributed evenly across all nodes, regardless of distribution in
              zones or racks.

            host_network (bool): HostNetwork defaults to false

            instance_type (str): No field description from API

            label_selector (dict[str, Any]): LabelSelector is used to specify custom labels of nodes to run OCS on

            log_collector (Any): Logging represents loggings settings

            manage_nodes (bool): No field description from API

            managed_resources (dict[str, Any]): ManagedResources specifies how to deal with auxiliary resources
              reconciled with the StorageCluster

            mgr (dict[str, Any]): MgrSpec defines the settings for the Ceph Manager

            mirroring (dict[str, Any]): Mirroring specifies data mirroring configuration for the storage
              cluster. This configuration will only be applied to resources
              managed by the operator.

            mon_data_dir_host_path (str): No field description from API

            mon_pvc_template (dict[str, Any]): PersistentVolumeClaim is a user's request for and claim to a
              persistent volume

            monitoring (dict[str, Any]): Monitoring controls the configuration of resources for exposing OCS
              metrics

            multi_cloud_gateway (dict[str, Any]): MultiCloudGatewaySpec defines specific multi-cloud gateway
              configuration options

            network (dict[str, Any]): Network represents cluster network settings

            nfs (dict[str, Any]): NFSSpec defines specific nfs configuration options

            node_topologies (dict[str, Any]): NodeTopologies specifies the nodes available for the storage cluster,
              preferred failure domain and location for the arbiter resources.
              This is optional for non-arbiter clusters. For arbiter clusters,
              the arbiterLocation is required; failure domain and the node
              labels are optional. When the failure domain and the node labels
              are missing, the ocs-operator makes a best effort to determine
              them automatically.

            overprovision_control (list[Any]): OverprovisionControl specifies the allowed hard-limit PVs
              overprovisioning relative to the effective usable storage
              capacity.

            placement (dict[str, Any]): Placement is optional and used to specify placements of OCS components
              explicitly

            provider_api_server_service_type (str): ProviderAPIServerServiceType Indicates the ServiceType for OCS
              Provider API Server Service. The default ServiceType is derived
              from hostNetwork field.

            resource_profile (str): Resource Profile can be used to choose from a set of predefined
              resource profiles for the ceph daemons. We have 3 profiles lean:
              suitable for clusters with limited resources, balanced: suitable
              for most use cases, performance: suitable for clusters with high
              amount of resources.

            resources (dict[str, Any]): Resources follows the conventions of and is mapped to
              CephCluster.Spec.Resources

            storage_device_sets (list[Any]): No field description from API

            version (str): Version specifies the version of StorageCluster

        """
        super().__init__(**kwargs)

        self.allow_remote_storage_consumers = allow_remote_storage_consumers
        self.arbiter = arbiter
        self.backing_storage_classes = backing_storage_classes
        self.csi = csi
        self.enable_ceph_tools = enable_ceph_tools
        self.encryption = encryption
        self.external_storage = external_storage
        self.flexible_scaling = flexible_scaling
        self.host_network = host_network
        self.instance_type = instance_type
        self.label_selector = label_selector
        self.log_collector = log_collector
        self.manage_nodes = manage_nodes
        self.managed_resources = managed_resources
        self.mgr = mgr
        self.mirroring = mirroring
        self.mon_data_dir_host_path = mon_data_dir_host_path
        self.mon_pvc_template = mon_pvc_template
        self.monitoring = monitoring
        self.multi_cloud_gateway = multi_cloud_gateway
        self.network = network
        self.nfs = nfs
        self.node_topologies = node_topologies
        self.overprovision_control = overprovision_control
        self.placement = placement
        self.provider_api_server_service_type = provider_api_server_service_type
        self.resource_profile = resource_profile
        self.resources = resources
        self.storage_device_sets = storage_device_sets
        self.version = version

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.allow_remote_storage_consumers is not None:
                _spec["allowRemoteStorageConsumers"] = self.allow_remote_storage_consumers

            if self.arbiter is not None:
                _spec["arbiter"] = self.arbiter

            if self.backing_storage_classes is not None:
                _spec["backingStorageClasses"] = self.backing_storage_classes

            if self.csi is not None:
                _spec["csi"] = self.csi

            if self.enable_ceph_tools is not None:
                _spec["enableCephTools"] = self.enable_ceph_tools

            if self.encryption is not None:
                _spec["encryption"] = self.encryption

            if self.external_storage is not None:
                _spec["externalStorage"] = self.external_storage

            if self.flexible_scaling is not None:
                _spec["flexibleScaling"] = self.flexible_scaling

            if self.host_network is not None:
                _spec["hostNetwork"] = self.host_network

            if self.instance_type is not None:
                _spec["instanceType"] = self.instance_type

            if self.label_selector is not None:
                _spec["labelSelector"] = self.label_selector

            if self.log_collector is not None:
                _spec["logCollector"] = self.log_collector

            if self.manage_nodes is not None:
                _spec["manageNodes"] = self.manage_nodes

            if self.managed_resources is not None:
                _spec["managedResources"] = self.managed_resources

            if self.mgr is not None:
                _spec["mgr"] = self.mgr

            if self.mirroring is not None:
                _spec["mirroring"] = self.mirroring

            if self.mon_data_dir_host_path is not None:
                _spec["monDataDirHostPath"] = self.mon_data_dir_host_path

            if self.mon_pvc_template is not None:
                _spec["monPVCTemplate"] = self.mon_pvc_template

            if self.monitoring is not None:
                _spec["monitoring"] = self.monitoring

            if self.multi_cloud_gateway is not None:
                _spec["multiCloudGateway"] = self.multi_cloud_gateway

            if self.network is not None:
                _spec["network"] = self.network

            if self.nfs is not None:
                _spec["nfs"] = self.nfs

            if self.node_topologies is not None:
                _spec["nodeTopologies"] = self.node_topologies

            if self.overprovision_control is not None:
                _spec["overprovisionControl"] = self.overprovision_control

            if self.placement is not None:
                _spec["placement"] = self.placement

            if self.provider_api_server_service_type is not None:
                _spec["providerAPIServerServiceType"] = self.provider_api_server_service_type

            if self.resource_profile is not None:
                _spec["resourceProfile"] = self.resource_profile

            if self.resources is not None:
                _spec["resources"] = self.resources

            if self.storage_device_sets is not None:
                _spec["storageDeviceSets"] = self.storage_device_sets

            if self.version is not None:
                _spec["version"] = self.version

    # End of generated code
