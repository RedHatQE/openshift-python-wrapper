from ocp_resources.resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
    Configmap in kubernetes API official docs:
        https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#configmap-v1-core
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        data=None,
        **kwargs,
    ):
        """
        Args:
            data (Object): Data contains the configuration data.
                Each key must consist of alphanumeric characters, '-', '_' or '.'.
                Values with non-UTF-8 byte sequences must use the BinaryData field. The keys stored in
                Data must not overlap with the keys in the BinaryData field, this is enforced during validation process.
        """
        super().__init__(**kwargs)
        self.data = data

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file and self.data:
            self.res.setdefault("data", {}).update(self.data)
