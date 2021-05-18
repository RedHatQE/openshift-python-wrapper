from ocp_resources.resource import Resource


class PrometheusRule(Resource):
    """
    Prometheus Rule object.
    """

    api_group = Resource.ApiGroup.MONITORING_COREOS_COM
