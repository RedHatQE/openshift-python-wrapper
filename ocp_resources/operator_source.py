from ocp_resources.resource import NamespacedResource


class OperatorSource(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        name,
        namespace,
        registry_namespace,
        display_name,
        publisher,
        secret,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.registry_namespace = registry_namespace
        self.display_name = display_name
        self.publisher = publisher
        self.secret = secret

    def to_dict(self):
        res = super().to_dict()
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
