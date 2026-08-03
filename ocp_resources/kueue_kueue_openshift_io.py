# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import Resource


class Kueue(Resource):
    """
    Kueue is the CRD to represent the Kueue operator.
    """

    api_group: str = Resource.ApiGroup.KUEUE_OPENSHIFT_IO

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        log_level: str | None = None,
        management_state: str | None = None,
        observed_config: dict[str, Any] | None = None,
        operator_log_level: str | None = None,
        unsupported_config_overrides: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            config (dict[str, Any]): config is the desired configuration for the Kueue operator.

            log_level (str): logLevel is an intent based logging for an overall component.  It does
              not give fine grained control, but it is a simple way to manage
              coarse grained logging choices that operators have to interpret
              for their operands.  Valid values are: "Normal", "Debug", "Trace",
              "TraceAll". Defaults to "Normal".

            management_state (str): managementState indicates whether and how the operator should manage
              the component

            observed_config (dict[str, Any]): observedConfig holds a sparse config that controller has observed from
              the cluster state.  It exists in spec because it is an input to
              the level for the operator

            operator_log_level (str): operatorLogLevel is an intent based logging for the operator itself.
              It does not give fine grained control, but it is a simple way to
              manage coarse grained logging choices that operators have to
              interpret for themselves.  Valid values are: "Normal", "Debug",
              "Trace", "TraceAll". Defaults to "Normal".

            unsupported_config_overrides (dict[str, Any]): unsupportedConfigOverrides overrides the final configuration that was
              computed by the operator. Red Hat does not support the use of this
              field. Misuse of this field could lead to unexpected behavior or
              conflict with other configuration options. Seek guidance from the
              Red Hat support before using this field. Use of this property
              blocks cluster upgrades, it must be removed before upgrading your
              cluster.

        """
        super().__init__(**kwargs)

        self.config = config
        self.log_level = log_level
        self.management_state = management_state
        self.observed_config = observed_config
        self.operator_log_level = operator_log_level
        self.unsupported_config_overrides = unsupported_config_overrides

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.config is not None:
                _spec["config"] = self.config

            if self.log_level is not None:
                _spec["logLevel"] = self.log_level

            if self.management_state is not None:
                _spec["managementState"] = self.management_state

            if self.observed_config is not None:
                _spec["observedConfig"] = self.observed_config

            if self.operator_log_level is not None:
                _spec["operatorLogLevel"] = self.operator_log_level

            if self.unsupported_config_overrides is not None:
                _spec["unsupportedConfigOverrides"] = self.unsupported_config_overrides

    # End of generated code
