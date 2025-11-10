# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class SSP(NamespacedResource):
    """
    SSP is the Schema for the ssps API
    """

    api_group: str = NamespacedResource.ApiGroup.SSP_KUBEVIRT_IO

    def __init__(
        self,
        common_templates: dict[str, Any] | None = None,
        template_validator: dict[str, Any] | None = None,
        tls_security_profile: dict[str, Any] | None = None,
        token_generation_service: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            common_templates (dict[str, Any]): CommonTemplates is the configuration of the common templates operand

            template_validator (dict[str, Any]): TemplateValidator is configuration of the template validator operand

            tls_security_profile (dict[str, Any]): TLSSecurityProfile is a configuration for the TLS.

            token_generation_service (dict[str, Any]): TokenGenerationService configures the service for generating tokens to
              access VNC for a VM.

        """
        super().__init__(**kwargs)

        self.common_templates = common_templates
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

            if self.template_validator is not None:
                _spec["templateValidator"] = self.template_validator

            if self.tls_security_profile is not None:
                _spec["tlsSecurityProfile"] = self.tls_security_profile

            if self.token_generation_service is not None:
                _spec["tokenGenerationService"] = self.token_generation_service

    # End of generated code
