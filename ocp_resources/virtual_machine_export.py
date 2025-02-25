# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from __future__ import annotations
from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource

from typing import Any


class VirtualMachineExport(NamespacedResource):
    """
    VirtualMachineExport defines the operation of exporting a VM source
    """

    api_group: str = NamespacedResource.ApiGroup.EXPORT_KUBEVIRT_IO

    def __init__(
        self,
        source: dict[str, Any] | None = None,
        token_secret_ref: str | None = None,
        ttl_duration: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            source (dict[str, Any]): TypedLocalObjectReference contains enough information to let you
              locate the typed referenced object inside the same namespace.

            token_secret_ref (str): TokenSecretRef is the name of the custom-defined secret that contains
              the token used by the export server pod

            ttl_duration (str): ttlDuration limits the lifetime of an export If this field is set,
              after this duration has passed from counting from
              CreationTimestamp, the export is eligible to be automatically
              deleted. If this field is omitted, a reasonable default is
              applied.

        """
        super().__init__(**kwargs)

        self.source = source
        self.token_secret_ref = token_secret_ref
        self.ttl_duration = ttl_duration

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.source is None:
                raise MissingRequiredArgumentError(argument="self.source")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["source"] = self.source

            if self.token_secret_ref:
                _spec["tokenSecretRef"] = self.token_secret_ref

            if self.ttl_duration:
                _spec["ttlDuration"] = self.ttl_duration

    # End of generated code
