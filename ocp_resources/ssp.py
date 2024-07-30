# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class SSP(NamespacedResource):
    """
    SSP is the Schema for the ssps API

    API Link: https://github.com/kubevirt/ssp-operator/blob/main/docs/configuration.md
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
            common_instancetypes(Dict[Any, Any]): CommonInstancetypes is the configuration of the common-instancetypes operand


              Deprecated: This functionality will be removed in a future release.

              FIELDS:
                url	<string>
                  URL of a remote Kustomize target from which to generate and deploy
                  resources.


                  The following caveats apply to the provided URL:


                  * Only 'https://' and 'git://' URLs are supported.


                  * The URL must include '?ref=$ref' or '?version=$ref' pinning it to a
                  specific
                    reference. It is recommended that the reference be a specific commit or
                  tag
                    to ensure the generated contents does not change over time. As such it is
                    recommended not to use branches as the ref for the time being.


                  * Only VirtualMachineClusterPreference and VirtualMachineClusterInstancetype
                    resources generated from the URL are deployed by the operand.


                  See the following Kustomize documentation for more details:


                  remote targets
                  https://github.com/kubernetes-sigs/kustomize/blob/master/examples/remoteBuild.md

            common_templates(Dict[Any, Any]): CommonTemplates is the configuration of the common templates operand

              FIELDS:
                dataImportCronTemplates	<[]Object>
                  DataImportCronTemplates defines a list of DataImportCrons managed by the SSP
                  Operator. This is intended for images used by CommonTemplates.

                namespace	<string> -required-
                  Namespace is the k8s namespace where CommonTemplates should be installed

            feature_gates(Dict[Any, Any]): FeatureGates for SSP

              FIELDS:
                deployCommonInstancetypes	<boolean>
                  Enables deployment of the common-instancetypes bundles, defaults to true.

                deployTektonTaskResources	<boolean>
                  Deprecated: This field is ignored.

                deployVmConsoleProxy	<boolean>
                  <no description>

            tekton_pipelines(Dict[Any, Any]): TektonPipelines is the configuration of the tekton-pipelines operand
              Deprecated: This field is ignored.

              FIELDS:
                namespace	<string>
                  <no description>

            tekton_tasks(Dict[Any, Any]): TektonTasks is the configuration of the tekton-tasks operand
              Deprecated: This field is ignored.

              FIELDS:
                namespace	<string>
                  <no description>

            template_validator(Dict[Any, Any]): TemplateValidator is configuration of the template validator operand

              FIELDS:
                placement	<Object>
                  Placement describes the node scheduling configuration

                replicas	<integer>
                  Replicas is the number of replicas of the template validator pod

            tls_security_profile(Dict[Any, Any]): TLSSecurityProfile is a configuration for the TLS.

              FIELDS:
                custom	<Object>
                  custom is a user-defined TLS security profile. Be extremely careful using a
                  custom
                  profile as invalid configurations can be catastrophic. An example custom
                  profile
                  looks like this:


                    ciphers:


                      - ECDHE-ECDSA-CHACHA20-POLY1305


                      - ECDHE-RSA-CHACHA20-POLY1305


                      - ECDHE-RSA-AES128-GCM-SHA256


                      - ECDHE-ECDSA-AES128-GCM-SHA256


                    minTLSVersion: VersionTLS11

                intermediate	<Object>
                  intermediate is a TLS security profile based on:


                  https://wiki.mozilla.org/Security/Server_Side_TLS#Intermediate_compatibility_.28recommended.29


                  and looks like this (yaml):


                    ciphers:


                      - TLS_AES_128_GCM_SHA256


                      - TLS_AES_256_GCM_SHA384


                      - TLS_CHACHA20_POLY1305_SHA256


                      - ECDHE-ECDSA-AES128-GCM-SHA256


                      - ECDHE-RSA-AES128-GCM-SHA256


                      - ECDHE-ECDSA-AES256-GCM-SHA384


                      - ECDHE-RSA-AES256-GCM-SHA384


                      - ECDHE-ECDSA-CHACHA20-POLY1305


                      - ECDHE-RSA-CHACHA20-POLY1305


                      - DHE-RSA-AES128-GCM-SHA256


                      - DHE-RSA-AES256-GCM-SHA384


                    minTLSVersion: VersionTLS12

                modern	<Object>
                  modern is a TLS security profile based on:


                  https://wiki.mozilla.org/Security/Server_Side_TLS#Modern_compatibility


                  and looks like this (yaml):


                    ciphers:


                      - TLS_AES_128_GCM_SHA256


                      - TLS_AES_256_GCM_SHA384


                      - TLS_CHACHA20_POLY1305_SHA256


                    minTLSVersion: VersionTLS13

                old	<Object>
                  old is a TLS security profile based on:


                  https://wiki.mozilla.org/Security/Server_Side_TLS#Old_backward_compatibility


                  and looks like this (yaml):


                    ciphers:


                      - TLS_AES_128_GCM_SHA256


                      - TLS_AES_256_GCM_SHA384


                      - TLS_CHACHA20_POLY1305_SHA256


                      - ECDHE-ECDSA-AES128-GCM-SHA256


                      - ECDHE-RSA-AES128-GCM-SHA256


                      - ECDHE-ECDSA-AES256-GCM-SHA384


                      - ECDHE-RSA-AES256-GCM-SHA384


                      - ECDHE-ECDSA-CHACHA20-POLY1305


                      - ECDHE-RSA-CHACHA20-POLY1305


                      - DHE-RSA-AES128-GCM-SHA256


                      - DHE-RSA-AES256-GCM-SHA384


                      - DHE-RSA-CHACHA20-POLY1305


                      - ECDHE-ECDSA-AES128-SHA256


                      - ECDHE-RSA-AES128-SHA256


                      - ECDHE-ECDSA-AES128-SHA


                      - ECDHE-RSA-AES128-SHA


                      - ECDHE-ECDSA-AES256-SHA384


                      - ECDHE-RSA-AES256-SHA384


                      - ECDHE-ECDSA-AES256-SHA


                      - ECDHE-RSA-AES256-SHA


                      - DHE-RSA-AES128-SHA256


                      - DHE-RSA-AES256-SHA256


                      - AES128-GCM-SHA256


                      - AES256-GCM-SHA384


                      - AES128-SHA256


                      - AES256-SHA256


                      - AES128-SHA


                      - AES256-SHA


                      - DES-CBC3-SHA


                    minTLSVersion: VersionTLS10

                type	<string>
                  type is one of Old, Intermediate, Modern or Custom. Custom provides
                  the ability to specify individual TLS security profile parameters.
                  Old, Intermediate and Modern are TLS security profiles based on:


                  https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_configurations


                  The profiles are intent based, so they may change over time as new ciphers
                  are developed and existing ciphers
                  are found to be insecure.  Depending on precisely which ciphers are
                  available to a process, the list may be
                  reduced.


                  Note that the Modern profile is currently not supported because it is not
                  yet well adopted by common software libraries.

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

        if not self.yaml_file:
            if not all([
                self.common_templates,
            ]):
                raise MissingRequiredArgumentError(argument="common_templates")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            self.res["commonTemplates"] = self.common_templates

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
