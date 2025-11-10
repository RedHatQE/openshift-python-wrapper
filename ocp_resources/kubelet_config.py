# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class KubeletConfig(Resource):
    """
        KubeletConfig describes a customized Kubelet configuration.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.MACHINECONFIGURATION_OPENSHIFT_IO

    def __init__(
        self,
        auto_sizing_reserved: bool | None = None,
        kubelet_config: Any | None = None,
        log_level: int | None = None,
        machine_config_pool_selector: dict[str, Any] | None = None,
        tls_security_profile: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            auto_sizing_reserved (bool): No field description from API

            kubelet_config (Any): kubeletConfig fields are defined in kubernetes upstream. Please refer
              to the types defined in the version/commit used by OpenShift of
              the upstream kubernetes. It's important to note that, since the
              fields of the kubelet configuration are directly fetched from
              upstream the validation of those values is handled directly by the
              kubelet. Please refer to the upstream version of the relevant
              kubernetes for the valid values of these fields. Invalid values of
              the kubelet configuration fields may render cluster nodes
              unusable.

            log_level (int): No field description from API

            machine_config_pool_selector (dict[str, Any]): machineConfigPoolSelector selects which pools the KubeletConfig shoud
              apply to. A nil selector will result in no pools being selected.

            tls_security_profile (dict[str, Any]): If unset, the default is based on the
              apiservers.config.openshift.io/cluster resource. Note that only
              Old and Intermediate profiles are currently supported, and the
              maximum available minTLSVersion is VersionTLS12.

        """
        super().__init__(**kwargs)

        self.auto_sizing_reserved = auto_sizing_reserved
        self.kubelet_config = kubelet_config
        self.log_level = log_level
        self.machine_config_pool_selector = machine_config_pool_selector
        self.tls_security_profile = tls_security_profile

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.auto_sizing_reserved is not None:
                _spec["autoSizingReserved"] = self.auto_sizing_reserved

            if self.kubelet_config is not None:
                _spec["kubeletConfig"] = self.kubelet_config

            if self.log_level is not None:
                _spec["logLevel"] = self.log_level

            if self.machine_config_pool_selector is not None:
                _spec["machineConfigPoolSelector"] = self.machine_config_pool_selector

            if self.tls_security_profile is not None:
                _spec["tlsSecurityProfile"] = self.tls_security_profile

    # End of generated code
