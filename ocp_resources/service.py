# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class Service(NamespacedResource):
    """
    Service is a named abstraction of software service (for example, mysql) consisting of local port (for example 3306) that the proxy listens on, and the selector that determines which pods will answer requests sent through the proxy.
    """

    api_version: str = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        allocate_load_balancer_node_ports: Optional[bool] = None,
        cluster_ip: Optional[str] = "",
        cluster_ips: Optional[List[Any]] = None,
        external_ips: Optional[List[Any]] = None,
        external_name: Optional[str] = "",
        external_traffic_policy: Optional[str] = "",
        health_check_node_port: Optional[int] = None,
        internal_traffic_policy: Optional[str] = "",
        ip_families: Optional[List[Any]] = None,
        ip_family_policy: Optional[str] = "",
        load_balancer_class: Optional[str] = "",
        load_balancer_ip: Optional[str] = "",
        load_balancer_source_ranges: Optional[List[Any]] = None,
        ports: Optional[List[Any]] = None,
        publish_not_ready_addresses: Optional[bool] = None,
        selector: Optional[Dict[str, Any]] = None,
        session_affinity: Optional[str] = "",
        session_affinity_config: Optional[Dict[str, Any]] = None,
        traffic_distribution: Optional[str] = "",
        type: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            allocate_load_balancer_node_ports (bool): allocateLoadBalancerNodePorts defines if NodePorts will be
              automatically allocated for services with type LoadBalancer.
              Default is "true". It may be set to "false" if the cluster load-
              balancer does not rely on NodePorts.  If the caller requests
              specific NodePorts (by specifying a value), those requests will be
              respected, regardless of this field. This field may only be set
              for services with type LoadBalancer and will be cleared if the
              type is changed to any other type.

            cluster_ip (str): clusterIP is the IP address of the service and is usually assigned
              randomly. If an address is specified manually, is in-range (as per
              system configuration), and is not in use, it will be allocated to
              the service; otherwise creation of the service will fail. This
              field may not be changed through updates unless the type field is
              also being changed to ExternalName (which requires this field to
              be blank) or the type field is being changed from ExternalName (in
              which case this field may optionally be specified, as describe
              above).  Valid values are "None", empty string (""), or a valid IP
              address. Setting this to "None" makes a "headless service" (no
              virtual IP), which is useful when direct endpoint connections are
              preferred and proxying is not required.  Only applies to types
              ClusterIP, NodePort, and LoadBalancer. If this field is specified
              when creating a Service of type ExternalName, creation will fail.
              This field will be wiped when updating a Service to type
              ExternalName. More info:
              https://kubernetes.io/docs/concepts/services-
              networking/service/#virtual-ips-and-service-proxies

            cluster_ips (List[Any]): ClusterIPs is a list of IP addresses assigned to this service, and are
              usually assigned randomly.  If an address is specified manually,
              is in-range (as per system configuration), and is not in use, it
              will be allocated to the service; otherwise creation of the
              service will fail. This field may not be changed through updates
              unless the type field is also being changed to ExternalName (which
              requires this field to be empty) or the type field is being
              changed from ExternalName (in which case this field may optionally
              be specified, as describe above).  Valid values are "None", empty
              string (""), or a valid IP address.  Setting this to "None" makes
              a "headless service" (no virtual IP), which is useful when direct
              endpoint connections are preferred and proxying is not required.
              Only applies to types ClusterIP, NodePort, and LoadBalancer. If
              this field is specified when creating a Service of type
              ExternalName, creation will fail. This field will be wiped when
              updating a Service to type ExternalName.  If this field is not
              specified, it will be initialized from the clusterIP field.  If
              this field is specified, clients must ensure that clusterIPs[0]
              and clusterIP have the same value.  This field may hold a maximum
              of two entries (dual-stack IPs, in either order). These IPs must
              correspond to the values of the ipFamilies field. Both clusterIPs
              and ipFamilies are governed by the ipFamilyPolicy field. More
              info: https://kubernetes.io/docs/concepts/services-
              networking/service/#virtual-ips-and-service-proxies

            external_ips (List[Any]): externalIPs is a list of IP addresses for which nodes in the cluster
              will also accept traffic for this service.  These IPs are not
              managed by Kubernetes.  The user is responsible for ensuring that
              traffic arrives at a node with this IP.  A common example is
              external load-balancers that are not part of the Kubernetes
              system.

            external_name (str): externalName is the external reference that discovery mechanisms will
              return as an alias for this service (e.g. a DNS CNAME record). No
              proxying will be involved.  Must be a lowercase RFC-1123 hostname
              (https://tools.ietf.org/html/rfc1123) and requires `type` to be
              "ExternalName".

            external_traffic_policy (str): externalTrafficPolicy describes how nodes distribute service traffic
              they receive on one of the Service's "externally-facing" addresses
              (NodePorts, ExternalIPs, and LoadBalancer IPs). If set to "Local",
              the proxy will configure the service in a way that assumes that
              external load balancers will take care of balancing the service
              traffic between nodes, and so each node will deliver traffic only
              to the node-local endpoints of the service, without masquerading
              the client source IP. (Traffic mistakenly sent to a node with no
              endpoints will be dropped.) The default value, "Cluster", uses the
              standard behavior of routing to all endpoints evenly (possibly
              modified by topology and other features). Note that traffic sent
              to an External IP or LoadBalancer IP from within the cluster will
              always get "Cluster" semantics, but clients sending to a NodePort
              from within the cluster may need to take traffic policy into
              account when picking a node.  Possible enum values:  - `"Cluster"`
              routes traffic to all endpoints.  - `"Local"` preserves the source
              IP of the traffic by routing only to endpoints on the same node as
              the traffic was received on (dropping the traffic if there are no
              local endpoints).

            health_check_node_port (int): healthCheckNodePort specifies the healthcheck nodePort for the
              service. This only applies when type is set to LoadBalancer and
              externalTrafficPolicy is set to Local. If a value is specified, is
              in-range, and is not in use, it will be used.  If not specified, a
              value will be automatically allocated.  External systems (e.g.
              load-balancers) can use this port to determine if a given node
              holds endpoints for this service or not.  If this field is
              specified when creating a Service which does not need it, creation
              will fail. This field will be wiped when updating a Service to no
              longer need it (e.g. changing type). This field cannot be updated
              once set.

            internal_traffic_policy (str): InternalTrafficPolicy describes how nodes distribute service traffic
              they receive on the ClusterIP. If set to "Local", the proxy will
              assume that pods only want to talk to endpoints of the service on
              the same node as the pod, dropping the traffic if there are no
              local endpoints. The default value, "Cluster", uses the standard
              behavior of routing to all endpoints evenly (possibly modified by
              topology and other features).  Possible enum values:  -
              `"Cluster"` routes traffic to all endpoints.  - `"Local"` routes
              traffic only to endpoints on the same node as the client pod
              (dropping the traffic if there are no local endpoints).

            ip_families (List[Any]): IPFamilies is a list of IP families (e.g. IPv4, IPv6) assigned to this
              service. This field is usually assigned automatically based on
              cluster configuration and the ipFamilyPolicy field. If this field
              is specified manually, the requested family is available in the
              cluster, and ipFamilyPolicy allows it, it will be used; otherwise
              creation of the service will fail. This field is conditionally
              mutable: it allows for adding or removing a secondary IP family,
              but it does not allow changing the primary IP family of the
              Service. Valid values are "IPv4" and "IPv6".  This field only
              applies to Services of types ClusterIP, NodePort, and
              LoadBalancer, and does apply to "headless" services. This field
              will be wiped when updating a Service to type ExternalName.  This
              field may hold a maximum of two entries (dual-stack families, in
              either order).  These families must correspond to the values of
              the clusterIPs field, if specified. Both clusterIPs and ipFamilies
              are governed by the ipFamilyPolicy field.

            ip_family_policy (str): IPFamilyPolicy represents the dual-stack-ness requested or required by
              this Service. If there is no value provided, then this field will
              be set to SingleStack. Services can be "SingleStack" (a single IP
              family), "PreferDualStack" (two IP families on dual-stack
              configured clusters or a single IP family on single-stack
              clusters), or "RequireDualStack" (two IP families on dual-stack
              configured clusters, otherwise fail). The ipFamilies and
              clusterIPs fields depend on the value of this field. This field
              will be wiped when updating a service to type ExternalName.
              Possible enum values:  - `"PreferDualStack"` indicates that this
              service prefers dual-stack when the cluster is configured for
              dual-stack. If the cluster is not configured for dual-stack the
              service will be assigned a single IPFamily. If the IPFamily is not
              set in service.spec.ipFamilies then the service will be assigned
              the default IPFamily configured on the cluster  -
              `"RequireDualStack"` indicates that this service requires dual-
              stack. Using IPFamilyPolicyRequireDualStack on a single stack
              cluster will result in validation errors. The IPFamilies (and
              their order) assigned to this service is based on
              service.spec.ipFamilies. If service.spec.ipFamilies was not
              provided then it will be assigned according to how they are
              configured on the cluster. If service.spec.ipFamilies has only one
              entry then the alternative IPFamily will be added by apiserver  -
              `"SingleStack"` indicates that this service is required to have a
              single IPFamily. The IPFamily assigned is based on the default
              IPFamily used by the cluster or as identified by
              service.spec.ipFamilies field

            load_balancer_class (str): loadBalancerClass is the class of the load balancer implementation
              this Service belongs to. If specified, the value of this field
              must be a label-style identifier, with an optional prefix, e.g.
              "internal-vip" or "example.com/internal-vip". Unprefixed names are
              reserved for end-users. This field can only be set when the
              Service type is 'LoadBalancer'. If not set, the default load
              balancer implementation is used, today this is typically done
              through the cloud provider integration, but should apply for any
              default implementation. If set, it is assumed that a load balancer
              implementation is watching for Services with a matching class. Any
              default load balancer implementation (e.g. cloud providers) should
              ignore Services that set this field. This field can only be set
              when creating or updating a Service to type 'LoadBalancer'. Once
              set, it can not be changed. This field will be wiped when a
              service is updated to a non 'LoadBalancer' type.

            load_balancer_ip (str): Only applies to Service Type: LoadBalancer. This feature depends on
              whether the underlying cloud-provider supports specifying the
              loadBalancerIP when a load balancer is created. This field will be
              ignored if the cloud-provider does not support the feature.
              Deprecated: This field was under-specified and its meaning varies
              across implementations. Using it is non-portable and it may not
              support dual-stack. Users are encouraged to use implementation-
              specific annotations when available.

            load_balancer_source_ranges (List[Any]): If specified and supported by the platform, this will restrict traffic
              through the cloud-provider load-balancer will be restricted to the
              specified client IPs. This field will be ignored if the cloud-
              provider does not support the feature." More info:
              https://kubernetes.io/docs/tasks/access-application-
              cluster/create-external-load-balancer/

            ports (List[Any]): The list of ports that are exposed by this service. More info:
              https://kubernetes.io/docs/concepts/services-
              networking/service/#virtual-ips-and-service-proxies

            publish_not_ready_addresses (bool): publishNotReadyAddresses indicates that any agent which deals with
              endpoints for this Service should disregard any indications of
              ready/not-ready. The primary use case for setting this field is
              for a StatefulSet's Headless Service to propagate SRV DNS records
              for its Pods for the purpose of peer discovery. The Kubernetes
              controllers that generate Endpoints and EndpointSlice resources
              for Services interpret this to mean that all endpoints are
              considered "ready" even if the Pods themselves are not. Agents
              which consume only Kubernetes generated endpoints through the
              Endpoints or EndpointSlice resources can safely assume this
              behavior.

            selector (Dict[str, Any]): Route service traffic to pods with label keys and values matching this
              selector. If empty or not present, the service is assumed to have
              an external process managing its endpoints, which Kubernetes will
              not modify. Only applies to types ClusterIP, NodePort, and
              LoadBalancer. Ignored if type is ExternalName. More info:
              https://kubernetes.io/docs/concepts/services-networking/service/

            session_affinity (str): Supports "ClientIP" and "None". Used to maintain session affinity.
              Enable client IP based session affinity. Must be ClientIP or None.
              Defaults to None. More info:
              https://kubernetes.io/docs/concepts/services-
              networking/service/#virtual-ips-and-service-proxies  Possible enum
              values:  - `"ClientIP"` is the Client IP based.  - `"None"` - no
              session affinity.

            session_affinity_config (Dict[str, Any]): SessionAffinityConfig represents the configurations of session
              affinity.

            traffic_distribution (str): TrafficDistribution offers a way to express preferences for how
              traffic is distributed to Service endpoints. Implementations can
              use this field as a hint, but are not required to guarantee strict
              adherence. If the field is not set, the implementation will apply
              its default routing strategy. If set to "PreferClose",
              implementations should prioritize endpoints that are topologically
              close (e.g., same zone). This is an alpha field and requires
              enabling ServiceTrafficDistribution feature.

            type (str): type determines how the Service is exposed. Defaults to ClusterIP.
              Valid options are ExternalName, ClusterIP, NodePort, and
              LoadBalancer. "ClusterIP" allocates a cluster-internal IP address
              for load-balancing to endpoints. Endpoints are determined by the
              selector or if that is not specified, by manual construction of an
              Endpoints object or EndpointSlice objects. If clusterIP is "None",
              no virtual IP is allocated and the endpoints are published as a
              set of endpoints rather than a virtual IP. "NodePort" builds on
              ClusterIP and allocates a port on every node which routes to the
              same endpoints as the clusterIP. "LoadBalancer" builds on NodePort
              and creates an external load-balancer (if supported in the current
              cloud) which routes to the same endpoints as the clusterIP.
              "ExternalName" aliases this service to the specified externalName.
              Several other fields do not apply to ExternalName services. More
              info: https://kubernetes.io/docs/concepts/services-
              networking/service/#publishing-services-service-types  Possible
              enum values:  - `"ClusterIP"` means a service will only be
              accessible inside the cluster, via the cluster IP.  -
              `"ExternalName"` means a service consists of only a reference to
              an external name that kubedns or equivalent will return as a CNAME
              record, with no exposing or proxying of any pods involved.  -
              `"LoadBalancer"` means a service will be exposed via an external
              load balancer (if the cloud provider supports it), in addition to
              'NodePort' type.  - `"NodePort"` means a service will be exposed
              on one port of every node, in addition to 'ClusterIP' type.

        """
        super().__init__(**kwargs)

        self.allocate_load_balancer_node_ports = allocate_load_balancer_node_ports
        self.cluster_ip = cluster_ip
        self.cluster_ips = cluster_ips
        self.external_ips = external_ips
        self.external_name = external_name
        self.external_traffic_policy = external_traffic_policy
        self.health_check_node_port = health_check_node_port
        self.internal_traffic_policy = internal_traffic_policy
        self.ip_families = ip_families
        self.ip_family_policy = ip_family_policy
        self.load_balancer_class = load_balancer_class
        self.load_balancer_ip = load_balancer_ip
        self.load_balancer_source_ranges = load_balancer_source_ranges
        self.ports = ports
        self.publish_not_ready_addresses = publish_not_ready_addresses
        self.selector = selector
        self.session_affinity = session_affinity
        self.session_affinity_config = session_affinity_config
        self.traffic_distribution = traffic_distribution
        self.type = type

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.allocate_load_balancer_node_ports is not None:
                _spec["allocateLoadBalancerNodePorts"] = self.allocate_load_balancer_node_ports

            if self.cluster_ip:
                _spec["clusterIP"] = self.cluster_ip

            if self.cluster_ips:
                _spec["clusterIPs"] = self.cluster_ips

            if self.external_ips:
                _spec["externalIPs"] = self.external_ips

            if self.external_name:
                _spec["externalName"] = self.external_name

            if self.external_traffic_policy:
                _spec["externalTrafficPolicy"] = self.external_traffic_policy

            if self.health_check_node_port:
                _spec["healthCheckNodePort"] = self.health_check_node_port

            if self.internal_traffic_policy:
                _spec["internalTrafficPolicy"] = self.internal_traffic_policy

            if self.ip_families:
                _spec["ipFamilies"] = self.ip_families

            if self.ip_family_policy:
                _spec["ipFamilyPolicy"] = self.ip_family_policy

            if self.load_balancer_class:
                _spec["loadBalancerClass"] = self.load_balancer_class

            if self.load_balancer_ip:
                _spec["loadBalancerIP"] = self.load_balancer_ip

            if self.load_balancer_source_ranges:
                _spec["loadBalancerSourceRanges"] = self.load_balancer_source_ranges

            if self.ports:
                _spec["ports"] = self.ports

            if self.publish_not_ready_addresses is not None:
                _spec["publishNotReadyAddresses"] = self.publish_not_ready_addresses

            if self.selector:
                _spec["selector"] = self.selector

            if self.session_affinity:
                _spec["sessionAffinity"] = self.session_affinity

            if self.session_affinity_config:
                _spec["sessionAffinityConfig"] = self.session_affinity_config

            if self.traffic_distribution:
                _spec["trafficDistribution"] = self.traffic_distribution

            if self.type:
                _spec["type"] = self.type

    # End of generated code
