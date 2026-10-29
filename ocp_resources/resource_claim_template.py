# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class ResourceClaimTemplate(NamespacedResource):
    """
    ResourceClaimTemplate is used to produce ResourceClaim objects.
    """

    api_group: str = NamespacedResource.ApiGroup.RESOURCE_K8S_IO

    def __init__(
        self,
        metadata: dict[str, Any] | None = None,
        spec_spec: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            metadata (dict[str, Any]): ObjectMeta is metadata that all persisted resources must have, which
              includes all objects users must create.

            spec_spec (dict[str, Any]): ResourceClaimSpec defines what is being requested in a ResourceClaim
              and how to configure it.

        """
        super().__init__(**kwargs)

        self.metadata = metadata
        self.spec_spec = spec_spec

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.spec_spec is None:
                raise MissingRequiredArgumentError(argument="self.spec_spec")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["spec"] = self.spec_spec

            if self.metadata is not None:
                _spec["metadata"] = self.metadata

    # End of generated code
