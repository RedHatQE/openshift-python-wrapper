from resources.resource import Resource


class OAuth(Resource):
    """
    OAuth object.
    """

    api_version = Resource.ApiVersion.V1

    def __init__(
        self,
        name,
        client=None,
        teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
