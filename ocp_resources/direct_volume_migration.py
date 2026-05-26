# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class DirectVolumeMigration(NamespacedResource):
    """
    DirectVolumeMigration is the Schema for the direct pv migration API
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATION_OPENSHIFT_IO

    def __init__(
        self,
        back_off_limit: int | None = None,
        create_destination_namespaces: bool | None = None,
        delete_progress_reporting_crs: bool | None = None,
        dest_mig_cluster_ref: dict[str, Any] | None = None,
        live_migrate: bool | None = None,
        migration_type: str | None = None,
        persistent_volume_claims: list[Any] | None = None,
        src_mig_cluster_ref: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            back_off_limit (int): BackOffLimit retry limit on Rsync pods

            create_destination_namespaces (bool): Set true to create namespaces in destination cluster

            delete_progress_reporting_crs (bool): Specifies if progress reporting CRs needs to be deleted or not

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

            live_migrate (bool): Specifies if any volumes associated with a VM should be live storage
              migrated instead of offline migrated

            migration_type (str): Specifies if this is the final DVM in the migration plan

            persistent_volume_claims (list[Any]):  Holds all the PVCs that are to be migrated with direct volume
              migration

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

        self.back_off_limit = back_off_limit
        self.create_destination_namespaces = create_destination_namespaces
        self.delete_progress_reporting_crs = delete_progress_reporting_crs
        self.dest_mig_cluster_ref = dest_mig_cluster_ref
        self.live_migrate = live_migrate
        self.migration_type = migration_type
        self.persistent_volume_claims = persistent_volume_claims
        self.src_mig_cluster_ref = src_mig_cluster_ref

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.back_off_limit is not None:
                _spec["backOffLimit"] = self.back_off_limit

            if self.create_destination_namespaces is not None:
                _spec["createDestinationNamespaces"] = self.create_destination_namespaces

            if self.delete_progress_reporting_crs is not None:
                _spec["deleteProgressReportingCRs"] = self.delete_progress_reporting_crs

            if self.dest_mig_cluster_ref is not None:
                _spec["destMigClusterRef"] = self.dest_mig_cluster_ref

            if self.live_migrate is not None:
                _spec["liveMigrate"] = self.live_migrate

            if self.migration_type is not None:
                _spec["migrationType"] = self.migration_type

            if self.persistent_volume_claims is not None:
                _spec["persistentVolumeClaims"] = self.persistent_volume_claims

            if self.src_mig_cluster_ref is not None:
                _spec["srcMigClusterRef"] = self.src_mig_cluster_ref

    # End of generated code
