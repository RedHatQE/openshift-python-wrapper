# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):
    """
        Backup is a Velero resource that represents the capture of Kubernetes
    cluster state at a point in time (API objects and associated volume state).
    """

    api_group: str = NamespacedResource.ApiGroup.VELERO_IO

    def __init__(
        self,
        csi_snapshot_timeout: str | None = None,
        datamover: str | None = None,
        default_volumes_to_fs_backup: bool | None = None,
        default_volumes_to_restic: bool | None = None,
        excluded_cluster_scoped_resources: list[Any] | None = None,
        excluded_namespace_scoped_resources: list[Any] | None = None,
        excluded_namespaces: list[Any] | None = None,
        excluded_resources: list[Any] | None = None,
        hooks: dict[str, Any] | None = None,
        include_cluster_resources: bool | None = None,
        included_cluster_scoped_resources: list[Any] | None = None,
        included_namespace_scoped_resources: list[Any] | None = None,
        included_namespaces: list[Any] | None = None,
        included_resources: list[Any] | None = None,
        item_operation_timeout: str | None = None,
        label_selector: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        or_label_selectors: list[Any] | None = None,
        ordered_resources: dict[str, Any] | None = None,
        resource_policy: dict[str, Any] | None = None,
        snapshot_move_data: bool | None = None,
        snapshot_volumes: bool | None = None,
        storage_location: str | None = None,
        ttl: str | None = None,
        uploader_config: dict[str, Any] | None = None,
        volume_snapshot_locations: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            csi_snapshot_timeout (str): CSISnapshotTimeout specifies the time used to wait for CSI
              VolumeSnapshot status turns to ReadyToUse during creation, before
              returning error as timeout. The default value is 10 minute.

            datamover (str): DataMover specifies the data mover to be used by the backup. If
              DataMover is "" or "velero", the built-in data mover will be used.

            default_volumes_to_fs_backup (bool): DefaultVolumesToFsBackup specifies whether pod volume file system
              backup should be used for all volumes by default.

            default_volumes_to_restic (bool): DefaultVolumesToRestic specifies whether restic should be used to take
              a backup of all pod volumes by default.  Deprecated: this field is
              no longer used and will be removed entirely in future. Use
              DefaultVolumesToFsBackup instead.

            excluded_cluster_scoped_resources (list[Any]): ExcludedClusterScopedResources is a slice of cluster-scoped resource
              type names to exclude from the backup. If set to "*", all cluster-
              scoped resource types are excluded. The default value is empty.


            excluded_namespace_scoped_resources (list[Any]): ExcludedNamespaceScopedResources is a slice of namespace-scoped
              resource type names to exclude from the backup. If set to "*", all
              namespace-scoped resource types are excluded. The default value is
              empty.

            excluded_namespaces (list[Any]): ExcludedNamespaces contains a list of namespaces that are not included
              in the backup.

            excluded_resources (list[Any]): ExcludedResources is a slice of resource names that are not included
              in the backup.

            hooks (dict[str, Any]): Hooks represent custom behaviors that should be executed at different
              phases of the backup.

            include_cluster_resources (bool): IncludeClusterResources specifies whether cluster-scoped resources
              should be included for consideration in the backup.

            included_cluster_scoped_resources (list[Any]): IncludedClusterScopedResources is a slice of cluster-scoped resource
              type names to include in the backup. If set to "*", all cluster-
              scoped resource types are included. The default value is empty,
              which means only related cluster-scoped resources are included.

            included_namespace_scoped_resources (list[Any]): IncludedNamespaceScopedResources is a slice of namespace-scoped
              resource type names to include in the backup. The default value is
              "*".

            included_namespaces (list[Any]): IncludedNamespaces is a slice of namespace names to include objects
              from. If empty, all namespaces are included.

            included_resources (list[Any]): IncludedResources is a slice of resource names to include in the
              backup. If empty, all resources are included.

            item_operation_timeout (str): ItemOperationTimeout specifies the time used to wait for asynchronous
              BackupItemAction operations The default value is 4 hour.

            label_selector (dict[str, Any]): LabelSelector is a metav1.LabelSelector to filter with when adding
              individual objects to the backup. If empty or nil, all objects are
              included. Optional.

            metadata (dict[str, Any]): No field description from API

            or_label_selectors (list[Any]): OrLabelSelectors is list of metav1.LabelSelector to filter with when
              adding individual objects to the backup. If multiple provided they
              will be joined by the OR operator. LabelSelector as well as
              OrLabelSelectors cannot co-exist in backup request, only one of
              them can be used.

            ordered_resources (dict[str, Any]): OrderedResources specifies the backup order of resources of specific
              Kind. The map key is the resource name and value is a list of
              object names separated by commas. Each resource name has format
              "namespace/objectname".  For cluster resources, simply use
              "objectname".

            resource_policy (dict[str, Any]): ResourcePolicy specifies the referenced resource policies that backup
              should follow

            snapshot_move_data (bool): SnapshotMoveData specifies whether snapshot data should be moved

            snapshot_volumes (bool): SnapshotVolumes specifies whether to take snapshots of any PV's
              referenced in the set of objects included in the Backup.

            storage_location (str): StorageLocation is a string containing the name of a
              BackupStorageLocation where the backup should be stored.

            ttl (str): TTL is a time.Duration-parseable string describing how long the Backup
              should be retained for.

            uploader_config (dict[str, Any]): UploaderConfig specifies the configuration for the uploader.

            volume_snapshot_locations (list[Any]): VolumeSnapshotLocations is a list containing names of
              VolumeSnapshotLocations associated with this backup.


        """
        super().__init__(**kwargs)

        self.csi_snapshot_timeout = csi_snapshot_timeout
        self.datamover = datamover
        self.default_volumes_to_fs_backup = default_volumes_to_fs_backup
        self.default_volumes_to_restic = default_volumes_to_restic
        self.excluded_cluster_scoped_resources = excluded_cluster_scoped_resources
        self.excluded_namespace_scoped_resources = excluded_namespace_scoped_resources
        self.excluded_namespaces = excluded_namespaces
        self.excluded_resources = excluded_resources
        self.hooks = hooks
        self.include_cluster_resources = include_cluster_resources
        self.included_cluster_scoped_resources = included_cluster_scoped_resources
        self.included_namespace_scoped_resources = included_namespace_scoped_resources
        self.included_namespaces = included_namespaces
        self.included_resources = included_resources
        self.item_operation_timeout = item_operation_timeout
        self.label_selector = label_selector
        self.metadata = metadata
        self.or_label_selectors = or_label_selectors
        self.ordered_resources = ordered_resources
        self.resource_policy = resource_policy
        self.snapshot_move_data = snapshot_move_data
        self.snapshot_volumes = snapshot_volumes
        self.storage_location = storage_location
        self.ttl = ttl
        self.uploader_config = uploader_config
        self.volume_snapshot_locations = volume_snapshot_locations

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.csi_snapshot_timeout is not None:
                _spec["csiSnapshotTimeout"] = self.csi_snapshot_timeout

            if self.datamover is not None:
                _spec["datamover"] = self.datamover

            if self.default_volumes_to_fs_backup is not None:
                _spec["defaultVolumesToFsBackup"] = self.default_volumes_to_fs_backup

            if self.default_volumes_to_restic is not None:
                _spec["defaultVolumesToRestic"] = self.default_volumes_to_restic

            if self.excluded_cluster_scoped_resources is not None:
                _spec["excludedClusterScopedResources"] = self.excluded_cluster_scoped_resources

            if self.excluded_namespace_scoped_resources is not None:
                _spec["excludedNamespaceScopedResources"] = self.excluded_namespace_scoped_resources

            if self.excluded_namespaces is not None:
                _spec["excludedNamespaces"] = self.excluded_namespaces

            if self.excluded_resources is not None:
                _spec["excludedResources"] = self.excluded_resources

            if self.hooks is not None:
                _spec["hooks"] = self.hooks

            if self.include_cluster_resources is not None:
                _spec["includeClusterResources"] = self.include_cluster_resources

            if self.included_cluster_scoped_resources is not None:
                _spec["includedClusterScopedResources"] = self.included_cluster_scoped_resources

            if self.included_namespace_scoped_resources is not None:
                _spec["includedNamespaceScopedResources"] = self.included_namespace_scoped_resources

            if self.included_namespaces is not None:
                _spec["includedNamespaces"] = self.included_namespaces

            if self.included_resources is not None:
                _spec["includedResources"] = self.included_resources

            if self.item_operation_timeout is not None:
                _spec["itemOperationTimeout"] = self.item_operation_timeout

            if self.label_selector is not None:
                _spec["labelSelector"] = self.label_selector

            if self.metadata is not None:
                _spec["metadata"] = self.metadata

            if self.or_label_selectors is not None:
                _spec["orLabelSelectors"] = self.or_label_selectors

            if self.ordered_resources is not None:
                _spec["orderedResources"] = self.ordered_resources

            if self.resource_policy is not None:
                _spec["resourcePolicy"] = self.resource_policy

            if self.snapshot_move_data is not None:
                _spec["snapshotMoveData"] = self.snapshot_move_data

            if self.snapshot_volumes is not None:
                _spec["snapshotVolumes"] = self.snapshot_volumes

            if self.storage_location is not None:
                _spec["storageLocation"] = self.storage_location

            if self.ttl is not None:
                _spec["ttl"] = self.ttl

            if self.uploader_config is not None:
                _spec["uploaderConfig"] = self.uploader_config

            if self.volume_snapshot_locations is not None:
                _spec["volumeSnapshotLocations"] = self.volume_snapshot_locations

    # End of generated code
