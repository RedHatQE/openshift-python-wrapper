# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class SSP(NamespacedResource):
    """
    SSP is the Schema for the ssps API
    """

    api_group: str = NamespacedResource.ApiGroup.SSP_KUBEVIRT_IO

    def __init__(
        self,
        common_instancetypes: Optional[Dict[str, Any]] = None,
        common_templates: Optional[Dict[str, Any]] = None,
        feature_gates: Optional[Dict[str, Any]] = None,
        tekton_pipelines: Optional[Dict[str, Any]] = None,
        tekton_tasks: Optional[Dict[str, Any]] = None,
        template_validator: Optional[Dict[str, Any]] = None,
        tls_security_profile: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            common_instancetypes (Dict[str, Any]): CommonInstancetypes is the configuration of the common-instancetypes
              operand   Deprecated: This functionality will be removed in a
              future release.

            common_templates (Dict[str, Any]): CommonTemplates is the configuration of the common templates operand

            feature_gates (Dict[str, Any]): FeatureGates for SSP

            tekton_pipelines (Dict[str, Any]): TektonPipelines is the configuration of the tekton-pipelines operand
              Deprecated: This field is ignored.

            tekton_tasks (Dict[str, Any]): TektonTasks is the configuration of the tekton-tasks operand
              Deprecated: This field is ignored.

            template_validator (Dict[str, Any]): TemplateValidator is configuration of the template validator operand

            tls_security_profile (Dict[str, Any]): TLSSecurityProfile is a configuration for the TLS.

        """
        super().__init__(**kwargs)

        self.common_instancetypes = common_instancetypes
        self.common_templates = common_templates
        self.feature_gates = feature_gates
        self.tekton_pipelines = tekton_pipelines
        self.tekton_tasks = tekton_tasks
        self.template_validator = template_validator
        self.tls_security_profile = tls_security_profile

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.common_templates:
                raise MissingRequiredArgumentError(argument="self.common_templates")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["commonTemplates"] = self.common_templates

            if self.common_instancetypes:
                _spec["commonInstancetypes"] = self.common_instancetypes

            if self.feature_gates:
                _spec["featureGates"] = self.feature_gates

            if self.tekton_pipelines:
                _spec["tektonPipelines"] = self.tekton_pipelines

            if self.tekton_tasks:
                _spec["tektonTasks"] = self.tekton_tasks

            if self.template_validator:
                _spec["templateValidator"] = self.template_validator

            if self.tls_security_profile:
                _spec["tlsSecurityProfile"] = self.tls_security_profile

    # End of generated code
