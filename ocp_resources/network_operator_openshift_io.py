# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import Resource


class Network(Resource):
    """
       Network describes the cluster's desired network configuration. It is consumed by the cluster-network-operator.
    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.OPERATOR_OPENSHIFT_IO

    def __init__(
        self,
        additional_networks: Optional[List[Any]] = None,
        cluster_network: Optional[List[Any]] = None,
        default_network: Optional[Dict[str, Any]] = None,
        deploy_kube_proxy: Optional[bool] = None,
        disable_multi_network: Optional[bool] = None,
        disable_network_diagnostics: Optional[bool] = None,
        export_network_flows: Optional[Dict[str, Any]] = None,
        kube_proxy_config: Optional[Dict[str, Any]] = None,
        log_level: Optional[str] = "",
        management_state: Optional[str] = "",
        migration: Optional[Dict[str, Any]] = None,
        observed_config: Optional[Any] = None,
        operator_log_level: Optional[str] = "",
        service_network: Optional[List[Any]] = None,
        unsupported_config_overrides: Optional[Any] = None,
        use_multi_network_policy: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            additional_networks (List[Any]): additionalNetworks is a list of extra networks to make available to
              pods when multiple networks are enabled.

            cluster_network (List[Any]): clusterNetwork is the IP address pool to use for pod IPs. Some network
              providers, e.g. OpenShift SDN, support multiple ClusterNetworks.
              Others only support one. This is equivalent to the cluster-cidr.

            default_network (Dict[str, Any]): defaultNetwork is the "default" network that all pods will receive

            deploy_kube_proxy (bool): deployKubeProxy specifies whether or not a standalone kube-proxy
              should be deployed by the operator. Some network providers include
              kube-proxy or similar functionality. If unset, the plugin will
              attempt to select the correct value, which is false when OpenShift
              SDN and ovn-kubernetes are used and true otherwise.

            disable_multi_network (bool): disableMultiNetwork specifies whether or not multiple pod network
              support should be disabled. If unset, this property defaults to
              'false' and multiple network support is enabled.

            disable_network_diagnostics (bool): disableNetworkDiagnostics specifies whether or not
              PodNetworkConnectivityCheck CRs from a test pod to every node,
              apiserver and LB should be disabled or not. If unset, this
              property defaults to 'false' and network diagnostics is enabled.
              Setting this to 'true' would reduce the additional load of the
              pods performing the checks.

            export_network_flows (Dict[str, Any]): exportNetworkFlows enables and configures the export of network flow
              metadata from the pod network by using protocols NetFlow, SFlow or
              IPFIX. Currently only supported on OVN-Kubernetes plugin. If
              unset, flows will not be exported to any collector.

            kube_proxy_config (Dict[str, Any]): kubeProxyConfig lets us configure desired proxy configuration. If not
              specified, sensible defaults will be chosen by OpenShift directly.
              Not consumed by all network providers - currently only openshift-
              sdn.

            log_level (str): logLevel is an intent based logging for an overall component.  It does
              not give fine grained control, but it is a simple way to manage
              coarse grained logging choices that operators have to interpret
              for their operands.   Valid values are: "Normal", "Debug",
              "Trace", "TraceAll". Defaults to "Normal".

            management_state (str): managementState indicates whether and how the operator should manage
              the component

            migration (Dict[str, Any]): migration enables and configures the cluster network migration. The
              migration procedure allows to change the network type and the MTU.

            observed_config (Any): observedConfig holds a sparse config that controller has observed from
              the cluster state.  It exists in spec because it is an input to
              the level for the operator

            operator_log_level (str): operatorLogLevel is an intent based logging for the operator itself.
              It does not give fine grained control, but it is a simple way to
              manage coarse grained logging choices that operators have to
              interpret for themselves.   Valid values are: "Normal", "Debug",
              "Trace", "TraceAll". Defaults to "Normal".

            service_network (List[Any]): serviceNetwork is the ip address pool to use for Service IPs
              Currently, all existing network providers only support a single
              value here, but this is an array to allow for growth.

            unsupported_config_overrides (Any): unsupportedConfigOverrides overrides the final configuration that was
              computed by the operator. Red Hat does not support the use of this
              field. Misuse of this field could lead to unexpected behavior or
              conflict with other configuration options. Seek guidance from the
              Red Hat support before using this field. Use of this property
              blocks cluster upgrades, it must be removed before upgrading your
              cluster.

            use_multi_network_policy (bool): useMultiNetworkPolicy enables a controller which allows for
              MultiNetworkPolicy objects to be used on additional networks as
              created by Multus CNI. MultiNetworkPolicy are similar to
              NetworkPolicy objects, but NetworkPolicy objects only apply to the
              primary interface. With MultiNetworkPolicy, you can control the
              traffic that a pod can receive over the secondary interfaces. If
              unset, this property defaults to 'false' and MultiNetworkPolicy
              objects are ignored. If 'disableMultiNetwork' is 'true' then the
              value of this field is ignored.

        """
        super().__init__(**kwargs)

        self.additional_networks = additional_networks
        self.cluster_network = cluster_network
        self.default_network = default_network
        self.deploy_kube_proxy = deploy_kube_proxy
        self.disable_multi_network = disable_multi_network
        self.disable_network_diagnostics = disable_network_diagnostics
        self.export_network_flows = export_network_flows
        self.kube_proxy_config = kube_proxy_config
        self.log_level = log_level
        self.management_state = management_state
        self.migration = migration
        self.observed_config = observed_config
        self.operator_log_level = operator_log_level
        self.service_network = service_network
        self.unsupported_config_overrides = unsupported_config_overrides
        self.use_multi_network_policy = use_multi_network_policy

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.additional_networks:
                _spec["additionalNetworks"] = self.additional_networks

            if self.cluster_network:
                _spec["clusterNetwork"] = self.cluster_network

            if self.default_network:
                _spec["defaultNetwork"] = self.default_network

            if self.deploy_kube_proxy is not None:
                _spec["deployKubeProxy"] = self.deploy_kube_proxy

            if self.disable_multi_network is not None:
                _spec["disableMultiNetwork"] = self.disable_multi_network

            if self.disable_network_diagnostics is not None:
                _spec["disableNetworkDiagnostics"] = self.disable_network_diagnostics

            if self.export_network_flows:
                _spec["exportNetworkFlows"] = self.export_network_flows

            if self.kube_proxy_config:
                _spec["kubeProxyConfig"] = self.kube_proxy_config

            if self.log_level:
                _spec["logLevel"] = self.log_level

            if self.management_state:
                _spec["managementState"] = self.management_state

            if self.migration:
                _spec["migration"] = self.migration

            if self.observed_config:
                _spec["observedConfig"] = self.observed_config

            if self.operator_log_level:
                _spec["operatorLogLevel"] = self.operator_log_level

            if self.service_network:
                _spec["serviceNetwork"] = self.service_network

            if self.unsupported_config_overrides:
                _spec["unsupportedConfigOverrides"] = self.unsupported_config_overrides

            if self.use_multi_network_policy is not None:
                _spec["useMultiNetworkPolicy"] = self.use_multi_network_policy

    # End of generated code
