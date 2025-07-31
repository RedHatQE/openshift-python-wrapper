# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any

from ocp_resources.resource import Resource


class NodeNetworkConfigurationPolicy(Resource):
    """
    NodeNetworkConfigurationPolicy is the Schema for the nodenetworkconfigurationpolicies API
    """

    api_group: str = Resource.ApiGroup.NMSTATE_IO

    def __init__(
        self,
        capture: dict[str, Any] | None = None,
        desired_state: Any | None = None,
        max_unavailable: Any | None = None,
        node_selector: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            capture (dict[str, Any]): Capture contains expressions with an associated name than can be
              referenced at the DesiredState.

            desired_state (Any): The desired configuration of the policy

            max_unavailable (Any): MaxUnavailable specifies percentage or number of machines that can be
              updating at a time. Default is "50%".

            node_selector (dict[str, Any]): NodeSelector is a selector which must be true for the policy to be
              applied to the node. Selector which must match a node's labels for
              the policy to be scheduled on that node. More info:
              https://kubernetes.io/docs/concepts/configuration/assign-pod-node/

        """
        super().__init__(**kwargs)

        self.capture = capture
        self.desired_state = desired_state
        self.max_unavailable = max_unavailable
        self.node_selector = node_selector

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.capture is not None:
                _spec["capture"] = self.capture

            if self.desired_state is not None:
                _spec["desiredState"] = self.desired_state

            if self.max_unavailable is not None:
                _spec["maxUnavailable"] = self.max_unavailable

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

    # End of generated code
