from .resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
    Configmap object
    """

    api_version = "v1"

    def __init__(self, name, namespace, cert_name=None, data=None, teardown=True):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.cert_name = cert_name
        self.data = data

    def to_dict(self):
        res = super()._base_body()
        if self.cert_name is None:
            res.update({"data": {"tlsregistry.crt": self.data}})
        else:
            res.update({"data": {self.cert_name: self.data}})
        return res
