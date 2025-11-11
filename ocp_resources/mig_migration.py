# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class MigMigration(NamespacedResource):
    """
    MigMigration is the Schema for the migmigrations API
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATION_OPENSHIFT_IO

    def __init__(
        self,
        canceled: bool | None = None,
        keep_annotations: bool | None = None,
        mig_plan_ref: dict[str, Any] | None = None,
        migrate_state: bool | None = None,
        quiesce_pods: bool | None = None,
        rollback: bool | None = None,
        run_as_group: int | None = None,
        run_as_root: bool | None = None,
        run_as_user: int | None = None,
        stage: bool | None = None,
        verify: bool | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            canceled (bool): Invokes the cancel migration operation, when set to true the migration
              controller switches to cancel itinerary. This field can be used
              on-demand to cancel the running migration.

            keep_annotations (bool): Specifies whether to retain the annotations set by the migration
              controller or not.

            mig_plan_ref (dict[str, Any]): ObjectReference contains enough information to let you inspect or
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

            migrate_state (bool): Invokes the state migration operation

            quiesce_pods (bool): Specifies whether to quiesce the application Pods before migrating
              Persistent Volume data.

            rollback (bool): Invokes the rollback migration operation, when set to true the
              migration controller switches to rollback itinerary. This field
              needs to be set prior to creation of a MigMigration.

            run_as_group (int): If set, runs rsync operations with provided group id. This provided
              user id should be a valid one that falls within the range of
              allowed GID of user namespace

            run_as_root (bool): If set True, run rsync operations with escalated privileged, takes
              precedence over setting RunAsUser and RunAsGroup

            run_as_user (int): If set, runs rsync operations with provided user id. This provided
              user id should be a valid one that falls within the range of
              allowed UID of user namespace

            stage (bool): Invokes the stage operation, when set to true the migration controller
              switches to stage itinerary. This is a required field.

            verify (bool): Specifies whether to verify the health of the migrated pods or not.

        """
        super().__init__(**kwargs)

        self.canceled = canceled
        self.keep_annotations = keep_annotations
        self.mig_plan_ref = mig_plan_ref
        self.migrate_state = migrate_state
        self.quiesce_pods = quiesce_pods
        self.rollback = rollback
        self.run_as_group = run_as_group
        self.run_as_root = run_as_root
        self.run_as_user = run_as_user
        self.stage = stage
        self.verify = verify

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.stage is None:
                raise MissingRequiredArgumentError(argument="self.stage")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["stage"] = self.stage

            if self.canceled is not None:
                _spec["canceled"] = self.canceled

            if self.keep_annotations is not None:
                _spec["keepAnnotations"] = self.keep_annotations

            if self.mig_plan_ref is not None:
                _spec["migPlanRef"] = self.mig_plan_ref

            if self.migrate_state is not None:
                _spec["migrateState"] = self.migrate_state

            if self.quiesce_pods is not None:
                _spec["quiescePods"] = self.quiesce_pods

            if self.rollback is not None:
                _spec["rollback"] = self.rollback

            if self.run_as_group is not None:
                _spec["runAsGroup"] = self.run_as_group

            if self.run_as_root is not None:
                _spec["runAsRoot"] = self.run_as_root

            if self.run_as_user is not None:
                _spec["runAsUser"] = self.run_as_user

            if self.verify is not None:
                _spec["verify"] = self.verify

    # End of generated code
