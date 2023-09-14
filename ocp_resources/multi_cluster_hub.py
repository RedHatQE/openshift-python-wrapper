from ocp_resources.resource import NamespacedResource


class MultiClusterHub(NamespacedResource):
    """
    https://github.com/stolostron/rhacm-docs/blob/8ccc58609821f5d3b2845bb6f5c0cbd597eb3b1c/apis/multicluster_hub.json.adoc#multicluster-hub-api
    """

    api_group = NamespacedResource.ApiGroup.OPERATOR_OPEN_CLUSTER_MANAGEMENT_IO
