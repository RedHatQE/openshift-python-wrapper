from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource


class IngressController(NamespacedResource):
    """
    https://docs.openshift.com/container-platform/4.15/rest_api/operator_apis/ingresscontroller-operator-openshift-io-v1.html
    """

    api_group = NamespacedResource.ApiGroup.OPERATOR_OPENSHIFT_IO

    def __init__(
        self,
        domain: Optional[str] = "",
        replicas: Optional[int] = None,
        endpoint_publishing_strategy: Optional[Dict[str, Any]] = None,
        default_certificate: Optional[Dict[str, str]] = None,
        namespace_selector: Optional[Dict[str, Any]] = None,
        node_selector: Optional[Dict[str, Any]] = None,
        route_selector: Optional[Dict[str, Any]] = None,
        tls_security_profile: Optional[Dict[str, Any]] = None,
        logging: Optional[Dict[str, Any]] = None,
        route_admission: Optional[Dict[str, Any]] = None,
        client_tls: Optional[Dict[str, Any]] = None,
        trusted_ca: Optional[Dict[str, Any]] = None,
        http_compression: Optional[Dict[str, str]] = None,
        http_empty_requests_policy: Optional[str] = "",
        http_error_code_pages: Optional[Dict[str, Any]] = None,
        http_headers: Optional[Dict[str, Any]] = None,
        node_placement: Optional[Dict[str, Any]] = None,
        tuning_options: Optional[Dict[str, Any]] = None,
        unsupported_config_overrides: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            domain (str, optional): The domain for the ingress controller.
            replicas (int, optional): The number of desired replicas.
            endpoint_publishing_strategy (dict, optional): The strategy for publishing endpoints.
                Example: {
                    "type": "LoadBalancerService",
                    "loadBalancer": {
                        "scope": "External"
                    }
                }
            default_certificate (dict, optional): A reference to a secret containing the default certificate.
                Example: {
                    "name": "default-cert-secret",
                    "namespace": "openshift-ingress"
                }
            namespace_selector (dict, optional): A selector to select which namespaces the ingress controller should observe.
                Example: {
                    "matchLabels": {
                        "app": "myapp"
                    }
                }
            node_selector (dict, optional): A selector to select nodes the ingress controller should run on.
                Example: {
                    "matchLabels": {
                        "node-role.kubernetes.io/worker": ""
                    }
                }
            route_selector (dict, optional): A selector to select which routes the ingress controller should observe.
                Example: {
                    "matchLabels": {
                        "route": "myroute"
                    }
                }
            tls_security_profile (dict, optional): Settings for TLS connections.
                Example: {
                    "type": "Intermediate"
                }
            logging (dict, optional): Parameters for logging.
                Example: {
                    "access": {
                        "destination": {
                            "type": "Container",
                            "name": "access-logs"
                        }
                    }
                }
            route_admission (dict, optional): Policy for handling new route claims.
                Example: {
                    "namespaceOwnership": "InterNamespaceAllowed"
                }
            client_tls (dict, optional): Client TLS settings, including `clientCA` and `clientCertificatePolicy`.
                Example: {
                    "clientCA": {
                        "name": "client-ca",
                        "namespace": "openshift-ingress"
                    },
                    "clientCertificatePolicy": "Required"
                }
            trusted_ca (dict, optional): TrustedCA data.
                Example: {
                    "name": "trusted-ca",
                    "namespace": "openshift-config"
                }
            http_compression (dict, optional): Policy for HTTP traffic compression.
                Example: {
                    "type": "Gzip"
                }
            http_empty_requests_policy (str, optional): Policy for handling HTTP connections if the connection times out.
            http_error_code_pages (dict, optional): Custom error pages.
                Example: {
                    "name": "custom-error-pages",
                    "namespace": "openshift-config"
                }
            http_headers (dict, optional): Policy for HTTP headers.
                Example: {
                    "setHeaders": {
                        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
                    }
                }
            node_placement (dict, optional): Control over the scheduling of the ingress controller.
                Example: {
                    "nodeSelector": {
                        "matchLabels": {
                            "kubernetes.io/os": "linux"
                        }
                    },
                    "tolerations": [
                        {
                            "effect": "NoSchedule",
                            "operator": "Exists"
                        }
                    ]
                }
            tuning_options (dict, optional): Parameters for adjusting the performance of ingress controller pods.
                Example: {
                    "maxConnections": 10000
                }
            unsupported_config_overrides (dict, optional): Unsupported configuration options.
                Example: {
                    "customConfig": "value"
                }
        """
        super().__init__(**kwargs)
        self.domain = domain
        self.replicas = replicas
        self.endpoint_publishing_strategy = endpoint_publishing_strategy
        self.default_certificate = default_certificate
        self.namespace_selector = namespace_selector
        self.node_selector = node_selector  # type: ignore
        self.route_selector = route_selector
        self.tls_security_profile = tls_security_profile
        self.logging = logging
        self.route_admission = route_admission
        self.client_tls = client_tls
        self.trusted_ca = trusted_ca
        self.http_compression = http_compression
        self.http_empty_requests_policy = http_empty_requests_policy
        self.http_error_code_pages = http_error_code_pages
        self.http_headers = http_headers
        self.node_placement = node_placement
        self.tuning_options = tuning_options
        self.unsupported_config_overrides = unsupported_config_overrides

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.domain:
                _spec["domain"] = self.domain

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.endpoint_publishing_strategy:
                _spec["endpointPublishingStrategy"] = self.endpoint_publishing_strategy

            if self.default_certificate:
                _spec["defaultCertificate"] = self.default_certificate

            if self.namespace_selector:
                _spec["namespaceSelector"] = self.namespace_selector

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.route_selector:
                _spec["routeSelector"] = self.route_selector

            if self.tls_security_profile:
                _spec["tlsSecurityProfile"] = self.tls_security_profile

            if self.logging:
                _spec["logging"] = self.logging

            if self.route_admission:
                _spec["routeAdmission"] = self.route_admission

            if self.client_tls:
                _spec["clientTLS"] = self.client_tls

            if self.trusted_ca:
                _spec["trustedCA"] = self.trusted_ca

            if self.http_compression:
                _spec["httpCompression"] = self.http_compression

            if self.http_empty_requests_policy:
                _spec["httpEmptyRequestsPolicy"] = self.http_empty_requests_policy

            if self.http_error_code_pages:
                _spec["httpErrorCodePages"] = self.http_error_code_pages

            if self.http_headers:
                _spec["httpHeaders"] = self.http_headers

            if self.node_placement:
                _spec["nodePlacement"] = self.node_placement

            if self.tuning_options:
                _spec["tuningOptions"] = self.tuning_options

            if self.unsupported_config_overrides:
                _spec["unsupportedConfigOverrides"] = self.unsupported_config_overrides
