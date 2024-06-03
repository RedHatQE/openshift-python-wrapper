from typing import Any, Dict, List
from ocp_resources.resource import Resource


class Proxy(Resource):
    """
    https://docs.openshift.com/container-platform/4.15/rest_api/config_apis/proxy-config-openshift-io-v1.html
    """

    api_group = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        http_proxy: str = "",
        https_proxy: str = "",
        no_proxy: str = "",
        readiness_endpoints: List[str] | None = None,
        trusted_ca: Dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            http_proxy (str): URL of the proxy for HTTP requests.
            https_proxy (str): URL of the proxy for HTTPS requests.
            no_proxy (str): Comma-separated list of hostnames for which the proxy should not be used.
            readiness_endpoints (list): List of endpoints used to verify readiness of the proxy.
            trusted_ca (dict): Reference to a ConfigMap containing a CA certificate bundle.
                Example: {
                    "name": "trusted-ca-bundle",
                    "namespace": "openshift-config"
                }
        """
        super().__init__(**kwargs)
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.no_proxy = no_proxy
        self.readiness_endpoints = readiness_endpoints
        self.trusted_ca = trusted_ca

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            _spec = self.res.setdefault("spec", {})

            if self.http_proxy:
                _spec["httpProxy"] = self.http_proxy

            if self.https_proxy:
                _spec["httpsProxy"] = self.https_proxy

            if self.no_proxy:
                _spec["noProxy"] = self.no_proxy

            if self.readiness_endpoints:
                _spec["readinessEndpoints"] = self.readiness_endpoints

            if self.trusted_ca:
                _spec["trustedCA"] = self.trusted_ca
