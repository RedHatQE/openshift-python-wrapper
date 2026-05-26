# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class FRRConfiguration(NamespacedResource):
    """
    FRRConfiguration is a piece of FRR configuration.
    """

    api_group: str = NamespacedResource.ApiGroup.FRRK8S_METALLB_IO

    def __init__(
        self,
        bgp: dict[str, Any] | None = None,
        node_selector: dict[str, Any] | None = None,
        raw: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            bgp (dict[str, Any]): BGP is the configuration related to the BGP protocol.

            node_selector (dict[str, Any]): NodeSelector limits the nodes that will attempt to apply this config.
              When specified, the configuration will be considered only on nodes
              whose labels match the specified selectors. When it is not
              specified all nodes will attempt to apply this config.

            raw (dict[str, Any]): Raw is a snippet of raw frr configuration that gets appended to the
              one rendered translating the type safe API.

        """
        super().__init__(**kwargs)

        self.bgp = bgp
        self.node_selector = node_selector
        self.raw = raw

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.bgp is not None:
                _spec["bgp"] = self.bgp

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

            if self.raw is not None:
                _spec["raw"] = self.raw

    # End of generated code
