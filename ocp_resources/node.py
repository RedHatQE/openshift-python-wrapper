# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class Node(Resource):
    """
    Node is a worker node in Kubernetes. Each node will have a unique identifier
    in the cache (i.e. in etcd).
    """

    api_version: str = Resource.ApiVersion.V1

    class Status(Resource.Status):
        SCHEDULING_DISABLED = "Ready,SchedulingDisabled"

    def __init__(
        self,
        config_source: Optional[Dict[str, Any]] = None,
        external_id: Optional[str] = "",
        pod_cidr: Optional[str] = "",
        pod_cidrs: Optional[Dict[str, Any]] = None,
        provider_id: Optional[str] = "",
        taints: Optional[Dict[str, Any]] = None,
        unschedulable: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            config_source(Dict[Any, Any]): Deprecated: Previously used to specify the source of the node's
              configuration for the DynamicKubeletConfig feature. This feature is removed.
              NodeConfigSource specifies a source of node configuration. Exactly one
              subfield (excluding metadata) must be non-nil. This API is deprecated since
              1.22

              FIELDS:
                configMap	<ConfigMapNodeConfigSource>
                  ConfigMap is a reference to a Node's ConfigMap

            external_id(str): Deprecated. Not all kubelets will set this field. Remove field after 1.13.
              see: https://issues.k8s.io/61966

            pod_cidr(str): PodCIDR represents the pod IP range assigned to the node.

            pod_cidrs(Dict[Any, Any]): podCIDRs represents the IP ranges assigned to the node for usage by Pods on
              that node. If this field is specified, the 0th entry must match the podCIDR
              field. It may contain at most 1 value for each of IPv4 and IPv6.

            provider_id(str): ID of the node assigned by the cloud provider in the format:
              <ProviderName>://<ProviderSpecificNodeID>

            taints(Dict[Any, Any]): If specified, the node's taints.
              The node this Taint is attached to has the "effect" on any pod that does not
              tolerate the Taint.

              FIELDS:
                effect	<string> -required-
                  Required. The effect of the taint on pods that do not tolerate the taint.
                  Valid effects are NoSchedule, PreferNoSchedule and NoExecute.

                  Possible enum values:
                   - `"NoExecute"` Evict any already-running pods that do not tolerate the
                  taint. Currently enforced by NodeController.
                   - `"NoSchedule"` Do not allow new pods to schedule onto the node unless
                  they tolerate the taint, but allow all pods submitted to Kubelet without
                  going through the scheduler to start, and allow all already-running pods to
                  continue running. Enforced by the scheduler.
                   - `"PreferNoSchedule"` Like TaintEffectNoSchedule, but the scheduler tries
                  not to schedule new pods onto the node, rather than prohibiting new pods
                  from scheduling onto the node entirely. Enforced by the scheduler.

                key	<string> -required-
                  Required. The taint key to be applied to a node.

                timeAdded	<string>
                  TimeAdded represents the time at which the taint was added. It is only
                  written for NoExecute taints.

                value	<string>
                  The taint value corresponding to the taint key.

            unschedulable(bool): Unschedulable controls node schedulability of new pods. By default, node is
              schedulable. More info:
              https://kubernetes.io/docs/concepts/nodes/node/#manual-node-administration

        """
        super().__init__(**kwargs)

        self.config_source = config_source
        self.external_id = external_id
        self.pod_cidr = pod_cidr
        self.pod_cidrs = pod_cidrs
        self.provider_id = provider_id
        self._taints = taints
        self.unschedulable = unschedulable

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.config_source:
                _spec["configSource"] = self.config_source

            if self.external_id:
                _spec["externalID"] = self.external_id

            if self.pod_cidr:
                _spec["podCIDR"] = self.pod_cidr

            if self.pod_cidrs:
                _spec["podCIDRs"] = self.pod_cidrs

            if self.provider_id:
                _spec["providerID"] = self.provider_id

            if self.taints:
                _spec["taints"] = self._taints

            if self.unschedulable is not None:
                _spec["unschedulable"] = self.unschedulable

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

    @property
    def taints(self):
        return self.instance.get("spec", {}).get("taints")
