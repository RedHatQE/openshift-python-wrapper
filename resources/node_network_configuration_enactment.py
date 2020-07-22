from resources.resource import Resource


class NodeNetworkConfigurationEnactment(Resource):

    api_group = "nmstate.io"

    class ConditionType:
        FAILING = "Failing"
        AVAILABLE = "Available"
        PROGRESSING = "Progressing"
        MATCHING = "Matching"
