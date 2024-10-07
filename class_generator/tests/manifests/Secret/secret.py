# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource


class Secret(NamespacedResource):
    """
    Secret holds secret data of a certain type. The total bytes of the values in the Data field must be less than MaxSecretSize bytes.
    """

    api_version: str = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        immutable: Optional[bool] = None,
        string_data: Optional[Dict[str, Any]] = None,
        type: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            data (Dict[str, Any]): Data contains the secret data. Each key must consist of alphanumeric
              characters, '-', '_' or '.'. The serialized form of the secret
              data is a base64 encoded string, representing the arbitrary
              (possibly non-string) data value here. Described in
              https://tools.ietf.org/html/rfc4648#section-4

            immutable (bool): Immutable, if set to true, ensures that data stored in the Secret
              cannot be updated (only object metadata can be modified). If not
              set to true, the field can be modified at any time. Defaulted to
              nil.

            string_data (Dict[str, Any]): stringData allows specifying non-binary secret data in string form. It
              is provided as a write-only input field for convenience. All keys
              and values are merged into the data field on write, overwriting
              any existing values. The stringData field is never output when
              reading from the API.

            type (str): Used to facilitate programmatic handling of secret data. More info:
              https://kubernetes.io/docs/concepts/configuration/secret/#secret-
              types

        """
        super().__init__(**kwargs)

        self.data = data
        self.immutable = immutable
        self.string_data = string_data
        self.type = type

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.data:
                self.res["data"] = self.data

            if self.immutable is not None:
                self.res["immutable"] = self.immutable

            if self.string_data:
                self.res["stringData"] = self.string_data

            if self.type:
                self.res["type"] = self.type

    # End of generated code
