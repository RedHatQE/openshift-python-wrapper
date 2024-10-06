# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class UserDefinedNetwork(NamespacedResource):
    """
    UserDefinedNetwork describes network request for a Namespace.
    """

    api_group: str = NamespacedResource.ApiGroup.K8S_OVN_ORG

    def __init__(
        self,
        layer2: Optional[Dict[str, Any]] = None,
        layer3: Optional[Dict[str, Any]] = None,
        local_net: Optional[Dict[str, Any]] = None,
        topology: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            layer2 (Dict[str, Any]): Layer2 is the Layer2 topology configuration.

            layer3 (Dict[str, Any]): Layer3 is the Layer3 topology configuration.

            local_net (Dict[str, Any]): LocalNet is the LocalNet topology configuration.

            topology (str): Topology describes network configuration.   Allowed values are
              "Layer3", "Layer2", "LocalNet". Layer3 topology creates a layer 2
              segment per node, each with a different subnet. Layer 3 routing is
              used to interconnect node subnets. Layer2 topology creates one
              logical switch shared by all nodes. LocalNet topology creates a
              cluster-wide logical switch connected to a physical network.

        """
        super().__init__(**kwargs)

        self.layer2 = layer2
        self.layer3 = layer3
        self.local_net = local_net
        self.topology = topology

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            if not all([
                self.topology,
            ]):
                raise MissingRequiredArgumentError(argument="topology")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["topology"] = self.topology

            if self.layer2:
                _spec["layer2"] = self.layer2

            if self.layer3:
                _spec["layer3"] = self.layer3

            if self.local_net:
                _spec["localNet"] = self.local_net

    # End of generated code

    @classmethod
    def is_ready_condition(cls, condition: dict) -> bool:
        """
        Check if the given condition indicates that the UserDefinedNetwork is ready.

        Args:
            condition (dict): A dictionary representing the condition of the UserDefinedNetwork.

        Returns:
            bool: True if the condition indicates the UserDefinedNetwork is ready, False otherwise.
        """
        return (
            condition.get("reason") == cls.Condition.Reason.NETWORK_ATTACHMENT_DEFINITION_READY
            and condition.get("status") == cls.Condition.Status.TRUE
            and condition.get("type") == cls.Condition.Type.NETWORK_READY
        )

    @classmethod
    def is_sync_error_condition(cls, condition: dict) -> bool:
        """
        Check if the given condition indicates a synchronization error for the UserDefinedNetwork.

        Args:
            condition (dict): A dictionary representing the condition of the UserDefinedNetwork.

        Returns:
            bool: True if the condition indicates a synchronization error, False otherwise.
        """
        return (
            condition.get("reason") == cls.Condition.Reason.SYNC_ERROR
            and condition.get("status") == cls.Condition.Status.FALSE
            and condition.get("type") == cls.Condition.Type.NETWORK_READY
        )
