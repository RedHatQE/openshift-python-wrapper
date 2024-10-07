from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class MultiNetworkPolicy(NamespacedResource):
    """
    MultiNetworkPolicy object.

    API reference:
    https://docs.openshift.com/container-platform/4.14/networking/multiple_networks/configuring-multi-network-policy.html
    """

    api_group = NamespacedResource.ApiGroup.K8S_CNI_CNCF_IO

    def __init__(
        self,
        network_name=None,
        policy_types=None,
        ingress=None,
        egress=None,
        pod_selector=None,
        **kwargs,
    ):
        """
        Create and manage MultiNetworkPolicy

        Args:
            network_name (str): The name of the NetworkAttachmentDefinition that the policy will impact.
            policy_types (list, optional): One or more of the valid ip policies.
            ingress (list, optional): list containing a dictionary specifying the allowed "from" parameters.
            egress (list, optional): list containing a dictionary specifying the allowed "to" parameters.
            pod_selector (dict): Map a label to match.
        """
        super().__init__(**kwargs)
        self.network_name = network_name
        self.policy_types = policy_types
        self.pod_selector = pod_selector
        self.ingress = ingress
        self.egress = egress

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.network_name and self.pod_selector is None:
                raise MissingRequiredArgumentError("'network_name' and 'pod_selector'")

            self.res["metadata"]["annotations"] = {
                f"{NamespacedResource.ApiGroup.K8S_V1_CNI_CNCF_IO}/policy-for": f"{self.namespace}/{self.network_name}"
            }
            self.res["spec"] = {}
            self.res["spec"]["podSelector"] = self.pod_selector
            if self.policy_types:
                self.res["spec"]["policyTypes"] = self.policy_types
            if self.ingress is not None:
                self.res["spec"]["ingress"] = self.ingress
            if self.egress is not None:
                self.res["spec"]["egress"] = self.egress
