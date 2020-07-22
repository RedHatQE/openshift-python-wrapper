from .resource import Resource


class MutatingWebhookConfiguration(Resource):
    """
    MutatingWebhookConfiguration object.
    """

    api_group = "admissionregistration.k8s.io"
