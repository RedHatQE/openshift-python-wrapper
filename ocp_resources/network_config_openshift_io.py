# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import Resource


class Network(Resource):
    """
       Network holds cluster-wide information about Network. The canonical name is `cluster`. It is used to configure the desired network configuration, such as: IP address pools for services/pod IPs, network plugin, etc. Please view network.spec for an explanation on what applies when configuring this resource.
    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        cluster_network: Optional[List[Any]] = None,
        external_ip: Optional[Dict[str, Any]] = None,
        network_diagnostics: Optional[Dict[str, Any]] = None,
        network_type: Optional[str] = "",
        service_network: Optional[List[Any]] = None,
        service_node_port_range: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            cluster_network (List[Any]): IP address pool to use for pod IPs. This field is immutable after
              installation.

            external_ip (Dict[str, Any]): externalIP defines configuration for controllers that affect
              Service.ExternalIP. If nil, then ExternalIP is not allowed to be
              set.

            network_diagnostics (Dict[str, Any]): networkDiagnostics defines network diagnostics configuration.   Takes
              precedence over spec.disableNetworkDiagnostics in
              network.operator.openshift.io. If networkDiagnostics is not
              specified or is empty, and the spec.disableNetworkDiagnostics flag
              in network.operator.openshift.io is set to true, the network
              diagnostics feature will be disabled.

            network_type (str): NetworkType is the plugin that is to be deployed (e.g. OVNKubernetes).
              This should match a value that the cluster-network-operator
              understands, or else no networking will be installed. Currently
              supported values are: - OVNKubernetes This field is immutable
              after installation.

            service_network (List[Any]): IP address pool for services. Currently, we only support a single
              entry here. This field is immutable after installation.

            service_node_port_range (str): The port range allowed for Services of type NodePort. If not
              specified, the default of 30000-32767 will be used. Such Services
              without a NodePort specified will have one automatically allocated
              from this range. This parameter can be updated after the cluster
              is installed.

        """
        super().__init__(**kwargs)

        self.cluster_network = cluster_network
        self.external_ip = external_ip
        self.network_diagnostics = network_diagnostics
        self.network_type = network_type
        self.service_network = service_network
        self.service_node_port_range = service_node_port_range

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cluster_network:
                _spec["clusterNetwork"] = self.cluster_network

            if self.external_ip:
                _spec["externalIP"] = self.external_ip

            if self.network_diagnostics:
                _spec["networkDiagnostics"] = self.network_diagnostics

            if self.network_type:
                _spec["networkType"] = self.network_type

            if self.service_network:
                _spec["serviceNetwork"] = self.service_network

            if self.service_node_port_range:
                _spec["serviceNodePortRange"] = self.service_node_port_range

    # End of generated code
