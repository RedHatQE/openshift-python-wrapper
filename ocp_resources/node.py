# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class Node(Resource):
    """
    Node is a worker node in Kubernetes. Each node will have a unique identifier
    in the cache (i.e. in etcd).

    API Link: https://docs.openshift.com/container-platform/4.16/rest_api/node_apis/node-v1.html
    """

    api_version: str = "v1"

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
            config_source(Dict[str, Any]): The source to get node configuration parameters from. Example:
                {
                    "configMap": {
                        "name": "node-config",
                        "namespace": "default"
                    }
                }
            external_id(str): Deprecated field, external ID of the node.
            pod_cidr(str): The CIDR block for Pods on this node.
            pod_cidrs(Dict[str, Any]): The list of CIDR blocks for Pods on this node. Example:
                {
                    "cidr": "192.168.0.0/16"
                }
            provider_id(str): Identifier of the node assigned by the cloud provider.
            taints(Dict[str, Any]): List of taints applied to the node to prevent certain pods from being scheduled on it. Example:
                {
                    "key": "example-key",
                    "value": "example-value",
                    "effect": "NoSchedule"
                }
                This taint would prevent pods that do not tolerate the taint from being scheduled on this node.
            unschedulable(bool): If true, the node is marked as unschedulable to prevent new pods from being scheduled on it.
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

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.config_source:
                self.res["configSource"] = self.config_source

            if self.external_id:
                self.res["externalID"] = self.external_id

            if self.pod_cidr:
                self.res["podCIDR"] = self.pod_cidr

            if self.pod_cidrs:
                self.res["podCIDRs"] = self.pod_cidrs

            if self.provider_id:
                self.res["providerID"] = self.provider_id

            if self.taints:
                self.res["taints"] = self.taints

            if self.unschedulable is not None:
                self.res["unschedulable"] = self.unschedulable
