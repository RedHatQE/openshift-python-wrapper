from ocp_resources.resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
    Configmap object
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        name=None,
        namespace=None,
        data=None,
        teardown=True,
        client=None,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.data = data

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res.setdefault("data", {}).update(self.data)
        return res
