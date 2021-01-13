from resources.resource import NamespacedResource


class ImageStreamTag(NamespacedResource):
    """
    ImageStreamTag object.
    """

    api_group = NamespacedResource.ApiGroup.IMAGE_OPENSHIFT_IO

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
