# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource


class Secret(NamespacedResource):
    """
    Secret holds secret data of a certain type. The total bytes of the values in
    the Data field must be less than MaxSecretSize bytes.

    API Link: https://example.explain
    """

    api_version: str = "v1"

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
            data(Dict[Any, Any]): <please add description>
            immutable(bool): <please add description>
            string_data(Dict[Any, Any]): <please add description>
            type(str): <please add description>
        """
        super().__init__(**kwargs)

        self.data = data
        self.immutable = immutable
        self.string_data = string_data
        self.type = type

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            if self.data:
                self.res["data"] = self.data

            if self.immutable is not None:
                self.res["immutable"] = self.immutable

            if self.string_data:
                self.res["stringData"] = self.string_data

            if self.type:
                self.res["type"] = self.type
