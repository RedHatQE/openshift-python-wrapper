# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import Resource


class DNS(Resource):
    """
       DNS manages the CoreDNS component to provide a name resolution service for pods and services in the cluster.
    This supports the DNS-based service discovery specification: https://github.com/kubernetes/dns/blob/master/docs/specification.md
    More details: https://kubernetes.io/docs/tasks/administer-cluster/coredns
    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.OPERATOR_OPENSHIFT_IO

    def __init__(
        self,
        cache: Optional[Dict[str, Any]] = None,
        log_level: Optional[str] = "",
        management_state: Optional[str] = "",
        node_placement: Optional[Dict[str, Any]] = None,
        operator_log_level: Optional[str] = "",
        servers: Optional[List[Any]] = None,
        upstream_resolvers: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            cache (Dict[str, Any]): cache describes the caching configuration that applies to all server
              blocks listed in the Corefile. This field allows a cluster admin
              to optionally configure: * positiveTTL which is a duration for
              which positive responses should be cached. * negativeTTL which is
              a duration for which negative responses should be cached. If this
              is not configured, OpenShift will configure positive and negative
              caching with a default value that is subject to change. At the
              time of writing, the default positiveTTL is 900 seconds and the
              default negativeTTL is 30 seconds or as noted in the respective
              Corefile for your version of OpenShift.

            log_level (str): logLevel describes the desired logging verbosity for CoreDNS. Any one
              of the following values may be specified: * Normal logs errors
              from upstream resolvers. * Debug logs errors, NXDOMAIN responses,
              and NODATA responses. * Trace logs errors and all responses.
              Setting logLevel: Trace will produce extremely verbose logs. Valid
              values are: "Normal", "Debug", "Trace". Defaults to "Normal".

            management_state (str): managementState indicates whether the DNS operator should manage
              cluster DNS

            node_placement (Dict[str, Any]): nodePlacement provides explicit control over the scheduling of DNS
              pods.   Generally, it is useful to run a DNS pod on every node so
              that DNS queries are always handled by a local DNS pod instead of
              going over the network to a DNS pod on another node.  However,
              security policies may require restricting the placement of DNS
              pods to specific nodes. For example, if a security policy
              prohibits pods on arbitrary nodes from communicating with the API,
              a node selector can be specified to restrict DNS pods to nodes
              that are permitted to communicate with the API.  Conversely, if
              running DNS pods on nodes with a particular taint is desired, a
              toleration can be specified for that taint.   If unset, defaults
              are used. See nodePlacement for more details.

            operator_log_level (str): operatorLogLevel controls the logging level of the DNS Operator. Valid
              values are: "Normal", "Debug", "Trace". Defaults to "Normal".
              setting operatorLogLevel: Trace will produce extremely verbose
              logs.

            servers (List[Any]): servers is a list of DNS resolvers that provide name query delegation
              for one or more subdomains outside the scope of the cluster
              domain. If servers consists of more than one Server, longest
              suffix match will be used to determine the Server.   For example,
              if there are two Servers, one for "foo.com" and another for
              "a.foo.com", and the name query is for "www.a.foo.com", it will be
              routed to the Server with Zone "a.foo.com".   If this field is
              nil, no servers are created.

            upstream_resolvers (Dict[str, Any]): upstreamResolvers defines a schema for configuring CoreDNS to proxy
              DNS messages to upstream resolvers for the case of the default
              (".") server   If this field is not specified, the upstream used
              will default to /etc/resolv.conf, with policy "sequential"

        """
        super().__init__(**kwargs)

        self.cache = cache
        self.log_level = log_level
        self.management_state = management_state
        self.node_placement = node_placement
        self.operator_log_level = operator_log_level
        self.servers = servers
        self.upstream_resolvers = upstream_resolvers

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cache:
                _spec["cache"] = self.cache

            if self.log_level:
                _spec["logLevel"] = self.log_level

            if self.management_state:
                _spec["managementState"] = self.management_state

            if self.node_placement:
                _spec["nodePlacement"] = self.node_placement

            if self.operator_log_level:
                _spec["operatorLogLevel"] = self.operator_log_level

            if self.servers:
                _spec["servers"] = self.servers

            if self.upstream_resolvers:
                _spec["upstreamResolvers"] = self.upstream_resolvers

    # End of generated code
