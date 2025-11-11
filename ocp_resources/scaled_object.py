# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class ScaledObject(NamespacedResource):
    """
    ScaledObject is a specification for a ScaledObject resource
    """

    api_group: str = NamespacedResource.ApiGroup.KEDA_SH

    def __init__(
        self,
        advanced: dict[str, Any] | None = None,
        cooldown_period: int | None = None,
        fallback: dict[str, Any] | None = None,
        idle_replica_count: int | None = None,
        initial_cooldown_period: int | None = None,
        max_replica_count: int | None = None,
        min_replica_count: int | None = None,
        polling_interval: int | None = None,
        scale_target_ref: dict[str, Any] | None = None,
        triggers: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            advanced (dict[str, Any]): AdvancedConfig specifies advance scaling options

            cooldown_period (int): No field description from API

            fallback (dict[str, Any]): Fallback is the spec for fallback options

            idle_replica_count (int): No field description from API

            initial_cooldown_period (int): No field description from API

            max_replica_count (int): No field description from API

            min_replica_count (int): No field description from API

            polling_interval (int): No field description from API

            scale_target_ref (dict[str, Any]): ScaleTarget holds the reference to the scale target Object

            triggers (list[Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.advanced = advanced
        self.cooldown_period = cooldown_period
        self.fallback = fallback
        self.idle_replica_count = idle_replica_count
        self.initial_cooldown_period = initial_cooldown_period
        self.max_replica_count = max_replica_count
        self.min_replica_count = min_replica_count
        self.polling_interval = polling_interval
        self.scale_target_ref = scale_target_ref
        self.triggers = triggers

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.scale_target_ref is None:
                raise MissingRequiredArgumentError(argument="self.scale_target_ref")

            if self.triggers is None:
                raise MissingRequiredArgumentError(argument="self.triggers")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["scaleTargetRef"] = self.scale_target_ref
            _spec["triggers"] = self.triggers

            if self.advanced is not None:
                _spec["advanced"] = self.advanced

            if self.cooldown_period is not None:
                _spec["cooldownPeriod"] = self.cooldown_period

            if self.fallback is not None:
                _spec["fallback"] = self.fallback

            if self.idle_replica_count is not None:
                _spec["idleReplicaCount"] = self.idle_replica_count

            if self.initial_cooldown_period is not None:
                _spec["initialCooldownPeriod"] = self.initial_cooldown_period

            if self.max_replica_count is not None:
                _spec["maxReplicaCount"] = self.max_replica_count

            if self.min_replica_count is not None:
                _spec["minReplicaCount"] = self.min_replica_count

            if self.polling_interval is not None:
                _spec["pollingInterval"] = self.polling_interval

    # End of generated code
