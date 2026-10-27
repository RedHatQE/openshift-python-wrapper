# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


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
        kubelet_config: dict[str, Any] | None = None,
        log_level: int | None = None,
        machine_config_pool_selector: dict[str, Any] | None = None,
        tls_security_profile: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            auto_sizing_reserved (bool): autoSizingReserved controls whether system-reserved CPU and memory are
              automatically calculated based on each node's installed capacity.
              When set to true, this prevents node failure from resource
              starvation of system components (kubelet, CRI-O) without manual
              configuration. When omitted, this means the user has no opinion
              and the platform is left to choose a reasonable default, which is
              subject to change over time. The current default is true for
              worker nodes and false for control plane nodes. When set to false,
              automatic resource reservation is disabled and manual settings
              must be configured.

            kubelet_config (dict[str, Any]): kubeletConfig contains upstream Kubernetes kubelet configuration
              fields. Values are validated by the kubelet itself. Invalid values
              may render nodes unusable. Refer to OpenShift documentation for
              the Kubernetes version corresponding to your OpenShift release to
              find valid kubelet configuration options.

            log_level (int): logLevel sets the kubelet log verbosity, controlling the amount of
              detail in kubelet logs. Valid values range from 0 (minimal
              logging) to 10 (maximum verbosity with trace-level detail). Higher
              log levels may impact node performance. When omitted, the platform
              chooses a reasonable default, which is subject to change over
              time. The current default is 2 (standard informational logging).

            machine_config_pool_selector (dict[str, Any]): machineConfigPoolSelector selects which pools the KubeletConfig should
              apply to. When omitted or set to an empty selector {}, no pools
              are selected, which is equivalent to not matching any
              MachineConfigPool.

            tls_security_profile (dict[str, Any]): tlsSecurityProfile configures TLS settings for the kubelet. When
              omitted, the TLS configuration defaults to the value from
              apiservers.config.openshift.io/cluster. When specified, the type
              field can be set to either "Old", "Intermediate", "Modern",
              "Custom" or omitted for backward compatibility.

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
