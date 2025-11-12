# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class CDI(Resource):
    """
    CDI is the CDI Operator CRD
    """

    api_group: str = Resource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        cert_config: dict[str, Any] | None = None,
        clone_strategy_override: str | None = None,
        config: dict[str, Any] | None = None,
        customize_components: dict[str, Any] | None = None,
        image_pull_policy: str | None = None,
        infra: dict[str, Any] | None = None,
        priority_class: str | None = None,
        uninstall_strategy: str | None = None,
        workload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            cert_config (dict[str, Any]): certificate configuration

            clone_strategy_override (str): Clone strategy override: should we use a host-assisted copy even if
              snapshots are available?

            config (dict[str, Any]): CDIConfig at CDI level

            customize_components (dict[str, Any]): CustomizeComponents defines patches for components deployed by the CDI
              operator.

            image_pull_policy (str): PullPolicy describes a policy for if/when to pull a container image

            infra (dict[str, Any]): Selectors and tolerations that should apply to cdi infrastructure
              components

            priority_class (str): PriorityClass of the CDI control plane

            uninstall_strategy (str): CDIUninstallStrategy defines the state to leave CDI on uninstall

            workload (dict[str, Any]): Restrict on which nodes CDI workload pods will be scheduled

        """
        super().__init__(**kwargs)

        self.cert_config = cert_config
        self.clone_strategy_override = clone_strategy_override
        self.config = config
        self.customize_components = customize_components
        self.image_pull_policy = image_pull_policy
        self.infra = infra
        self.priority_class = priority_class
        self.uninstall_strategy = uninstall_strategy
        self.workload = workload

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cert_config is not None:
                _spec["certConfig"] = self.cert_config

            if self.clone_strategy_override is not None:
                _spec["cloneStrategyOverride"] = self.clone_strategy_override

            if self.config is not None:
                _spec["config"] = self.config

            if self.customize_components is not None:
                _spec["customizeComponents"] = self.customize_components

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.infra is not None:
                _spec["infra"] = self.infra

            if self.priority_class is not None:
                _spec["priorityClass"] = self.priority_class

            if self.uninstall_strategy is not None:
                _spec["uninstallStrategy"] = self.uninstall_strategy

            if self.workload is not None:
                _spec["workload"] = self.workload

    # End of generated code
