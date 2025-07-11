# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any

from ocp_resources.resource import Resource


class Node(Resource):
    """
    Node is a worker node in Kubernetes. Each node will have a unique identifier in the cache (i.e. in etcd).
    """

    api_version: str = Resource.ApiVersion.V1

    def __init__(
        self,
        config_source: dict[str, Any] | None = None,
        external_id: str | None = None,
        pod_cidr: str | None = None,
        pod_cidrs: list[Any] | None = None,
        provider_id: str | None = None,
        taints: list[Any] | None = None,
        unschedulable: bool | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            config_source (dict[str, Any]): NodeConfigSource specifies a source of node configuration. Exactly one
              subfield (excluding metadata) must be non-nil. This API is
              deprecated since 1.22

            external_id (str): Deprecated. Not all kubelets will set this field. Remove field after
              1.13. see: https://issues.k8s.io/61966

            pod_cidr (str): PodCIDR represents the pod IP range assigned to the node.

            pod_cidrs (list[Any]): podCIDRs represents the IP ranges assigned to the node for usage by
              Pods on that node. If this field is specified, the 0th entry must
              match the podCIDR field. It may contain at most 1 value for each
              of IPv4 and IPv6.

            provider_id (str): ID of the node assigned by the cloud provider in the format:
              <ProviderName>://<ProviderSpecificNodeID>

            taints (list[Any]): If specified, the node's taints.

            unschedulable (bool): Unschedulable controls node schedulability of new pods. By default,
              node is schedulable. More info:
              https://kubernetes.io/docs/concepts/nodes/node/#manual-node-
              administration

        """
        super().__init__(**kwargs)

        self.config_source = config_source
        self.external_id = external_id
        self.pod_cidr = pod_cidr
        self.pod_cidrs = pod_cidrs
        self.provider_id = provider_id
        self.taints = taints
        self.unschedulable = unschedulable

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.config_source is not None:
                _spec["configSource"] = self.config_source

            if self.external_id is not None:
                _spec["externalID"] = self.external_id

            if self.pod_cidr is not None:
                _spec["podCIDR"] = self.pod_cidr

            if self.pod_cidrs is not None:
                _spec["podCIDRs"] = self.pod_cidrs

            if self.provider_id is not None:
                _spec["providerID"] = self.provider_id

            if self.taints is not None:
                _spec["taints"] = self.taints

            if self.unschedulable is not None:
                _spec["unschedulable"] = self.unschedulable

    # End of generated code

    @property
    def kubelet_ready(self):
        return any(
            stat["reason"] == "KubeletReady" and stat["status"] == self.Condition.Status.TRUE
            for stat in self.instance.status.conditions
        )

    @property
    def machine_name(self):
        return self.instance.metadata.annotations[f"{self.ApiGroup.MACHINE_OPENSHIFT_IO}/machine"].split("/")[-1]

    @property
    def internal_ip(self):
        for addr in self.instance.status.addresses:
            if addr.type == "InternalIP":
                return addr.address

    @property
    def hostname(self):
        return self.labels["kubernetes.io/hostname"]

    def get_taints(self):
        return self.instance.get("spec", {}).get("taints")
