from resources.resource import NamespacedResource


class KubevirtNodeLabellerBundle(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.SSP_KUBEVIRT_IO

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
