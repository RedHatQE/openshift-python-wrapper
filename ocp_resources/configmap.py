from ocp_resources.resource import NamespacedResource


class ConfigMap(NamespacedResource):
    """
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
            data (dict): key-value configuration pairs.
        """
        super().__init__(**kwargs)
        self.data = data

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file and self.data:
            self.res.setdefault("data", {}).update(self.data)
