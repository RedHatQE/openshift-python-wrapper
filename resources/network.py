from resources.resource import Resource


class Network(Resource):
    api_group = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self, name, client=None, teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
