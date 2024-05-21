from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class OperatorSource(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        name=None,
        namespace=None,
        registry_namespace=None,
        display_name=None,
        publisher=None,
        secret=None,
        client=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.registry_namespace = registry_namespace
        self.display_name = display_name
        self.publisher = publisher
        self.secret = secret

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            self.res.update({
                "spec": {
                    "type": "appregistry",
                    "endpoint": "https://quay.io/cnr",
                    "registryNamespace": self.registry_namespace,
                    "displayName": self.display_name,
                    "publisher": self.publisher,
                    "authorizationToken": {"secretName": self.secret},
                }
            })
