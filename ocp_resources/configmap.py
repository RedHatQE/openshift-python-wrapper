from __future__ import annotations
from typing import Any, Dict

from ocp_resources.resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
    https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/config-map-v1/
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        data: Dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        """
        Args:
            data (dict, optional): key-value configuration pairs.
        """
        super().__init__(**kwargs)

        self.data = data

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file and self.data:
            self.res["data"] = self.data
