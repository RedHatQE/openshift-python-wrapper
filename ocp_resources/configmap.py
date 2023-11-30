from ocp_resources.resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
    https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/config-map-v1/
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        data=None,
        **kwargs,
    ):
        """
        Args:
            data (dict, optional): key-value configuration pairs.
        """
        super().__init__(**kwargs)
        self.data = data

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file and self.data:
            self.res.setdefault("data", {}).update(self.data)
