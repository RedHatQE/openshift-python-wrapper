# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from __future__ import annotations
from typing import Any
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ServingRuntime(NamespacedResource):
    """
    No field description from API; please add description
    """

    api_group: str = NamespacedResource.ApiGroup.SERVING_KSERVE_IO

    def __init__(
        self,
        affinity: dict[str, Any] | None = None,
        spec_annotations: dict[str, Any] | None = None,
        built_in_adapter: dict[str, Any] | None = None,
        containers: list[Any] | None = None,
        disabled: bool | None = None,
        grpc_data_endpoint: str | None = None,
        grpc_endpoint: str | None = None,
        http_data_endpoint: str | None = None,
        image_pull_secrets: list[Any] | None = None,
        spec_labels: dict[str, Any] | None = None,
        multi_model: bool | None = None,
        node_selector: dict[str, Any] | None = None,
        protocol_versions: list[Any] | None = None,
        replicas: int | None = None,
        storage_helper: dict[str, Any] | None = None,
        supported_model_formats: list[Any] | None = None,
        tolerations: list[Any] | None = None,
        volumes: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            affinity (dict[str, Any]): No field description from API; please add description

            spec_annotations (dict[str, Any]): No field description from API; please add description

            built_in_adapter (dict[str, Any]): No field description from API; please add description

            containers (list[Any]): No field description from API; please add description

            disabled (bool): No field description from API; please add description

            grpc_data_endpoint (str): No field description from API; please add description

            grpc_endpoint (str): No field description from API; please add description

            http_data_endpoint (str): No field description from API; please add description

            image_pull_secrets (list[Any]): No field description from API; please add description

            spec_labels (dict[str, Any]): No field description from API; please add description

            multi_model (bool): No field description from API; please add description

            node_selector (dict[str, Any]): No field description from API; please add description

            protocol_versions (list[Any]): No field description from API; please add description

            replicas (int): No field description from API; please add description

            storage_helper (dict[str, Any]): No field description from API; please add description

            supported_model_formats (list[Any]): No field description from API; please add description

            tolerations (list[Any]): No field description from API; please add description

            volumes (list[Any]): No field description from API; please add description

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
            if self.containers is None:
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
