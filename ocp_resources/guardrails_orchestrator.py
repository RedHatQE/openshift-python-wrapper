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
        custom_detectors_config: str | None = None,
        disable_orchestrator: bool | None = None,
        enable_built_in_detectors: bool | None = None,
        enable_guardrails_gateway: bool | None = None,
        env: list[Any] | None = None,
        guardrails_gateway_config: str | None = None,
        log_level: str | None = None,
        orchestrator_config: str | None = None,
        otel_exporter: dict[str, Any] | None = None,
        replicas: int | None = None,
        tls_secrets: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            auto_config (dict[str, Any]): Settings governing the automatic configuration of the orchestrator.
              Replaces `OrchestratorConfig`.

            custom_detectors_config (str): Name of configmap containing user-defined Python detectors. This is
              only used if EnableBuiltInDetectors is true

            disable_orchestrator (bool):  Boolean flag to disable the orchestrator container, if running the
              built-in detectors in standalone mode

            enable_built_in_detectors (bool): Boolean flag to enable/disable built-in detectors

            enable_guardrails_gateway (bool): Boolean flag to enable/disable the guardrails sidecar gateway

            env (list[Any]): Define environment variables. These will be added to the orchestrator,
              gateway, and built-in detector pods.

            guardrails_gateway_config (str):  Name of the configmap containing guadrails sidecar gateway arguments

            log_level (str): Set log level in the orchestrator deployment

            orchestrator_config (str): Name of configmap containing generator, detector, and chunker
              arguments

            otel_exporter (dict[str, Any]): List of orchestrator enviroment variables for configuring the OTLP
              exporter

            replicas (int): INSERT ADDITIONAL SPEC FIELDS - desired state of cluster Important:
              Run "make" to regenerate code after modifying this file Number of
              replicas

            tls_secrets (list[Any]): Define TLS secrets to be mounted to the orchestrator. Secrets will be
              mounted at /etc/tls/$SECRET_NAME

        """
        super().__init__(**kwargs)

        self.auto_config = auto_config
        self.custom_detectors_config = custom_detectors_config
        self.disable_orchestrator = disable_orchestrator
        self.enable_built_in_detectors = enable_built_in_detectors
        self.enable_guardrails_gateway = enable_guardrails_gateway
        self.env = env
        self.guardrails_gateway_config = guardrails_gateway_config
        self.log_level = log_level
        self.orchestrator_config = orchestrator_config
        self.otel_exporter = otel_exporter
        self.replicas = replicas
        self.tls_secrets = tls_secrets

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

            if self.custom_detectors_config is not None:
                _spec["customDetectorsConfig"] = self.custom_detectors_config

            if self.disable_orchestrator is not None:
                _spec["disableOrchestrator"] = self.disable_orchestrator

            if self.enable_built_in_detectors is not None:
                _spec["enableBuiltInDetectors"] = self.enable_built_in_detectors

            if self.enable_guardrails_gateway is not None:
                _spec["enableGuardrailsGateway"] = self.enable_guardrails_gateway

            if self.env is not None:
                _spec["env"] = self.env

            if self.guardrails_gateway_config is not None:
                _spec["guardrailsGatewayConfig"] = self.guardrails_gateway_config

            if self.log_level is not None:
                _spec["logLevel"] = self.log_level

            if self.orchestrator_config is not None:
                _spec["orchestratorConfig"] = self.orchestrator_config

            if self.otel_exporter is not None:
                _spec["otelExporter"] = self.otel_exporter

            if self.tls_secrets is not None:
                _spec["tlsSecrets"] = self.tls_secrets

    # End of generated code
