# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class VirtualMachineBackupTracker(NamespacedResource):
    """
        VirtualMachineBackupTracker defines the way to track the latest checkpoint of
    a backup solution for a vm
    """

    api_group: str = NamespacedResource.ApiGroup.BACKUP_KUBEVIRT_IO

    def __init__(
        self,
        source: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            source (dict[str, Any]): Source specifies the VM that this backupTracker is associated with

        """
        super().__init__(**kwargs)

        self.source = source

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.source is None:
                raise MissingRequiredArgumentError(argument="self.source")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["source"] = self.source

    # End of generated code
