from __future__ import annotations
from typing import List, Optional, Any, Dict

from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ServingRuntime(NamespacedResource):
    """
    https://github.com/kserve/kserve/blob/master/pkg/apis/serving/v1alpha1/servingruntime_types.go
    """

    api_group: str = NamespacedResource.ApiGroup.SERVING_KSERVE_IO

    def __init__(
        self,
        supported_model_formats: Optional[List[Dict[str, Any]]] = None,
        protocol_versions: Optional[List[str]] = None,
        multi_model: Optional[bool] = None,
        containers: Optional[List[Dict[str, Any]]] = None,
        grpc_endpoint: Optional[int] = None,
        grpc_data_endpoint: Optional[int] = None,
        built_in_adapter: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        ServingRuntime object

        Args:
            supported_model_formats Optional[List[Dict[str, Any]]]: Model formats supported by the serving runtime.
            protocol_versions Optional[List[str]]: List of protocols versions used by the serving runtime.
            multi_model (Optional[bool]): Specifies if the model server can serve multiple models.
            containers Optional[List[Dict[str, Any]]]: Containers of the serving runtime.
            grpc_endpoint Optional[int]: Port of the gRPC endpoint.
            grpc_data_endpoint Optional[int]: Port of the gRPC data endpoint.
            built_in_adapter Optional[Dict[str, Any]]: Configuration for the built-in adapter.
        """
        super().__init__(**kwargs)
        self.supported_model_formats = supported_model_formats
        self.protocol_versions = protocol_versions
        self.multi_model = multi_model
        self.containers = containers
        self.grpc_endpoint = grpc_endpoint
        self.grpc_data_endpoint = grpc_data_endpoint
        self.built_in_adapter = built_in_adapter

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.containers:
                raise MissingRequiredArgumentError(argument="'containers'")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.supported_model_formats:
                _spec["supportedModelFormats"] = self.supported_model_formats

            if self.protocol_versions:
                _spec["protocolVersions"] = self.protocol_versions

            if self.multi_model is not None:
                _spec["multiModel"] = self.multi_model

            if self.grpc_endpoint:
                _spec["grpcEndpoint"] = f"port:{self.grpc_endpoint}"

            if self.grpc_data_endpoint:
                _spec["grpcDataEndpoint"] = f"port:{self.grpc_data_endpoint}"

            if self.containers:
                _spec["containers"] = self.containers

            if self.built_in_adapter:
                _spec["builtInAdapter"] = self.built_in_adapter
