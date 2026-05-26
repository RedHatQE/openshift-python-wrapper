# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class KubeDescheduler(NamespacedResource):
    """
    KubeDescheduler is the Schema for the deschedulers API
    """

    api_group: str = NamespacedResource.ApiGroup.OPERATOR_OPENSHIFT_IO

    def __init__(
        self,
        descheduling_interval_seconds: int | None = None,
        log_level: str | None = None,
        management_state: str | None = None,
        mode: str | None = None,
        observed_config: Any | None = None,
        operator_log_level: str | None = None,
        profile_customizations: dict[str, Any] | None = None,
        profiles: list[Any] | None = None,
        unsupported_config_overrides: Any | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            descheduling_interval_seconds (int): DeschedulingIntervalSeconds is the number of seconds between
              descheduler runs

            log_level (str): logLevel is an intent based logging for an overall component.  It does
              not give fine grained control, but it is a simple way to manage
              coarse grained logging choices that operators have to interpret
              for their operands.   Valid values are: "Normal", "Debug",
              "Trace", "TraceAll". Defaults to "Normal".

            management_state (str): managementState indicates whether and how the operator should manage
              the component

            mode (str): Mode configures the descheduler to either evict pods (Automatic) or to
              simulate the eviction (Predictive)

            observed_config (Any): observedConfig holds a sparse config that controller has observed from
              the cluster state.  It exists in spec because it is an input to
              the level for the operator

            operator_log_level (str): operatorLogLevel is an intent based logging for the operator itself.
              It does not give fine grained control, but it is a simple way to
              manage coarse grained logging choices that operators have to
              interpret for themselves.   Valid values are: "Normal", "Debug",
              "Trace", "TraceAll". Defaults to "Normal".

            profile_customizations (dict[str, Any]): ProfileCustomizations contains various parameters for modifying the
              default behavior of certain profiles

            profiles (list[Any]): Profiles sets which descheduler strategy profiles are enabled

            unsupported_config_overrides (Any): unsupportedConfigOverrides holds a sparse config that will override
              any previously set options.  It only needs to be the fields to
              override it will end up overlaying in the following order: 1.
              hardcoded defaults 2. observedConfig 3. unsupportedConfigOverrides

        """
        super().__init__(**kwargs)

        self.descheduling_interval_seconds = descheduling_interval_seconds
        self.log_level = log_level
        self.management_state = management_state
        self.mode = mode
        self.observed_config = observed_config
        self.operator_log_level = operator_log_level
        self.profile_customizations = profile_customizations
        self.profiles = profiles
        self.unsupported_config_overrides = unsupported_config_overrides

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.descheduling_interval_seconds is not None:
                _spec["deschedulingIntervalSeconds"] = self.descheduling_interval_seconds

            if self.log_level is not None:
                _spec["logLevel"] = self.log_level

            if self.management_state is not None:
                _spec["managementState"] = self.management_state

            if self.mode is not None:
                _spec["mode"] = self.mode

            if self.observed_config is not None:
                _spec["observedConfig"] = self.observed_config

            if self.operator_log_level is not None:
                _spec["operatorLogLevel"] = self.operator_log_level

            if self.profile_customizations is not None:
                _spec["profileCustomizations"] = self.profile_customizations

            if self.profiles is not None:
                _spec["profiles"] = self.profiles

            if self.unsupported_config_overrides is not None:
                _spec["unsupportedConfigOverrides"] = self.unsupported_config_overrides

    # End of generated code
