from ocp_resources.resource import NamespacedResource
from typing import Optional, Any, Dict


class TrustyAIService(NamespacedResource):
    """
    https://github.com/trustyai-explainability/trustyai-service-operator/blob/main/api/v1alpha1/trustyaiservice_types.go
    """

    api_group: str = NamespacedResource.ApiGroup.TRUSTYAI_OPENDATAHUB_IO

    def __init__(
        self,
        storage: Dict[str, Any],
        data: Dict[str, Any],
        metrics: Dict[str, Any],
        replicas: Optional[int] = 1,
        image: Optional[str] = None,
        tag: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        TrustyAIService object

        Args:
            storage (Dic[str, Any]): TrustyAIService storage config (format, folder and size).
            data (Dict[str, Any]): TrustyAIService data config (filename and format).
            metrics (Dict[str, Any]): TrustyAIService metrics config.
            replicas (Optional[int], default: 1): Number of replicas for the TrustyAIService.
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

    def to_dict(self):
        super().to_dict()

        if not self.yaml_file:
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
