from .resource import NamespacedResource


class CDI(NamespacedResource):
    """
    CDI object.
    """

    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    class Status(NamespacedResource.Status):
        DEPLOYING = "Deploying"
        DEPLOYED = "Deployed"

    def __init__(
        self, name, namespace, teardown=True, client=None,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
