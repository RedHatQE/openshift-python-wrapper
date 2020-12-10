from .resource import NamespacedResource


class ServiceAccount(NamespacedResource):
    """
    Service Account object
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self, name, namespace, client=None, teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
