from typing import Any, Optional, Dict
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class GuardrailsOrchestrator(NamespacedResource):
    """
    GuardrailsOrchestrator is the Schema for the guardrailsorchestrators API.
    """

    api_group: str = NamespacedResource.ApiGroup.TRUSTYAI_OPENDATAHUB_IO

    def __init__(
        self,
        orchestrator_config: Optional[str] = "",
        otel_exporter: Optional[Dict[str, Any]] = None,
        replicas: Optional[int] = None,
        vllm_gateway_config: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            orchestrator_config (str): Name of configmap containing generator,detector,and chunker arguments

            otel_exporter (Dict[str, Any]): List of orchestrator enviroment variables for configuring the OTLP
              exporter

            replicas (int): Number of replicas

            vllm_gateway_config (str):  Name of the configmap containg vLLM gateway arguments

        """
        super().__init__(**kwargs)

        self.orchestrator_config = orchestrator_config
        self.otel_exporter = otel_exporter
        self.replicas = replicas
        self.vllm_gateway_config = vllm_gateway_config

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.orchestrator_config is None:
                raise MissingRequiredArgumentError(argument="self.orchestrator_config")

            if self.replicas is None:
                raise MissingRequiredArgumentError(argument="self.replicas")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["orchestratorConfig"] = self.orchestrator_config
            _spec["replicas"] = self.replicas

            if self.otel_exporter is not None:
                _spec["otelExporter"] = self.otel_exporter

            if self.vllm_gateway_config is not None:
                _spec["vllmGatewayConfig"] = self.vllm_gateway_config

    # End of generated code
