from ocp_resources.resource import NamespacedResource


class ServiceMonitor(NamespacedResource):
    """
    Service Monitor object.
    """

    api_group = NamespacedResource.ApiGroup.MONITORING_COREOS_COM
