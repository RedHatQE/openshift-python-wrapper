# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class MaaSModel(NamespacedResource):
    """
    MaaSModel is the Schema for the maasmodels API
    """

    api_group: str = NamespacedResource.ApiGroup.MAAS_OPENDATAHUB_IO

    def __init__(
        self,
        model_ref: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            model_ref (dict[str, Any]): ModelRef references the actual model endpoint

        """
        super().__init__(**kwargs)

        self.model_ref = model_ref

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.model_ref is None:
                raise MissingRequiredArgumentError(argument="self.model_ref")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["modelRef"] = self.model_ref

    # End of generated code
