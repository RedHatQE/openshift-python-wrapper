# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

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
            egress (list[Any]): egress is a list of egress rules to be applied to the selected pods.
              Outgoing traffic is allowed if there are no NetworkPolicies
              selecting the pod (and cluster policy otherwise allows the
              traffic), OR if the traffic matches at least one egress rule
              across all of the NetworkPolicy objects whose podSelector matches
              the pod. If this field is empty then this NetworkPolicy limits all
              outgoing traffic (and serves solely to ensure that the pods it
              selects are isolated by default). This field is beta-level in 1.8

            ingress (list[Any]): ingress is a list of ingress rules to be applied to the selected pods.
              Traffic is allowed to a pod if there are no NetworkPolicies
              selecting the pod (and cluster policy otherwise allows the
              traffic), OR if the traffic source is the pod's local node, OR if
              the traffic matches at least one ingress rule across all of the
              NetworkPolicy objects whose podSelector matches the pod. If this
              field is empty then this NetworkPolicy does not allow any traffic
              (and serves solely to ensure that the pods it selects are isolated
              by default)

            pod_selector (dict[str, Any]): A label selector is a label query over a set of resources. The result
              of matchLabels and matchExpressions are ANDed. An empty label
              selector matches all objects. A null label selector matches no
              objects.

            policy_types (list[Any]): policyTypes is a list of rule types that the NetworkPolicy relates to.
              Valid options are ["Ingress"], ["Egress"], or ["Ingress",
              "Egress"]. If this field is not specified, it will default based
              on the existence of ingress or egress rules; policies that contain
              an egress section are assumed to affect egress, and all policies
              (whether or not they contain an ingress section) are assumed to
              affect ingress. If you want to write an egress-only policy, you
              must explicitly specify policyTypes [ "Egress" ]. Likewise, if you
              want to write a policy that specifies that no egress is allowed,
              you must specify a policyTypes value that include "Egress" (since
              such a policy would not include an egress section and would
              otherwise default to just [ "Ingress" ]). This field is beta-level
              in 1.8

        """
        super().__init__(**kwargs)

        self.egress = egress
        self.ingress = ingress
        self.pod_selector = pod_selector
        self.policy_types = policy_types

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.egress is not None:
                _spec["egress"] = self.egress

            if self.ingress is not None:
                _spec["ingress"] = self.ingress

            if self.pod_selector is not None:
                _spec["podSelector"] = self.pod_selector

            if self.policy_types is not None:
                _spec["policyTypes"] = self.policy_types

    # End of generated code
