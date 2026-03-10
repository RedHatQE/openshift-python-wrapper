# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class MaaSSubscription(NamespacedResource):
    """
    MaaSSubscription is the Schema for the maassubscriptions API
    """

    api_group: str = NamespacedResource.ApiGroup.MAAS_OPENDATAHUB_IO

    def __init__(
        self,
        model_refs: list[Any] | None = None,
        owner: dict[str, Any] | None = None,
        priority: int | None = None,
        token_metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            model_refs (list[Any]): ModelRefs defines which models are included with per-model token rate
              limits

            owner (dict[str, Any]): Owner defines who owns this subscription

            priority (int): Priority determines subscription priority when user has multiple
              subscriptions Higher numbers have higher priority. Defaults to 0.

            token_metadata (dict[str, Any]): TokenMetadata contains metadata for token attribution and metering

        """
        super().__init__(**kwargs)

        self.model_refs = model_refs
        self.owner = owner
        self.priority = priority
        self.token_metadata = token_metadata

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.model_refs is None:
                raise MissingRequiredArgumentError(argument="self.model_refs")

            if self.owner is None:
                raise MissingRequiredArgumentError(argument="self.owner")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["modelRefs"] = self.model_refs
            _spec["owner"] = self.owner

            if self.priority is not None:
                _spec["priority"] = self.priority

            if self.token_metadata is not None:
                _spec["tokenMetadata"] = self.token_metadata

    # End of generated code
