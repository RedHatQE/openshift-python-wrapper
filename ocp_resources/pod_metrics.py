from ocp_resources.resource import NamespacedResource


class PodMetrics(NamespacedResource):
    """
    PodMetrics object. API reference:
    This resource is managed by: https://github.com/kubernetes-sigs/metrics-server and is a built-in resource
    """

    api_group = NamespacedResource.ApiGroup.METRICS_K8S_IO
