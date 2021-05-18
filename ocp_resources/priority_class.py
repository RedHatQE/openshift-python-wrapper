from ocp_resources.resource import Resource


class PriorityClass(Resource):
    """
    Priority Class object.
    """

    api_group = Resource.ApiGroup.SCHEDULING_K8S_IO
