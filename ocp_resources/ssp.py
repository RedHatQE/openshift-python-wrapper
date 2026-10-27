# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class SSP(NamespacedResource):
    """
    SSP is the Schema for the ssps API
    """

    api_group: str = NamespacedResource.ApiGroup.SSP_KUBEVIRT_IO

    def __init__(
        self,
        common_instancetypes: dict[str, Any] | None = None,
        common_templates: dict[str, Any] | None = None,
        feature_gates: dict[str, Any] | None = None,
        tekton_pipelines: dict[str, Any] | None = None,
        tekton_tasks: dict[str, Any] | None = None,
        template_validator: dict[str, Any] | None = None,
        tls_security_profile: dict[str, Any] | None = None,
        token_generation_service: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            common_instancetypes (dict[str, Any]): CommonInstancetypes is ignored. Deprecated: This field is ignored.

            common_templates (dict[str, Any]): CommonTemplates is the configuration of the common templates operand

            feature_gates (dict[str, Any]): FeatureGates for SSP

            tekton_pipelines (dict[str, Any]): TektonPipelines is the configuration of the tekton-pipelines operand
              Deprecated: This field is ignored.

            tekton_tasks (dict[str, Any]): TektonTasks is the configuration of the tekton-tasks operand
              Deprecated: This field is ignored.

            template_validator (dict[str, Any]): TemplateValidator is configuration of the template validator operand

            tls_security_profile (dict[str, Any]): TLSSecurityProfile is a configuration for the TLS.

            token_generation_service (dict[str, Any]): TokenGenerationService configures the service for generating tokens to
              access VNC for a VM.

        """
        super().__init__(**kwargs)

        self.common_instancetypes = common_instancetypes
        self.common_templates = common_templates
        self.feature_gates = feature_gates
        self.tekton_pipelines = tekton_pipelines
        self.tekton_tasks = tekton_tasks
        self.template_validator = template_validator
        self.tls_security_profile = tls_security_profile
        self.token_generation_service = token_generation_service

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.common_templates is None:
                raise MissingRequiredArgumentError(argument="self.common_templates")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["commonTemplates"] = self.common_templates

            if self.common_instancetypes is not None:
                _spec["commonInstancetypes"] = self.common_instancetypes

            if self.feature_gates is not None:
                _spec["featureGates"] = self.feature_gates

            if self.tekton_pipelines is not None:
                _spec["tektonPipelines"] = self.tekton_pipelines

            if self.tekton_tasks is not None:
                _spec["tektonTasks"] = self.tekton_tasks

            if self.template_validator is not None:
                _spec["templateValidator"] = self.template_validator

            if self.tls_security_profile is not None:
                _spec["tlsSecurityProfile"] = self.tls_security_profile

            if self.token_generation_service is not None:
                _spec["tokenGenerationService"] = self.token_generation_service

    # End of generated code
