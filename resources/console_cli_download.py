from resources.resource import Resource


class ConsoleCLIDownload(Resource):
    """
    ConsoleCLIDownload object, inherited from Resource.
    """

    api_group = Resource.ApiGroup.CONSOLE_OPENSHIFT_IO

    def __init__(
        self,
        name,
        client=None,
        teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
