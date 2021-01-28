from resources.resource import Resource
from resources.utils import TimeoutSampler


class NodeNetworkConfigurationEnactment(Resource):
    api_group = Resource.ApiGroup.NMSTATE_IO

    class ConditionType:
        FAILING = "Failing"
        AVAILABLE = "Available"
        PROGRESSING = "Progressing"
        MATCHING = "Matching"

    def wait_for_conditions(self):
        samples = TimeoutSampler(
            timeout=30, sleep=1, func=lambda: self.instance.status.conditions
        )
        for sample in samples:
            if sample:
                return
