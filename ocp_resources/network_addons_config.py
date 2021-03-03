from ocp_resources.resource import Resource


class NetworkAddonsConfig(Resource):
    """
    NetworkAddonsConfig (a Custom Resource) object, inherited from Resource.
    """

    api_group = Resource.ApiGroup.NETWORKADDONSOPERATOR_NETWORK_KUBEVIRT_IO
