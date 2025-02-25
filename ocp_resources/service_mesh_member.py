# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ServiceMeshMember(NamespacedResource):
    """
    ServiceMeshMember provide a way for administrators to delegate permissions to add projects to a service mesh,
    even when the respective users do not have direct access to the service mesh project or member roll.
    """

    api_group: str = NamespacedResource.ApiGroup.MAISTRA_IO

    def __init__(
        self,
        control_plane_ref: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            control_plane_ref (Dict[str, Any]): Dict with `ServiceMeshControlPlane` information.

        """
        super().__init__(**kwargs)

        self.control_plane_ref = control_plane_ref

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.control_plane_ref:
                raise MissingRequiredArgumentError(argument="self.control_plane_ref")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["controlPlaneRef"] = self.control_plane_ref

    # End of generated code
