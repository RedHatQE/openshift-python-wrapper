# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class HTTPRoute(NamespacedResource):
    """
        HTTPRoute provides a way to route HTTP requests. This includes the capability
    to match requests by hostname, path, header, or query param. Filters can be
    used to specify additional processing steps. Backends specify where matching
    requests should be routed.
    """

    api_group: str = NamespacedResource.ApiGroup.GATEWAY_NETWORKING_K8S_IO

    def __init__(
        self,
        hostnames: list[Any] | None = None,
        parent_refs: list[Any] | None = None,
        rules: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            hostnames (list[Any]): Hostnames defines a set of hostnames that should match against the
              HTTP Host header to select a HTTPRoute used to process the
              request. Implementations MUST ignore any port value specified in
              the HTTP Host header while performing a match and (absent of any
              applicable header modification configuration) MUST forward this
              header unmodified to the backend.  Valid values for Hostnames are
              determined by RFC 1123 definition of a hostname with 2 notable
              exceptions:  1. IPs are not allowed. 2. A hostname may be prefixed
              with a wildcard label (`*.`). The wildcard    label must appear by
              itself as the first label.  If a hostname is specified by both the
              Listener and HTTPRoute, there must be at least one intersecting
              hostname for the HTTPRoute to be attached to the Listener. For
              example:  * A Listener with `test.example.com` as the hostname
              matches HTTPRoutes   that have either not specified any hostnames,
              or have specified at   least one of `test.example.com` or
              `*.example.com`. * A Listener with `*.example.com` as the hostname
              matches HTTPRoutes   that have either not specified any hostnames
              or have specified at least   one hostname that matches the
              Listener hostname. For example,   `*.example.com`,
              `test.example.com`, and `foo.test.example.com` would   all match.
              On the other hand, `example.com` and `test.example.net` would
              not match.  Hostnames that are prefixed with a wildcard label
              (`*.`) are interpreted as a suffix match. That means that a match
              for `*.example.com` would match both `test.example.com`, and
              `foo.test.example.com`, but not `example.com`.  If both the
              Listener and HTTPRoute have specified hostnames, any HTTPRoute
              hostnames that do not match the Listener hostname MUST be ignored.
              For example, if a Listener specified `*.example.com`, and the
              HTTPRoute specified `test.example.com` and `test.example.net`,
              `test.example.net` must not be considered for a match.  If both
              the Listener and HTTPRoute have specified hostnames, and none
              match with the criteria above, then the HTTPRoute is not accepted.
              The implementation must raise an 'Accepted' Condition with a
              status of `False` in the corresponding RouteParentStatus.  In the
              event that multiple HTTPRoutes specify intersecting hostnames
              (e.g. overlapping wildcard matching and exact matching hostnames),
              precedence must be given to rules from the HTTPRoute with the
              largest number of:  * Characters in a matching non-wildcard
              hostname. * Characters in a matching hostname.  If ties exist
              across multiple Routes, the matching precedence rules for
              HTTPRouteMatches takes over.  Support: Core

            parent_refs (list[Any]): ParentRefs references the resources (usually Gateways) that a Route
              wants to be attached to. Note that the referenced parent resource
              needs to allow this for the attachment to be complete. For
              Gateways, that means the Gateway needs to allow attachment from
              Routes of this kind and namespace. For Services, that means the
              Service must either be in the same namespace for a "producer"
              route, or the mesh implementation must support and allow
              "consumer" routes for the referenced Service. ReferenceGrant is
              not applicable for governing ParentRefs to Services - it is not
              possible to create a "producer" route for a Service in a different
              namespace from the Route.  There are two kinds of parent resources
              with "Core" support:  * Gateway (Gateway conformance profile) *
              Service (Mesh conformance profile, ClusterIP Services only)  This
              API may be extended in the future to support additional kinds of
              parent resources.  ParentRefs must be _distinct_. This means
              either that:  * They select different objects.  If this is the
              case, then parentRef   entries are distinct. In terms of fields,
              this means that the   multi-part key defined by `group`, `kind`,
              `namespace`, and `name` must   be unique across all parentRef
              entries in the Route. * They do not select different objects, but
              for each optional field used,   each ParentRef that selects the
              same object must set the same set of   optional fields to
              different values. If one ParentRef sets a   combination of
              optional fields, all must set the same combination.  Some
              examples:  * If one ParentRef sets `sectionName`, all ParentRefs
              referencing the   same object must also set `sectionName`. * If
              one ParentRef sets `port`, all ParentRefs referencing the same
              object must also set `port`. * If one ParentRef sets `sectionName`
              and `port`, all ParentRefs   referencing the same object must also
              set `sectionName` and `port`.  It is possible to separately
              reference multiple distinct objects that may be collapsed by an
              implementation. For example, some implementations may choose to
              merge compatible Gateway Listeners together. If that is the case,
              the list of routes attached to those resources should also be
              merged.  Note that for ParentRefs that cross namespace boundaries,
              there are specific rules. Cross-namespace references are only
              valid if they are explicitly allowed by something in the namespace
              they are referring to. For example, Gateway has the AllowedRoutes
              field, and ReferenceGrant provides a generic way to enable other
              kinds of cross-namespace reference.

            rules (list[Any]): Rules are a list of HTTP matchers, filters and actions.

        """
        super().__init__(**kwargs)

        self.hostnames = hostnames
        self.parent_refs = parent_refs
        self.rules = rules

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.hostnames is not None:
                _spec["hostnames"] = self.hostnames

            if self.parent_refs is not None:
                _spec["parentRefs"] = self.parent_refs

            if self.rules is not None:
                _spec["rules"] = self.rules

    # End of generated code
