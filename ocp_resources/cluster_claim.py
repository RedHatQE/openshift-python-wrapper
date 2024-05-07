from typing import Any

from ocp_resources.resource import NamespacedResource


class ClusterClaim(NamespacedResource):
    """
    https://github.com/openshift/hive/blob/master/docs/clusterpools.md#sample-cluster-claim
    """

    api_group: str = NamespacedResource.ApiGroup.HIVE_OPENSHIFT_IO

    def __init__(
        self,
        cluster_pool_name: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            cluster_pool_name (str): ClusterPool name to claim the cluster from
        """
        super().__init__(**kwargs)
        self.cluster_pool_name = cluster_pool_name

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file and self.cluster_pool_name:
            self.res.setdefault("spec", {})["clusterPoolName"] = self.cluster_pool_name
