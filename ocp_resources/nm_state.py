# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import Resource


class NMState(Resource):
    """
    NMState is the Schema for the nmstates API
    """

    api_group: str = Resource.ApiGroup.NMSTATE_IO

    def __init__(
        self,
        affinity: Optional[Dict[str, Any]] = None,
        infra_affinity: Optional[Dict[str, Any]] = None,
        infra_node_selector: Optional[Dict[str, Any]] = None,
        infra_tolerations: Optional[List[Any]] = None,
        node_selector: Optional[Dict[str, Any]] = None,
        self_sign_configuration: Optional[Dict[str, Any]] = None,
        tolerations: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            affinity (Dict[str, Any]): Affinity is an optional affinity selector that will be added to
              handler DaemonSet manifest.

            infra_affinity (Dict[str, Any]): Affinity is an optional affinity selector that will be added to
              webhook & certmanager Deployment manifests.

            infra_node_selector (Dict[str, Any]): InfraNodeSelector is an optional selector that will be added to
              webhook & certmanager Deployment manifests If InfraNodeSelector is
              specified, the webhook and certmanager will run only on nodes that
              have each of the indicated key-value pairs as labels applied to
              the node.

            infra_tolerations (List[Any]): InfraTolerations is an optional list of tolerations to be added to
              webhook & certmanager Deployment manifests If InfraTolerations is
              specified, the webhook and certmanager will be able to be
              scheduled on nodes with corresponding taints

            node_selector (Dict[str, Any]): NodeSelector is an optional selector that will be added to handler
              DaemonSet manifest for both workers and control-plane
              (https://github.com/nmstate/kubernetes-
              nmstate/blob/main/deploy/handler/operator.yaml). If NodeSelector
              is specified, the handler will run only on nodes that have each of
              the indicated key-value pairs as labels applied to the node.

            self_sign_configuration (Dict[str, Any]): SelfSignConfiguration defines self signed certificate configuration

            tolerations (List[Any]): Tolerations is an optional list of tolerations to be added to handler
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
        self.self_sign_configuration = self_sign_configuration
        self.tolerations = tolerations

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.affinity:
                _spec["affinity"] = self.affinity

            if self.infra_affinity:
                _spec["infraAffinity"] = self.infra_affinity

            if self.infra_node_selector:
                _spec["infraNodeSelector"] = self.infra_node_selector

            if self.infra_tolerations:
                _spec["infraTolerations"] = self.infra_tolerations

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.self_sign_configuration:
                _spec["selfSignConfiguration"] = self.self_sign_configuration

            if self.tolerations:
                _spec["tolerations"] = self.tolerations

    # End of generated code
