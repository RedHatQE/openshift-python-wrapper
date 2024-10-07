from typing import Optional, Dict, Any

from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class InferenceService(NamespacedResource):
    """
    https://github.com/kserve/kserve/blob/master/pkg/apis/serving/v1beta1/inference_service.go
    """

    api_group: str = NamespacedResource.ApiGroup.SERVING_KSERVE_IO

    def __init__(
        self,
        predictor: Optional[Dict[str, Any]] = None,
        explainer: Optional[Dict[str, Any]] = None,
        transformer: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        InferenceService object

        Args:
            predictor (Optional[Dict[str, Any]], mandatory if yaml_file is not provided): Defines the model serving spec.
            explainer (Optional[Dict[str, Any]]): Defines the model explanation service spec.
            transformer (Optional[Dict[str, Any]]): Defines the pre/post processing before and after the predictor call.
        """
        super().__init__(
            **kwargs,
        )
        self.predictor = predictor
        self.explainer = explainer
        self.transformer = transformer

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.predictor:
                raise MissingRequiredArgumentError(argument="predictor")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["predictor"] = self.predictor

            if self.explainer:
                _spec["explainer"] = self.explainer

            if self.transformer:
                _spec["transformer"] = self.transformer
