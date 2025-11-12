# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class GuardrailsOrchestrator(NamespacedResource):
    """
    GuardrailsOrchestrator is the Schema for the guardrailsorchestrators API.
    """

    api_group: str = NamespacedResource.ApiGroup.TRUSTYAI_OPENDATAHUB_IO

    def __init__(
        self,
        auto_config: dict[str, Any] | None = None,
        enable_built_in_detectors: bool | None = None,
        enable_guardrails_gateway: bool | None = None,
        guardrails_gateway_config: str | None = None,
        log_level: str | None = None,
        orchestrator_config: str | None = None,
        otel_exporter: dict[str, Any] | None = None,
        replicas: int | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            auto_config (dict[str, Any]): Settings governing the automatic configuration of the orchestrator.
              Replaces `OrchestratorConfig`.

            enable_built_in_detectors (bool): Boolean flag to enable/disable built-in detectors

            enable_guardrails_gateway (bool): Boolean flag to enable/disable the guardrails sidecar gateway

            guardrails_gateway_config (str):  Name of the configmap containing guadrails sidecar gateway arguments

            log_level (str): Set log level in the orchestrator deployment

            orchestrator_config (str): Name of configmap containing generator,detector,and chunker arguments

            otel_exporter (dict[str, Any]): List of orchestrator enviroment variables for configuring the OTLP
              exporter

            replicas (int): INSERT ADDITIONAL SPEC FIELDS - desired state of cluster Important:
              Run "make" to regenerate code after modifying this file Number of
              replicas

        """
        super().__init__(**kwargs)

        self.auto_config = auto_config
        self.enable_built_in_detectors = enable_built_in_detectors
        self.enable_guardrails_gateway = enable_guardrails_gateway
        self.guardrails_gateway_config = guardrails_gateway_config
        self.log_level = log_level
        self.orchestrator_config = orchestrator_config
        self.otel_exporter = otel_exporter
        self.replicas = replicas

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.replicas is None:
                raise MissingRequiredArgumentError(argument="self.replicas")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["replicas"] = self.replicas

            if self.auto_config is not None:
                _spec["autoConfig"] = self.auto_config

            if self.enable_built_in_detectors is not None:
                _spec["enableBuiltInDetectors"] = self.enable_built_in_detectors

            if self.enable_guardrails_gateway is not None:
                _spec["enableGuardrailsGateway"] = self.enable_guardrails_gateway

            if self.guardrails_gateway_config is not None:
                _spec["guardrailsGatewayConfig"] = self.guardrails_gateway_config

            if self.log_level is not None:
                _spec["logLevel"] = self.log_level

            if self.orchestrator_config is not None:
                _spec["orchestratorConfig"] = self.orchestrator_config

            if self.otel_exporter is not None:
                _spec["otelExporter"] = self.otel_exporter

    # End of generated code
