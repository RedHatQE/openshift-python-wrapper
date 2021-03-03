from ocp_resources.resource import Resource


class MutatingWebhookConfiguration(Resource):
    """
    MutatingWebhookConfiguration object.
    """

    api_group = Resource.ApiGroup.ADMISSIONREGISTRATION_K8S_IO
