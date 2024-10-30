# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError
from typing import List


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

        if not self.kind_dict and not self.yaml_file:
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

    @property
    def conditions(self) -> List:
        """
        Retrieve the current status conditions of the UserDefinedNetwork instance.

        Returns:
            list: A list of status conditions associated with the UserDefinedNetwork instance.
        """
        # Cache instance to avoid repeated API requests
        instance = self.instance
        if instance.status and instance.status.conditions:
            return instance.status.conditions
        return []

    @property
    def ready(self) -> bool:
        """
        Check if the UserDefinedNetwork is ready.

        Returns:
            bool: True if the UserDefinedNetwork is ready; otherwise, False.
        """
        return any(self.is_ready_condition(condition=condition) for condition in self.conditions)

    @property
    def sync_error(self) -> bool:
        """
        Check for synchronization errors in the UserDefinedNetwork.

        Returns:
            bool: True if there is a synchronization error; otherwise, False.
        """
        return any(self.is_sync_error_condition(condition=condition) for condition in self.conditions)


class Layer2UserDefinedNetwork(UserDefinedNetwork):
    """
    UserDefinedNetwork layer2 object.

    API reference:
    https://ovn-kubernetes.io/api-reference/userdefinednetwork-api-spec/#layer2config
    """

    LAYER2: str = "Layer2"

    def __init__(
        self,
        role: Optional[str] = None,
        mtu: Optional[int] = None,
        subnets: Optional[List[str]] = None,
        join_subnets: Optional[List[str]] = None,
        ipam_lifecycle: Optional[str] = None,
        **kwargs,
    ):
        """
        Create and manage UserDefinedNetwork with layer2 configuration

        Args:
            role (Optional[str]): role describes the network role in the pod.
            mtu (Optional[int]): mtu is the maximum transmission unit for a network.
            subnets (Optional[List[str]]): subnets are used for the pod network across the cluster.
            join_subnets (Optional[List[str]]): join_subnets are used inside the OVN network topology.
            ipam_lifecycle (Optional[str]): ipam_lifecycle controls IP addresses management lifecycle.
        """
        super().__init__(
            topology=self.LAYER2,
            **kwargs,
        )
        self.role = role
        self.mtu = mtu
        self.subnets = subnets
        self.join_subnets = join_subnets
        self.ipam_lifecycle = ipam_lifecycle

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.role:
                raise MissingRequiredArgumentError(argument="role")

            self.res["spec"][self.LAYER2.lower()] = {"role": self.role}
            _layer2 = self.res["spec"][self.LAYER2.lower()]

            if self.mtu:
                _layer2["mtu"] = self.mtu

            if self.subnets:
                _layer2["subnets"] = self.subnets

            if self.join_subnets:
                _layer2["joinSubnets"] = self.join_subnets

            if self.ipam_lifecycle:
                _layer2["ipamLifecycle"] = self.ipam_lifecycle
