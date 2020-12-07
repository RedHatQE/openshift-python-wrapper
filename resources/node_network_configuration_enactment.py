from resources.resource import Resource


class NodeNetworkConfigurationEnactment(Resource):
    api_group = Resource.ApiGroup.NMSTATE_IO

    class ConditionType:
        FAILING = "Failing"
        AVAILABLE = "Available"
        PROGRESSING = "Progressing"
        MATCHING = "Matching"

    def __init__(
        self, name, client=None, teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
