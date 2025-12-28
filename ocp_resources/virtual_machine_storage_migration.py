# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class VirtualMachineStorageMigration(NamespacedResource):
    """
    VirtualMachineStorageMigration is the Schema for the virtualmachinestoragemigrations API
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATIONS_KUBEVIRT_IO

    def __init__(
        self,
        virtual_machine_storage_migration_plan_ref: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            virtual_machine_storage_migration_plan_ref (dict[str, Any]): ObjectReference contains enough information to let you inspect or
              modify the referred object.

        """
        super().__init__(**kwargs)

        self.virtual_machine_storage_migration_plan_ref = virtual_machine_storage_migration_plan_ref

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.virtual_machine_storage_migration_plan_ref is None:
                raise MissingRequiredArgumentError(argument="self.virtual_machine_storage_migration_plan_ref")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["virtualMachineStorageMigrationPlanRef"] = self.virtual_machine_storage_migration_plan_ref

    # End of generated code
