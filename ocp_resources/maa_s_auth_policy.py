# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class MaaSAuthPolicy(NamespacedResource):
    """
    MaaSAuthPolicy is the Schema for the maasauthpolicies API
    """

    api_group: str = NamespacedResource.ApiGroup.MAAS_OPENDATAHUB_IO

    def __init__(
        self,
        metering_metadata: dict[str, Any] | None = None,
        model_refs: list[Any] | None = None,
        subjects: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            metering_metadata (dict[str, Any]): MeteringMetadata contains billing and tracking information

            model_refs (list[Any]): ModelRefs is a list of model names that this policy grants access to

            subjects (dict[str, Any]): Subjects defines who has access (OR logic - any match grants access)

        """
        super().__init__(**kwargs)

        self.metering_metadata = metering_metadata
        self.model_refs = model_refs
        self.subjects = subjects

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.model_refs is None:
                raise MissingRequiredArgumentError(argument="self.model_refs")

            if self.subjects is None:
                raise MissingRequiredArgumentError(argument="self.subjects")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["modelRefs"] = self.model_refs
            _spec["subjects"] = self.subjects

            if self.metering_metadata is not None:
                _spec["meteringMetadata"] = self.metering_metadata

    # End of generated code
