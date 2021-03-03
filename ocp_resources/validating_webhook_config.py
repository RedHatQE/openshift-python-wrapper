from ocp_resources.resource import Resource


class ValidatingWebhookConfiguration(Resource):
    """
    ValidatingWebhookConfiguration object.
    """

    api_group = Resource.ApiGroup.ADMISSIONREGISTRATION_K8S_IO
