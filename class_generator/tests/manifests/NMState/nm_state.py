# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class NMState(Resource):
    """
    NMState is the Schema for the nmstates API
    """

    api_group: str = Resource.ApiGroup.NMSTATE_IO

    def __init__(
        self,
        affinity: dict[str, Any] | None = None,
        infra_affinity: dict[str, Any] | None = None,
        infra_node_selector: dict[str, Any] | None = None,
        infra_tolerations: list[Any] | None = None,
        node_selector: dict[str, Any] | None = None,
        probe_configuration: dict[str, Any] | None = None,
        self_sign_configuration: dict[str, Any] | None = None,
        tolerations: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            affinity (dict[str, Any]): Affinity is an optional affinity selector that will be added to
              handler DaemonSet manifest.

            infra_affinity (dict[str, Any]): InfraAffinity is an optional affinity selector that will be added to
              webhook, metrics & console-plugin Deployment manifests.

            infra_node_selector (dict[str, Any]): InfraNodeSelector is an optional selector that will be added to
              webhook, metrics & console-plugin Deployment manifests If
              InfraNodeSelector is specified, the webhook, metrics and the
              console plugin will run only on nodes that have each of the
              indicated key-value pairs as labels applied to the node.

            infra_tolerations (list[Any]): InfraTolerations is an optional list of tolerations to be added to
              webhook, metrics & console-plugin Deployment manifests If
              InfraTolerations is specified, the webhook, metrics and the
              console plugin will be able to be scheduled on nodes with
              corresponding taints

            node_selector (dict[str, Any]): NodeSelector is an optional selector that will be added to handler
              DaemonSet manifest for both workers and control-plane
              (https://github.com/nmstate/kubernetes-
              nmstate/blob/main/deploy/handler/operator.yaml). If NodeSelector
              is specified, the handler will run only on nodes that have each of
              the indicated key-value pairs as labels applied to the node.

            probe_configuration (dict[str, Any]): ProbeConfiguration is an optional configuration of NMstate probes
              testing various functionalities. If ProbeConfiguration is
              specified, the handler will use the config defined here instead of
              its default values.

            self_sign_configuration (dict[str, Any]): SelfSignConfiguration defines self signed certificate configuration

            tolerations (list[Any]): Tolerations is an optional list of tolerations to be added to handler
              DaemonSet manifest If Tolerations is specified, the handler
              daemonset will be also scheduled on nodes with corresponding
              taints

        """
        super().__init__(**kwargs)

        self.affinity = affinity
        self.infra_affinity = infra_affinity
        self.infra_node_selector = infra_node_selector
        self.infra_tolerations = infra_tolerations
        self.node_selector = node_selector
        self.probe_configuration = probe_configuration
        self.self_sign_configuration = self_sign_configuration
        self.tolerations = tolerations

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.infra_affinity is not None:
                _spec["infraAffinity"] = self.infra_affinity

            if self.infra_node_selector is not None:
                _spec["infraNodeSelector"] = self.infra_node_selector

            if self.infra_tolerations is not None:
                _spec["infraTolerations"] = self.infra_tolerations

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

            if self.probe_configuration is not None:
                _spec["probeConfiguration"] = self.probe_configuration

            if self.self_sign_configuration is not None:
                _spec["selfSignConfiguration"] = self.self_sign_configuration

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

    # End of generated code
