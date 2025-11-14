# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class ServingRuntime(NamespacedResource):
    """
    No field description from API
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
        r"""
        Args:
            affinity (dict[str, Any]): No field description from API

            spec_annotations (dict[str, Any]): No field description from API

            built_in_adapter (dict[str, Any]): No field description from API

            containers (list[Any]): No field description from API

            disabled (bool): No field description from API

            grpc_data_endpoint (str): No field description from API

            grpc_endpoint (str): No field description from API

            http_data_endpoint (str): No field description from API

            image_pull_secrets (list[Any]): No field description from API

            spec_labels (dict[str, Any]): No field description from API

            multi_model (bool): No field description from API

            node_selector (dict[str, Any]): No field description from API

            protocol_versions (list[Any]): No field description from API

            replicas (int): No field description from API

            storage_helper (dict[str, Any]): No field description from API

            supported_model_formats (list[Any]): No field description from API

            tolerations (list[Any]): No field description from API

            volumes (list[Any]): No field description from API

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

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.spec_annotations is not None:
                _spec["annotations"] = self.spec_annotations

            if self.built_in_adapter is not None:
                _spec["builtInAdapter"] = self.built_in_adapter

            if self.disabled is not None:
                _spec["disabled"] = self.disabled

            if self.grpc_data_endpoint is not None:
                _spec["grpcDataEndpoint"] = self.grpc_data_endpoint

            if self.grpc_endpoint is not None:
                _spec["grpcEndpoint"] = self.grpc_endpoint

            if self.http_data_endpoint is not None:
                _spec["httpDataEndpoint"] = self.http_data_endpoint

            if self.image_pull_secrets is not None:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.spec_labels is not None:
                _spec["labels"] = self.spec_labels

            if self.multi_model is not None:
                _spec["multiModel"] = self.multi_model

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

            if self.protocol_versions is not None:
                _spec["protocolVersions"] = self.protocol_versions

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.storage_helper is not None:
                _spec["storageHelper"] = self.storage_helper

            if self.supported_model_formats is not None:
                _spec["supportedModelFormats"] = self.supported_model_formats

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

            if self.volumes is not None:
                _spec["volumes"] = self.volumes

    # End of generated code
