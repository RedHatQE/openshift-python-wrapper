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
        retention_policy: str | None = None,
        virtual_machines: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            retention_policy (str): RetentionPolicy indicates whether to keep or delete the source
              DataVolume/PVC after each VM migration completes. When
              "keepSource" (default), the source is preserved. When
              "deleteSource", the source DataVolume is deleted if it exists,
              otherwise the source PVC is deleted.

            virtual_machines (list[Any]): The virtual machines to migrate.

        """
        super().__init__(**kwargs)

        self.retention_policy = retention_policy
        self.virtual_machines = virtual_machines

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.virtual_machines is None:
                raise MissingRequiredArgumentError(argument="self.virtual_machines")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["virtualMachines"] = self.virtual_machines

            if self.retention_policy is not None:
                _spec["retentionPolicy"] = self.retention_policy

    # End of generated code
