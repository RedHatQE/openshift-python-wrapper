# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class NetworkPolicy(NamespacedResource):
    """
    NetworkPolicy describes what network traffic is allowed for a set of Pods
    """

    api_group: str = NamespacedResource.ApiGroup.NETWORKING_K8S_IO

    def __init__(
        self,
        egress: list[Any] | None = None,
        ingress: list[Any] | None = None,
        pod_selector: dict[str, Any] | None = None,
        policy_types: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            egress (list[Any]): ports endPort port protocol enum: SCTP, TCP, UDP to ipBlock cidr
              except namespaceSelector matchExpressions key operator values
              matchLabels podSelector matchExpressions key operator values
              matchLabels.

            ingress (list[Any]): from ipBlock cidr except namespaceSelector matchExpressions key
              operator values matchLabels podSelector matchExpressions key
              operator values matchLabels ports endPort port protocol enum:
              SCTP, TCP, UDP.

            pod_selector (dict[str, Any]): matchExpressions key operator values matchLabels.

            policy_types (list[Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.egress = egress
        self.ingress = ingress
        self.pod_selector = pod_selector
        self.policy_types = policy_types

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.pod_selector is None:
                raise MissingRequiredArgumentError(argument="self.pod_selector")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["podSelector"] = self.pod_selector

            if self.egress is not None:
                _spec["egress"] = self.egress

            if self.ingress is not None:
                _spec["ingress"] = self.ingress

            if self.policy_types is not None:
                _spec["policyTypes"] = self.policy_types

    # End of generated code
