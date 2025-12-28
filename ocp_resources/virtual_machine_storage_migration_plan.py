# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class VirtualMachineStorageMigrationPlan(NamespacedResource):
    """
    VirtualMachineStorageMigrationPlan is the Schema for the virtualmachinestoragemigrationplans API
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATIONS_KUBEVIRT_IO

    def __init__(
        self,
        virtual_machines: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            virtual_machines (list[Any]): The virtual machines to migrate.

        """
        super().__init__(**kwargs)

        self.virtual_machines = virtual_machines

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.virtual_machines is None:
                raise MissingRequiredArgumentError(argument="self.virtual_machines")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["virtualMachines"] = self.virtual_machines

    # End of generated code
