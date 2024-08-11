# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import Resource


class VirtualMachineClusterPreference(Resource):
    """
    VirtualMachineClusterPreference is a cluster scoped version of the
    VirtualMachinePreference resource.
    """

    api_group: str = Resource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
