from __future__ import annotations
from typing import Any, Dict

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class SealedSecret(NamespacedResource):
    """
    https://github.com/bitnami-labs/sealed-secrets/blob/main/pkg/apis/sealedsecrets/v1alpha1/types.go

    Requires the Sealed Secrets Operator to be installed.
    """

    api_group = NamespacedResource.ApiGroup.BITNAMI_COM

    def __init__(
        self,
        encrypted_data: Dict[str, Any] | None = None,
        template: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            encrypted_data (dict): secret encrypted data
            template (dict): defines the structure of the Secret that will be created from this sealed secret
            data (dict): secret encrypted data
        """
        super().__init__(**kwargs)
        self.encrypted_data = encrypted_data
        self.template = template
        self.data = data

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.encrypted_data:
                raise MissingRequiredArgumentError(argument="encrypted_data")

            self.res["spec"] = {}
            _spec = self.res["spec"]
            _spec["encryptedData"] = self.encrypted_data

            if self.template:
                _spec["template"] = self.template

            if self.data:
                _spec["data"] = self.data

    @property
    def keys_to_hash(self):
        return ["spec..data", "spec..encryptedData"]
