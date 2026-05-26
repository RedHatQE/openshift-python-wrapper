# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class MigPlan(NamespacedResource):
    """
    MigPlan is the Schema for the migplans API
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATION_OPENSHIFT_IO

    def __init__(
        self,
        closed: bool | None = None,
        dest_mig_cluster_ref: dict[str, Any] | None = None,
        hooks: list[Any] | None = None,
        included_resources: list[Any] | None = None,
        indirect_image_migration: bool | None = None,
        indirect_volume_migration: bool | None = None,
        label_selector: dict[str, Any] | None = None,
        live_migrate: bool | None = None,
        mig_storage_ref: dict[str, Any] | None = None,
        namespaces: list[Any] | None = None,
        persistent_volumes: list[Any] | None = None,
        refresh: bool | None = None,
        src_mig_cluster_ref: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            closed (bool): If the migration was successful for a migplan, this value can be set
              True indicating that after one successful migration no new
              migrations can be carried out for this migplan.

            dest_mig_cluster_ref (dict[str, Any]): ObjectReference contains enough information to let you inspect or
              modify the referred object. --- New uses of this type are
              discouraged because of difficulty describing its usage when
              embedded in APIs.  1. Ignored fields.  It includes many fields
              which are not generally honored.  For instance, ResourceVersion
              and FieldPath are both very rarely valid in actual usage.  2.
              Invalid usage help.  It is impossible to add specific help for
              individual usage.  In most embedded usages, there are particular
              restrictions like, "must refer only to types A and B" or "UID not
              honored" or "name must be restricted".     Those cannot be well
              described when embedded.  3. Inconsistent validation.  Because the
              usages are different, the validation rules are different by usage,
              which makes it hard for users to predict what will happen.  4. The
              fields are both imprecise and overly precise.  Kind is not a
              precise mapping to a URL. This can produce ambiguity     during
              interpretation and require a REST mapping.  In most cases, the
              dependency is on the group,resource tuple     and the version of
              the actual struct is irrelevant.  5. We cannot easily change it.
              Because this type is embedded in many locations, updates to this
              type     will affect numerous schemas.  Don't make new APIs embed
              an underspecified API type they do not control.   Instead of using
              this type, create a locally provided and used type that is well-
              focused on your reference. For example, ServiceReferences for
              admission registration: https://github.com/kubernetes/api/blob/rel
              ease-1.17/admissionregistration/v1/types.go#L533 .

            hooks (list[Any]): Holds a reference to a MigHook along with the desired phase to run it
              in.

            included_resources (list[Any]): IncludedResources optional list of included resources in Velero Backup
              When not set, all the resources are included in the backup

            indirect_image_migration (bool): If set True, disables direct image migrations.

            indirect_volume_migration (bool): If set True, disables direct volume migrations.

            label_selector (dict[str, Any]): LabelSelector optional label selector on the included resources in
              Velero Backup

            live_migrate (bool): LiveMigrate optional flag to enable live migration of VMs during
              direct volume migration Only running VMs when the plan is executed
              will be live migrated

            mig_storage_ref (dict[str, Any]): ObjectReference contains enough information to let you inspect or
              modify the referred object. --- New uses of this type are
              discouraged because of difficulty describing its usage when
              embedded in APIs.  1. Ignored fields.  It includes many fields
              which are not generally honored.  For instance, ResourceVersion
              and FieldPath are both very rarely valid in actual usage.  2.
              Invalid usage help.  It is impossible to add specific help for
              individual usage.  In most embedded usages, there are particular
              restrictions like, "must refer only to types A and B" or "UID not
              honored" or "name must be restricted".     Those cannot be well
              described when embedded.  3. Inconsistent validation.  Because the
              usages are different, the validation rules are different by usage,
              which makes it hard for users to predict what will happen.  4. The
              fields are both imprecise and overly precise.  Kind is not a
              precise mapping to a URL. This can produce ambiguity     during
              interpretation and require a REST mapping.  In most cases, the
              dependency is on the group,resource tuple     and the version of
              the actual struct is irrelevant.  5. We cannot easily change it.
              Because this type is embedded in many locations, updates to this
              type     will affect numerous schemas.  Don't make new APIs embed
              an underspecified API type they do not control.   Instead of using
              this type, create a locally provided and used type that is well-
              focused on your reference. For example, ServiceReferences for
              admission registration: https://github.com/kubernetes/api/blob/rel
              ease-1.17/admissionregistration/v1/types.go#L533 .

            namespaces (list[Any]): Holds names of all the namespaces to be included in migration.

            persistent_volumes (list[Any]): No field description from API

            refresh (bool): If set True, the controller is forced to check if the migplan is in
              Ready state or not.

            src_mig_cluster_ref (dict[str, Any]): ObjectReference contains enough information to let you inspect or
              modify the referred object. --- New uses of this type are
              discouraged because of difficulty describing its usage when
              embedded in APIs.  1. Ignored fields.  It includes many fields
              which are not generally honored.  For instance, ResourceVersion
              and FieldPath are both very rarely valid in actual usage.  2.
              Invalid usage help.  It is impossible to add specific help for
              individual usage.  In most embedded usages, there are particular
              restrictions like, "must refer only to types A and B" or "UID not
              honored" or "name must be restricted".     Those cannot be well
              described when embedded.  3. Inconsistent validation.  Because the
              usages are different, the validation rules are different by usage,
              which makes it hard for users to predict what will happen.  4. The
              fields are both imprecise and overly precise.  Kind is not a
              precise mapping to a URL. This can produce ambiguity     during
              interpretation and require a REST mapping.  In most cases, the
              dependency is on the group,resource tuple     and the version of
              the actual struct is irrelevant.  5. We cannot easily change it.
              Because this type is embedded in many locations, updates to this
              type     will affect numerous schemas.  Don't make new APIs embed
              an underspecified API type they do not control.   Instead of using
              this type, create a locally provided and used type that is well-
              focused on your reference. For example, ServiceReferences for
              admission registration: https://github.com/kubernetes/api/blob/rel
              ease-1.17/admissionregistration/v1/types.go#L533 .

        """
        super().__init__(**kwargs)

        self.closed = closed
        self.dest_mig_cluster_ref = dest_mig_cluster_ref
        self.hooks = hooks
        self.included_resources = included_resources
        self.indirect_image_migration = indirect_image_migration
        self.indirect_volume_migration = indirect_volume_migration
        self.label_selector = label_selector
        self.live_migrate = live_migrate
        self.mig_storage_ref = mig_storage_ref
        self.namespaces = namespaces
        self.persistent_volumes = persistent_volumes
        self.refresh = refresh
        self.src_mig_cluster_ref = src_mig_cluster_ref

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.closed is not None:
                _spec["closed"] = self.closed

            if self.dest_mig_cluster_ref is not None:
                _spec["destMigClusterRef"] = self.dest_mig_cluster_ref

            if self.hooks is not None:
                _spec["hooks"] = self.hooks

            if self.included_resources is not None:
                _spec["includedResources"] = self.included_resources

            if self.indirect_image_migration is not None:
                _spec["indirectImageMigration"] = self.indirect_image_migration

            if self.indirect_volume_migration is not None:
                _spec["indirectVolumeMigration"] = self.indirect_volume_migration

            if self.label_selector is not None:
                _spec["labelSelector"] = self.label_selector

            if self.live_migrate is not None:
                _spec["liveMigrate"] = self.live_migrate

            if self.mig_storage_ref is not None:
                _spec["migStorageRef"] = self.mig_storage_ref

            if self.namespaces is not None:
                _spec["namespaces"] = self.namespaces

            if self.persistent_volumes is not None:
                _spec["persistentVolumes"] = self.persistent_volumes

            if self.refresh is not None:
                _spec["refresh"] = self.refresh

            if self.src_mig_cluster_ref is not None:
                _spec["srcMigClusterRef"] = self.src_mig_cluster_ref

    # End of generated code
