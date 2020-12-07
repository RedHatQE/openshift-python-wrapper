from .resource import Resource


class ImageContentSourcePolicy(Resource):
    """
    ICSP object, inherited from Resource.
    """

    api_version = Resource.ApiVersion.V1ALPHA1

    def __init__(
        self, name, client=None, teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
