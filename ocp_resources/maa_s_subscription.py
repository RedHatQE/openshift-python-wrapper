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
        billing_metadata: dict[str, Any] | None = None,
        model_refs: list[Any] | None = None,
        owner: dict[str, Any] | None = None,
        priority: int | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            billing_metadata (dict[str, Any]): BillingMetadata contains billing information

            model_refs (list[Any]): ModelRefs defines which models are included with per-model token rate
              limits

            owner (dict[str, Any]): Owner defines who owns this subscription

            priority (int): Priority determines subscription priority when user has multiple
              subscriptions Higher numbers have higher priority. Defaults to 0.

        """
        super().__init__(**kwargs)

        self.billing_metadata = billing_metadata
        self.model_refs = model_refs
        self.owner = owner
        self.priority = priority

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

            if self.billing_metadata is not None:
                _spec["billingMetadata"] = self.billing_metadata

            if self.priority is not None:
                _spec["priority"] = self.priority

    # End of generated code
