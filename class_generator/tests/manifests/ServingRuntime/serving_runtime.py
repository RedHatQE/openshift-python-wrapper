# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ServingRuntime(NamespacedResource):
    """
    No field description from API; please add description
    """

    api_group: str = NamespacedResource.ApiGroup.SERVING_KSERVE_IO

    def __init__(
        self,
        affinity: Optional[Dict[str, Any]] = None,
        spec_annotations: Optional[Dict[str, Any]] = None,
        built_in_adapter: Optional[Dict[str, Any]] = None,
        containers: Optional[List[Any]] = None,
        disabled: Optional[bool] = None,
        grpc_data_endpoint: Optional[str] = "",
        grpc_endpoint: Optional[str] = "",
        http_data_endpoint: Optional[str] = "",
        image_pull_secrets: Optional[List[Any]] = None,
        spec_labels: Optional[Dict[str, Any]] = None,
        multi_model: Optional[bool] = None,
        node_selector: Optional[Dict[str, Any]] = None,
        protocol_versions: Optional[List[Any]] = None,
        replicas: Optional[int] = None,
        storage_helper: Optional[Dict[str, Any]] = None,
        supported_model_formats: Optional[List[Any]] = None,
        tolerations: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            affinity (Dict[str, Any]): No field description from API; please add description

            spec_annotations (Dict[str, Any]): No field description from API; please add description

            built_in_adapter (Dict[str, Any]): No field description from API; please add description

            containers (List[Any]): No field description from API; please add description

            disabled (bool): No field description from API; please add description

            grpc_data_endpoint (str): No field description from API; please add description

            grpc_endpoint (str): No field description from API; please add description

            http_data_endpoint (str): No field description from API; please add description

            image_pull_secrets (List[Any]): No field description from API; please add description

            spec_labels (Dict[str, Any]): No field description from API; please add description

            multi_model (bool): No field description from API; please add description

            node_selector (Dict[str, Any]): No field description from API; please add description

            protocol_versions (List[Any]): No field description from API; please add description

            replicas (int): No field description from API; please add description

            storage_helper (Dict[str, Any]): No field description from API; please add description

            supported_model_formats (List[Any]): No field description from API; please add description

            tolerations (List[Any]): No field description from API; please add description

            volumes (List[Any]): No field description from API; please add description

        """
        super().__init__(**kwargs)

        self.affinity = affinity
        self.spec_annotations = spec_annotations
        self.built_in_adapter = built_in_adapter
        self.containers = containers
        self.disabled = disabled
        self.grpc_data_endpoint = grpc_data_endpoint
        self.grpc_endpoint = grpc_endpoint
        self.http_data_endpoint = http_data_endpoint
        self.image_pull_secrets = image_pull_secrets
        self.spec_labels = spec_labels
        self.multi_model = multi_model
        self.node_selector = node_selector
        self.protocol_versions = protocol_versions
        self.replicas = replicas
        self.storage_helper = storage_helper
        self.supported_model_formats = supported_model_formats
        self.tolerations = tolerations
        self.volumes = volumes

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.containers:
                raise MissingRequiredArgumentError(argument="self.containers")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["containers"] = self.containers

            if self.affinity:
                _spec["affinity"] = self.affinity

            if self.spec_annotations:
                _spec["annotations"] = self.spec_annotations

            if self.built_in_adapter:
                _spec["builtInAdapter"] = self.built_in_adapter

            if self.disabled is not None:
                _spec["disabled"] = self.disabled

            if self.grpc_data_endpoint:
                _spec["grpcDataEndpoint"] = self.grpc_data_endpoint

            if self.grpc_endpoint:
                _spec["grpcEndpoint"] = self.grpc_endpoint

            if self.http_data_endpoint:
                _spec["httpDataEndpoint"] = self.http_data_endpoint

            if self.image_pull_secrets:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.spec_labels:
                _spec["labels"] = self.spec_labels

            if self.multi_model is not None:
                _spec["multiModel"] = self.multi_model

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.protocol_versions:
                _spec["protocolVersions"] = self.protocol_versions

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.storage_helper:
                _spec["storageHelper"] = self.storage_helper

            if self.supported_model_formats:
                _spec["supportedModelFormats"] = self.supported_model_formats

            if self.tolerations:
                _spec["tolerations"] = self.tolerations

            if self.volumes:
                _spec["volumes"] = self.volumes

    # End of generated code
