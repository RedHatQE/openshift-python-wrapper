from ocp_resources.resource import NamespacedResource


class Prometheus(NamespacedResource):
    """
    Prometheus object.
    """

    api_group = NamespacedResource.ApiGroup.MONITORING_COREOS_COM
