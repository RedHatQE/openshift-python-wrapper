from .resource import Resource


class ValidatingWebhookConfiguration(Resource):
    """
    ValidatingWebhookConfiguration object.
    """

    api_group = "admissionregistration.k8s.io"
