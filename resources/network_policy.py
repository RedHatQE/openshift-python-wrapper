from .resource import NamespacedResource


class NetworkPolicy(NamespacedResource):
    """
    NetworkPolicy object.
    """

    api_group = NamespacedResource.ApiGroup.NETWORKING_K8S_IO

    def __init__(
        self,
        name,
        namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
