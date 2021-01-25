from resources.resource import Resource


class CustomResourceDefinition(Resource):
    api_group = Resource.ApiGroup.APIEXTENSIONS_K8S_IO

    def __init__(
        self,
        name,
        client=None,
        teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
