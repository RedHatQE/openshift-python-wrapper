# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import Resource


class VTEP(Resource):
    """
    VTEP defines VTEP (VXLAN Tunnel Endpoint) IP configuration for EVPN.
    """

    api_group: str = Resource.ApiGroup.K8S_OVN_ORG

    def __init__(
        self,
        cidrs: list[Any] | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            cidrs (list[Any]): CIDRs is the list of IP ranges from which VTEP IPs are discovered
              (unmanaged mode) or allocated (managed mode). Multiple CIDRs may
              be specified to expand capacity over time without recreating the
              VTEP. Each entry must be a valid network address in CIDR notation
              (for example, "100.64.0.0/24" or "fd00:100::/64"). Each node
              receives at most one IP per address family from the CIDRs listed
              here. In managed mode, CIDRs are consumed sequentially: IPs are
              allocated from the first CIDR until it is exhausted, then from the
              next, and so on. In managed mode, CIDRs are append-only: existing
              entries cannot be removed, reordered, or shrunk to a smaller mask;
              they can only be expanded to a wider mask, and new entries may be
              appended. In unmanaged mode, if multiple IPs on a node match the
              configured CIDRs, or if the match is otherwise ambiguous, the VTEP
              will be placed into a failed status. In unmanaged mode, CIDRs may
              be freely added, removed, reordered, or resized. Caution: removing
              or modifying CIDRs in unmanaged mode that are actively in use may
              cause traffic disruption; no downtime guarantees are provided for
              such operations.

            mode (str): Mode specifies how VTEP IPs are managed. "Managed" means OVN-
              Kubernetes allocates and assigns VTEP IPs per node automatically.
              "Unmanaged" means an external provider handles IP assignment; OVN-
              Kubernetes discovers existing IPs on nodes. Defaults to "Managed".

        """
        super().__init__(**kwargs)

        self.cidrs = cidrs
        self.mode = mode

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.cidrs is None:
                raise MissingRequiredArgumentError(argument="self.cidrs")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["cidrs"] = self.cidrs

            if self.mode is not None:
                _spec["mode"] = self.mode

    # End of generated code
