from ocp_resources.resource import Resource


class ServiceMonitor(Resource):
    """
    Service Monitor object.
    """

    api_group = Resource.ApiGroup.MONITORING_COREOS_COM
