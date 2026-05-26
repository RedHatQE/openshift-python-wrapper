# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import Resource


class RouteAdvertisements(Resource):
    """
    RouteAdvertisements is the Schema for the routeadvertisements API
    """

    api_group: str = Resource.ApiGroup.K8S_OVN_ORG

    def __init__(
        self,
        advertisements: list[Any] | None = None,
        frr_configuration_selector: dict[str, Any] | None = None,
        network_selectors: list[Any] | None = None,
        node_selector: dict[str, Any] | None = None,
        target_vrf: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            advertisements (list[Any]): advertisements determines what is advertised.

            frr_configuration_selector (dict[str, Any]): frrConfigurationSelector determines which FRRConfigurations will the
              OVN-Kubernetes driven FRRConfigurations be based on. This field
              follows standard label selector semantics.

            network_selectors (list[Any]): networkSelectors determines which network routes should be advertised.
              Only ClusterUserDefinedNetworks and the default network can be
              selected.

            node_selector (dict[str, Any]): nodeSelector limits the advertisements to selected nodes. This field
              follows standard label selector semantics.

            target_vrf (str): targetVRF determines which VRF the routes should be advertised in.

        """
        super().__init__(**kwargs)

        self.advertisements = advertisements
        self.frr_configuration_selector = frr_configuration_selector
        self.network_selectors = network_selectors
        self.node_selector = node_selector
        self.target_vrf = target_vrf

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.advertisements is None:
                raise MissingRequiredArgumentError(argument="self.advertisements")

            if self.frr_configuration_selector is None:
                raise MissingRequiredArgumentError(argument="self.frr_configuration_selector")

            if self.network_selectors is None:
                raise MissingRequiredArgumentError(argument="self.network_selectors")

            if self.node_selector is None:
                raise MissingRequiredArgumentError(argument="self.node_selector")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["advertisements"] = self.advertisements
            _spec["frrConfigurationSelector"] = self.frr_configuration_selector
            _spec["networkSelectors"] = self.network_selectors
            _spec["nodeSelector"] = self.node_selector

            if self.target_vrf is not None:
                _spec["targetVRF"] = self.target_vrf

    # End of generated code
