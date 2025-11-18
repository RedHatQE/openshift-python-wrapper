# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class GatewayConfig(Resource):
    """
    GatewayConfig is the Schema for the gatewayconfigs API
    """

    api_group: str = Resource.ApiGroup.SERVICES_PLATFORM_OPENDATAHUB_IO

    def __init__(
        self,
        certificate: dict[str, Any] | None = None,
        cookie: dict[str, Any] | None = None,
        domain: str | None = None,
        oidc: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            certificate (dict[str, Any]): Certificate management

            cookie (dict[str, Any]): Cookie configuration for OAuth2 proxy (applies to both OIDC and
              OpenShift OAuth)

            domain (str): Domain configuration for the GatewayConfig Example: apps.example.com

            oidc (dict[str, Any]): OIDC configuration (used when cluster is in OIDC authentication mode)

        """
        super().__init__(**kwargs)

        self.certificate = certificate
        self.cookie = cookie
        self.domain = domain
        self.oidc = oidc

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.certificate is not None:
                _spec["certificate"] = self.certificate

            if self.cookie is not None:
                _spec["cookie"] = self.cookie

            if self.domain is not None:
                _spec["domain"] = self.domain

            if self.oidc is not None:
                _spec["oidc"] = self.oidc

    # End of generated code
