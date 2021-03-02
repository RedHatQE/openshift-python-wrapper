from ocp_resources.resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
    Configmap object
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(self, name, namespace, data=None, teardown=True, client=None):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.data = data

    def to_dict(self):
        res = super().to_dict()
        res.setdefault("data", {}).update(self.data)
        return res
