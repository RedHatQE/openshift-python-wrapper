from resources.resource import Resource


class NetworkAddonsConfig(Resource):
    """
    NetworkAddonsConfig (a Custom Resource) object, inherited from Resource.
    """

    api_group = Resource.ApiGroup.NETWORKADDONSOPERATOR_NETWORK_KUBEVIRT_IO

    def __init__(
        self,
        name,
        client=None,
        teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
