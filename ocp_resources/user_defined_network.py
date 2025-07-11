# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from warnings import warn

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class UserDefinedNetwork(NamespacedResource):
    """
    UserDefinedNetwork describe network request for a Namespace.
    """

    api_group: str = NamespacedResource.ApiGroup.K8S_OVN_ORG

    def __init__(
        self,
        layer2: dict[str, Any] | None = None,
        layer3: dict[str, Any] | None = None,
        topology: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            layer2 (dict[str, Any]): Layer2 is the Layer2 topology configuration.

            layer3 (dict[str, Any]): Layer3 is the Layer3 topology configuration.

            topology (str): Topology describes network configuration.  Allowed values are
              "Layer3", "Layer2". Layer3 topology creates a layer 2 segment per
              node, each with a different subnet. Layer 3 routing is used to
              interconnect node subnets. Layer2 topology creates one logical
              switch shared by all nodes.

        """
        super().__init__(**kwargs)

        self.layer2 = layer2
        self.layer3 = layer3
        self.topology = topology

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.topology is None:
                raise MissingRequiredArgumentError(argument="self.topology")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["topology"] = self.topology

            if self.layer2 is not None:
                _spec["layer2"] = self.layer2

            if self.layer3 is not None:
                _spec["layer3"] = self.layer3

    # End of generated code

    def wait_for_network_ready(self, timeout: int = 30) -> None:
        """
        Wait for the network to be ready.

        Args:
            timeout (int, optional): Maximum time to wait in seconds. Defaults to 30.

        Raises:
            TimeoutExpiredError: If the network is not ready within the specified timeout.
        """
        self.wait_for_condition(
            condition=self.Condition.NETWORK_READY,
            status=self.Condition.Status.TRUE,
            timeout=timeout,
        )


class Layer2UserDefinedNetwork(UserDefinedNetwork):
    """
    UserDefinedNetwork layer2 object.

    API reference:
    https://ovn-kubernetes.io/api-reference/userdefinednetwork-api-spec/#layer2config
    """

    LAYER2: str = "Layer2"

    def __init__(
        self,
        role: str | None = None,
        mtu: int | None = None,
        subnets: list[str] | None = None,
        join_subnets: list[str] | None = None,
        ipam_lifecycle: str | None = None,
        ipam: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Create and manage UserDefinedNetwork with layer2 configuration

        Args:
            role (Optional[str]): role describes the network role in the pod.
            mtu (Optional[int]): mtu is the maximum transmission unit for a network.
            subnets (Optional[List[str]]): subnets are used for the pod network across the cluster.
            join_subnets (Optional[List[str]]): join_subnets are used inside the OVN network topology.
            ipam_lifecycle (Optional[str]): ipam_lifecycle controls IP addresses management lifecycle.
            ipam (Optional[dict[str, Any]]): ipam section contains IPAM-related configuration for the network.
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
        self.ipam = ipam

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
                if self.ipam:
                    raise ValueError("Cannot use both 'ipam_lifecycle' and 'ipam'.")

                warn(
                    message="ipam_lifecycle is deprecated and will be removed in v4.19. Use ipam instead.",
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                _layer2["ipam"] = self.ipam_lifecycle
            if self.ipam:
                _layer2["ipam"] = self.ipam


class Layer3UserDefinedNetwork(UserDefinedNetwork):
    """
    UserDefinedNetwork layer3 object.

    API reference:
    https://ovn-kubernetes.io/api-reference/userdefinednetwork-api-spec/#layer3config
    """

    LAYER3: str = "Layer3"

    def __init__(
        self,
        role: str | None = None,
        mtu: int | None = None,
        subnets: list[dict[str, Any]] | None = None,
        join_subnets: list[str] | None = None,
        **kwargs: Any,
    ):
        """
        Create and manage UserDefinedNetwork with layer3 configuration

        Args:
            role (Optional[str]): role describes the network role in the pod.
            mtu (Optional[int]): mtu is the maximum transmission unit for a network.
            subnets (Optional[List[Dict]]): subnets are used for the pod network across the cluster, each expecting:
                - `cidr` (str): IP range in CIDR notation.
                - `hostSubnet` (Optional[int]): Host-specific subnet.
                API reference:
                https://ovn-kubernetes.io/api-reference/userdefinednetwork-api-spec/#layer3subnet
            join_subnets (Optional[List[str]]): join_subnets are used inside the OVN network topology.
        """
        super().__init__(
            topology=self.LAYER3,
            **kwargs,
        )
        self.role = role
        self.mtu = mtu
        self.subnets = subnets
        self.join_subnets = join_subnets

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.role:
                raise MissingRequiredArgumentError(argument="role")
            if not self.subnets:
                raise MissingRequiredArgumentError(argument="subnets")

            self.res["spec"][self.LAYER3.lower()] = {"role": self.role}
            _layer3 = self.res["spec"][self.LAYER3.lower()]

            if self.mtu:
                _layer3["mtu"] = self.mtu

            if self.join_subnets:
                _layer3["joinSubnets"] = self.join_subnets

            if self.subnets:
                _layer3["subnets"] = self.subnets
