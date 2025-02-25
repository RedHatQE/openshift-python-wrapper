# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Optional
from ocp_resources.resource import NamespacedResource


class VirtualMachineInstanceMigration(NamespacedResource):
    """
        VirtualMachineInstanceMigration represents the object tracking a VMI's migration
    to another host in the cluster
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        vmi_name: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            vmi_name (str): The name of the VMI to perform the migration on. VMI must exist in the
              migration objects namespace

        """
        super().__init__(**kwargs)

        self.vmi_name = vmi_name

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.vmi_name:
                _spec["vmiName"] = self.vmi_name

    # End of generated code
