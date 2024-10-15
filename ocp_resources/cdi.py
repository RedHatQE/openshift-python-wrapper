# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class CDI(Resource):
    """
    CDI is the CDI Operator CRD
    """

    api_group: str = Resource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        cert_config: Optional[Dict[str, Any]] = None,
        clone_strategy_override: Optional[str] = "",
        config: Optional[Dict[str, Any]] = None,
        customize_components: Optional[Dict[str, Any]] = None,
        image_pull_policy: Optional[str] = "",
        infra: Optional[Dict[str, Any]] = None,
        priority_class: Optional[str] = "",
        uninstall_strategy: Optional[str] = "",
        workload: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            cert_config (Dict[str, Any]): certificate configuration

            clone_strategy_override (str): Clone strategy override: should we use a host-assisted copy even if
              snapshots are available?

            config (Dict[str, Any]): CDIConfig at CDI level

            customize_components (Dict[str, Any]): CustomizeComponents defines patches for components deployed by the CDI
              operator.

            image_pull_policy (str): PullPolicy describes a policy for if/when to pull a container image

            infra (Dict[str, Any]): Selectors and tolerations that should apply to cdi infrastructure
              components

            priority_class (str): PriorityClass of the CDI control plane

            uninstall_strategy (str): CDIUninstallStrategy defines the state to leave CDI on uninstall

            workload (Dict[str, Any]): Restrict on which nodes CDI workload pods will be scheduled

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

            if self.cert_config:
                _spec["certConfig"] = self.cert_config

            if self.clone_strategy_override:
                _spec["cloneStrategyOverride"] = self.clone_strategy_override

            if self.config:
                _spec["config"] = self.config

            if self.customize_components:
                _spec["customizeComponents"] = self.customize_components

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.infra:
                _spec["infra"] = self.infra

            if self.priority_class:
                _spec["priorityClass"] = self.priority_class

            if self.uninstall_strategy:
                _spec["uninstallStrategy"] = self.uninstall_strategy

            if self.workload:
                _spec["workload"] = self.workload

    # End of generated code
