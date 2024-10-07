# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
    ConfigMap holds configuration data for pods to consume.
    """

    api_version: str = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        binary_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        immutable: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            binary_data (Dict[str, Any]): BinaryData contains the binary data. Each key must consist of
              alphanumeric characters, '-', '_' or '.'. BinaryData can contain
              byte sequences that are not in the UTF-8 range. The keys stored in
              BinaryData must not overlap with the ones in the Data field, this
              is enforced during validation process. Using this field will
              require 1.10+ apiserver and kubelet.

            data (Dict[str, Any]): Data contains the configuration data. Each key must consist of
              alphanumeric characters, '-', '_' or '.'. Values with non-UTF-8
              byte sequences must use the BinaryData field. The keys stored in
              Data must not overlap with the keys in the BinaryData field, this
              is enforced during validation process.

            immutable (bool): Immutable, if set to true, ensures that data stored in the ConfigMap
              cannot be updated (only object metadata can be modified). If not
              set to true, the field can be modified at any time. Defaulted to
              nil.

        """
        super().__init__(**kwargs)

        self.binary_data = binary_data
        self.data = data
        self.immutable = immutable

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.binary_data:
                self.res["binaryData"] = self.binary_data

            if self.data:
                self.res["data"] = self.data

            if self.immutable is not None:
                self.res["immutable"] = self.immutable

    # End of generated code

    @property
    def keys_to_hash(self):
        return ["data", "binaryData"]
