# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class Authentication(Resource):
    """
        Authentication specifies cluster-wide settings for authentication (like OAuth and
    webhook token authenticators). The canonical name of an instance is `cluster`.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        oauth_metadata: dict[str, Any] | None = None,
        oidc_providers: list[Any] | None = None,
        service_account_issuer: str | None = None,
        type: str | None = None,
        webhook_token_authenticator: dict[str, Any] | None = None,
        webhook_token_authenticators: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            oauth_metadata (dict[str, Any]): oauthMetadata contains the discovery endpoint data for OAuth 2.0
              Authorization Server Metadata for an external OAuth server. This
              discovery document can be viewed from its served location: oc get
              --raw '/.well-known/oauth-authorization-server' For further
              details, see the IETF Draft: https://tools.ietf.org/html/draft-
              ietf-oauth-discovery-04#section-2 If oauthMetadata.name is non-
              empty, this value has precedence over any metadata reference
              stored in status. The key "oauthMetadata" is used to locate the
              data. If specified and the config map or expected key is not
              found, no metadata is served. If the specified metadata is not
              valid, no metadata is served. The namespace for this config map is
              openshift-config.

            oidc_providers (list[Any]): oidcProviders are OIDC identity providers that can issue tokens for
              this cluster Can only be set if "Type" is set to "OIDC".  At most
              one provider can be configured.

            service_account_issuer (str): serviceAccountIssuer is the identifier of the bound service account
              token issuer. The default is https://kubernetes.default.svc
              WARNING: Updating this field will not result in immediate
              invalidation of all bound tokens with the previous issuer value.
              Instead, the tokens issued by previous service account issuer will
              continue to be trusted for a time period chosen by the platform
              (currently set to 24h). This time period is subject to change over
              time. This allows internal components to transition to use new
              service account issuer without service distruption.

            type (str): type identifies the cluster managed, user facing authentication mode
              in use. Specifically, it manages the component that responds to
              login attempts. The default is IntegratedOAuth.

            webhook_token_authenticator (dict[str, Any]): webhookTokenAuthenticator configures a remote token reviewer. These
              remote authentication webhooks can be used to verify bearer tokens
              via the tokenreviews.authentication.k8s.io REST API. This is
              required to honor bearer tokens that are provisioned by an
              external authentication service.  Can only be set if "Type" is set
              to "None".

            webhook_token_authenticators (list[Any]): webhookTokenAuthenticators is DEPRECATED, setting it has no effect.

        """
        super().__init__(**kwargs)

        self.oauth_metadata = oauth_metadata
        self.oidc_providers = oidc_providers
        self.service_account_issuer = service_account_issuer
        self.type = type
        self.webhook_token_authenticator = webhook_token_authenticator
        self.webhook_token_authenticators = webhook_token_authenticators

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.oauth_metadata is not None:
                _spec["oauthMetadata"] = self.oauth_metadata

            if self.oidc_providers is not None:
                _spec["oidcProviders"] = self.oidc_providers

            if self.service_account_issuer is not None:
                _spec["serviceAccountIssuer"] = self.service_account_issuer

            if self.type is not None:
                _spec["type"] = self.type

            if self.webhook_token_authenticator is not None:
                _spec["webhookTokenAuthenticator"] = self.webhook_token_authenticator

            if self.webhook_token_authenticators is not None:
                _spec["webhookTokenAuthenticators"] = self.webhook_token_authenticators

    # End of generated code
