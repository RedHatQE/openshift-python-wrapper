from .resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
    Configmap object
    """

    api_version = "v1"

    def __init__(self, name, namespace, data=None, teardown=True):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.data = data

    def to_dict(self):
        res = super()._base_body()
        res.setdefault("data", {}).update(self.data)
        return res
