from typing import Any, Dict
from ocp_resources.resource import NamespacedResource


class ClusterDeployment(NamespacedResource):
    """
    https://github.com/openshift/hive/blob/master/docs/using-hive.md#clusterdeployment
    """

    api_group: str = NamespacedResource.ApiGroup.HIVE_OPENSHIFT_IO

    def __init__(
        self,
        base_domain: str = "",
        cluster_name: str = "",
        platform: Dict[str, Any] | None = None,
        provisioning: Dict[str, Any] | None = None,
        pull_secret_ref_name: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            base_domain (str): ClusterDeployment base domain
            cluster_name (str): ClusterDeployment cluster name
            platform (dict): ClusterDeployment platform
            provisioning (dict): ClusterDeployment provisioning
            pull_secret_ref_name (str): ClusterDeployment pull secret name
        """
        super().__init__(**kwargs)
        self.base_domain = base_domain
        self.cluster_name = cluster_name
        self.platform = platform
        self.provisioning = provisioning
        self.pull_secret_ref_name = pull_secret_ref_name

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.base_domain:
                _spec["baseDomain"] = self.base_domain

            if self.cluster_name:
                _spec["clusterName"] = self.cluster_name

            if self.platform:
                _spec["platform"] = self.platform

            if self.provisioning:
                _spec["provisioning"] = self.provisioning

            if self.pull_secret_ref_name:
                _spec["pullSecretRef"] = {"name": self.pull_secret_ref_name}
