from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError
from typing import Optional, Any, Dict


class TrustyAIService(NamespacedResource):
    """
    https://github.com/trustyai-explainability/trustyai-service-operator/blob/main/api/v1alpha1/trustyaiservice_types.go
    """

    api_group: str = NamespacedResource.ApiGroup.TRUSTYAI_OPENDATAHUB_IO

    def __init__(
        self,
        storage: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        replicas: Optional[int] = None,
        image: Optional[str] = None,
        tag: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        TrustyAIService object

        Args:
            storage (Optional[Dic[str, Any]], mandatory if not passing yaml_file): TrustyAIService storage config (format, folder and size).
            data (Optional[Dict[str, Any]], mandatory if not passing yaml_file): TrustyAIService data config (filename and format).
            metrics (Optional[Dict[str, Any]], mandatory if not passing yaml_file): TrustyAIService metrics config.
            replicas (Optional[int]): Number of replicas for the TrustyAIService.
            image (Optional[str]): Pull url of the TrustyAIService.
            tag (Optional[str]): Tag of the image.
        """
        super().__init__(**kwargs)
        self.storage = storage
        self.data = data
        self.metrics = metrics
        self.replicas = replicas
        self.image = image
        self.tag = tag

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            if not (self.storage or self.data or self.metrics):
                raise MissingRequiredArgumentError(argument="'storage' or 'data' or 'metrics'")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["storage"] = self.storage
            _spec["data"] = self.data
            _spec["metrics"] = self.metrics

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.image:
                _spec["image"] = self.image

            if self.tag:
                _spec["tag"] = self.tag
