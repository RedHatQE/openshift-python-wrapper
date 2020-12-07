from .resource import NamespacedResource


class PackageManifest(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.PACKAGES_OPERATORS_COREOS_COM

    def __init__(
        self, name, namespace, client=None, teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
