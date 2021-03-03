from ocp_resources.resource import Resource


class APIService(Resource):
    """
    APIService object.
    """

    api_group = Resource.ApiGroup.APIREGISTRATION_K8S_IO
