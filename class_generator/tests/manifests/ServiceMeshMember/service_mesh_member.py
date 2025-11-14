# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class ServiceMeshMember(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.MAISTRA_IO

    def __init__(
        self,
        control_plane_ref: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            control_plane_ref (dict[str, Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.control_plane_ref = control_plane_ref

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.control_plane_ref is None:
                raise MissingRequiredArgumentError(argument="self.control_plane_ref")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["controlPlaneRef"] = self.control_plane_ref

    # End of generated code
