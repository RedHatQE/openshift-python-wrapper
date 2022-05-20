from ocp_resources.resource import Resource


class ConsolePlugin(Resource):
    """
    ConsolePlugin object.
    """

    api_group = Resource.ApiGroup.CONSOLE_OPENSHIFT_IO
    api_version = Resource.ApiVersion.V1ALPHA1
