from .resource import NamespacedResource


class OperatorSource(NamespacedResource):
    api_group = "operators.coreos.com"

    def __init__(
        self,
        name,
        namespace,
        registry_namespace,
        display_name,
        publisher,
        secret,
        teardown=True,
    ):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.registry_namespace = registry_namespace
        self.display_name = display_name
        self.publisher = publisher
        self.secret = secret

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "type": "appregistry",
                    "endpoint": "https://quay.io/cnr",
                    "registryNamespace": self.registry_namespace,
                    "displayName": self.display_name,
                    "publisher": self.publisher,
                    "authorizationToken": {"secretName": self.secret},
                }
            }
        )

        return res
