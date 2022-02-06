from ocp_resources.resource import Resource


class NodeNetworkConfigurationEnactment(Resource):
    api_group = Resource.ApiGroup.NMSTATE_IO

    class Conditions:
        class Type:
            FAILING = "Failing"
            AVAILABLE = "Available"
            PROGRESSING = "Progressing"
            PENDING = "Pending"
            ABORTED = "Aborted"

        class Reason:
            CONFIGURATION_PROGRESSING = "ConfigurationProgressing"
            SUCCESSFULLY_CONFIGURED = "SuccessfullyConfigured"
            FAILED_TO_CONFIGURE = "FailedToConfigure"
            CONFIGURATION_ABORTED = "ConfigurationAborted"
            MAX_UNAVAILABLE_LIMIT_REACHED = "MaxUnavailableLimitReached"
