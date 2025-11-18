# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class Ingress(Resource):
    """
        Ingress holds cluster-wide information about ingress, including the default ingress domain
    used for routes. The canonical name is `cluster`.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        apps_domain: str | None = None,
        component_routes: list[Any] | None = None,
        domain: str | None = None,
        load_balancer: dict[str, Any] | None = None,
        required_hsts_policies: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            apps_domain (str): appsDomain is an optional domain to use instead of the one specified
              in the domain field when a Route is created without specifying an
              explicit host. If appsDomain is nonempty, this value is used to
              generate default host values for Route. Unlike domain, appsDomain
              may be modified after installation. This assumes a new
              ingresscontroller has been setup with a wildcard certificate.

            component_routes (list[Any]): componentRoutes is an optional list of routes that are managed by
              OpenShift components that a cluster-admin is able to configure the
              hostname and serving certificate for. The namespace and name of
              each route in this list should match an existing entry in the
              status.componentRoutes list.  To determine the set of configurable
              Routes, look at namespace and name of entries in the
              .status.componentRoutes list, where participating operators write
              the status of configurable routes.

            domain (str): domain is used to generate a default host name for a route when the
              route's host name is empty. The generated host name will follow
              this pattern: "<route-name>.<route-namespace>.<domain>".  It is
              also used as the default wildcard domain suffix for ingress. The
              default ingresscontroller domain will follow this pattern:
              "*.<domain>".  Once set, changing domain is not currently
              supported.

            load_balancer (dict[str, Any]): loadBalancer contains the load balancer details in general which are
              not only specific to the underlying infrastructure provider of the
              current cluster and are required for Ingress Controller to work on
              OpenShift.

            required_hsts_policies (list[Any]): requiredHSTSPolicies specifies HSTS policies that are required to be
              set on newly created  or updated routes matching the
              domainPattern/s and namespaceSelector/s that are specified in the
              policy. Each requiredHSTSPolicy must have at least a domainPattern
              and a maxAge to validate a route HSTS Policy route annotation, and
              affect route admission.  A candidate route is checked for HSTS
              Policies if it has the HSTS Policy route annotation:
              "haproxy.router.openshift.io/hsts_header" E.g.
              haproxy.router.openshift.io/hsts_header: max-
              age=31536000;preload;includeSubDomains  - For each candidate
              route, if it matches a requiredHSTSPolicy domainPattern and
              optional namespaceSelector, then the maxAge, preloadPolicy, and
              includeSubdomainsPolicy must be valid to be admitted.  Otherwise,
              the route is rejected. - The first match, by domainPattern and
              optional namespaceSelector, in the ordering of the
              RequiredHSTSPolicies determines the route's admission status. - If
              the candidate route doesn't match any requiredHSTSPolicy
              domainPattern and optional namespaceSelector, then it may use any
              HSTS Policy annotation.  The HSTS policy configuration may be
              changed after routes have already been created. An update to a
              previously admitted route may then fail if the updated route does
              not conform to the updated HSTS policy configuration. However,
              changing the HSTS policy configuration will not cause a route that
              is already admitted to stop working.  Note that if there are no
              RequiredHSTSPolicies, any HSTS Policy annotation on the route is
              valid.

        """
        super().__init__(**kwargs)

        self.apps_domain = apps_domain
        self.component_routes = component_routes
        self.domain = domain
        self.load_balancer = load_balancer
        self.required_hsts_policies = required_hsts_policies

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.apps_domain is not None:
                _spec["appsDomain"] = self.apps_domain

            if self.component_routes is not None:
                _spec["componentRoutes"] = self.component_routes

            if self.domain is not None:
                _spec["domain"] = self.domain

            if self.load_balancer is not None:
                _spec["loadBalancer"] = self.load_balancer

            if self.required_hsts_policies is not None:
                _spec["requiredHSTSPolicies"] = self.required_hsts_policies

    # End of generated code
