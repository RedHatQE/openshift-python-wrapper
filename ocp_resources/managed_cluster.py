from ocp_resources.resource import Resource


class ManagedCluster(Resource):
    """
    https://github.com/stolostron/api/blob/main/cluster/v1/0000_00_clusters.open-cluster-management.io_managedclusters.crd.yaml
    Provides a representation of the managed cluster on the hub.
    """

    api_group = Resource.ApiGroup.CLUSTER_OPEN_CLUSTER_MANAGEMENT_IO
