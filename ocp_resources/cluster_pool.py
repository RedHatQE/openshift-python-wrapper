from __future__ import annotations
from typing import Any, Dict
from ocp_resources.resource import NamespacedResource


class ClusterPool(NamespacedResource):
    """
    https://github.com/openshift/hive/blob/master/docs/clusterpools.md#supported-cloud-platforms
    """

    api_group: str = NamespacedResource.ApiGroup.HIVE_OPENSHIFT_IO

    def __init__(
        self,
        base_domain: str = "",
        image_set_ref_name: str = "",
        platform: Dict[str, Any] | None = None,
        pull_secret_ref_name: str = "",
        running_count: int | None = None,
        size: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            base_domain (str): ClusterPool base domain
            image_set_ref_name (str): ClusterPool image set name
            platform (dict): ClusterPool platform
            pull_secret_ref_name (str): ClusterPool pull secret name
            running_count (int): ClusterPool running count
            size (int): ClusterPool size
        """
        super().__init__(**kwargs)
        self.base_domain = base_domain
        self.image_set_ref_name = image_set_ref_name
        self.platform = platform
        self.pull_secret_ref_name = pull_secret_ref_name
        self.running_count = running_count
        self.size = size

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]
            if self.base_domain:
                _spec["baseDomain"] = self.base_domain

            if self.image_set_ref_name:
                _spec["imageSetRef"] = {"name": self.image_set_ref_name}

            if self.platform:
                _spec["platform"] = self.platform

            if self.pull_secret_ref_name:
                _spec["pullSecretRef"] = {"name": self.pull_secret_ref_name}

            if self.running_count:
                _spec["runningCount"] = self.running_count

            if self.size:
                _spec["size"] = self.size
