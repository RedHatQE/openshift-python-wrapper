from ocp_resources.resource import NamespacedResource


class PrometheusRule(NamespacedResource):
    """
    Prometheus Rule object.
    """

    api_group = NamespacedResource.ApiGroup.MONITORING_COREOS_COM
