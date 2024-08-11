# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import NamespacedResource


class VirtualMachineInstancePreset(NamespacedResource):
    """
    Deprecated for removal in v2, please use VirtualMachineInstanceType and
    VirtualMachinePreference instead.
     VirtualMachineInstancePreset defines a VMI spec.domain to be applied to all
    VMIs that match the provided label selector More info:
    https://kubevirt.io/user-guide/virtual_machines/presets/#overrides
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
