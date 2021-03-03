from ocp_resources.resource import NamespacedResource


class ServiceAccount(NamespacedResource):
    """
    Service Account object
    """

    api_version = NamespacedResource.ApiVersion.V1
