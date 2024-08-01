# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import Resource


class OAuth(Resource):
    """
    OAuth holds cluster-wide information about OAuth.  The canonical name is
    `cluster`. It is used to configure the integrated OAuth server. This
    configuration is only honored when the top level Authentication config has
    type set to IntegratedOAuth.
     Compatibility level 1: Stable within a major release for a minimum of 12
    months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        identity_providers: Optional[List[Any]] = None,
        templates: Optional[Dict[str, Any]] = None,
        token_config: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            identity_providers(List[Any]): identityProviders is an ordered list of ways for a user to identify
              themselves. When this list is empty, no identities are provisioned for
              users.
              IdentityProvider provides identities for users authenticating using
              credentials

              FIELDS:
                basicAuth	<Object>
                  basicAuth contains configuration options for the BasicAuth IdP

                github	<Object>
                  github enables user authentication using GitHub credentials

                gitlab	<Object>
                  gitlab enables user authentication using GitLab credentials

                google	<Object>
                  google enables user authentication using Google credentials

                htpasswd	<Object>
                  htpasswd enables user authentication using an HTPasswd file to validate
                  credentials

                keystone	<Object>
                  keystone enables user authentication using keystone password credentials

                ldap	<Object>
                  ldap enables user authentication using LDAP credentials

                mappingMethod	<string>
                  mappingMethod determines how identities from this provider are mapped to
                  users Defaults to "claim"

                name	<string>
                  name is used to qualify the identities returned by this provider. - It MUST
                  be unique and not shared by any other identity provider used - It MUST be a
                  valid path segment: name cannot equal "." or ".." or contain "/" or "%" or
                  ":" Ref:
                  https://godoc.org/github.com/openshift/origin/pkg/user/apis/user/validation#ValidateIdentityProviderName

                openID	<Object>
                  openID enables user authentication using OpenID credentials

                requestHeader	<Object>
                  requestHeader enables user authentication using request header credentials

                type	<string>
                  type identifies the identity provider type for this entry.

            templates(Dict[Any, Any]): templates allow you to customize pages like the login page.

              FIELDS:
                error	<Object>
                  error is the name of a secret that specifies a go template to use to render
                  error pages during the authentication or grant flow. The key "errors.html"
                  is used to locate the template data. If specified and the secret or expected
                  key is not found, the default error page is used. If the specified template
                  is not valid, the default error page is used. If unspecified, the default
                  error page is used. The namespace for this secret is openshift-config.

                login	<Object>
                  login is the name of a secret that specifies a go template to use to render
                  the login page. The key "login.html" is used to locate the template data. If
                  specified and the secret or expected key is not found, the default login
                  page is used. If the specified template is not valid, the default login page
                  is used. If unspecified, the default login page is used. The namespace for
                  this secret is openshift-config.

                providerSelection	<Object>
                  providerSelection is the name of a secret that specifies a go template to
                  use to render the provider selection page. The key "providers.html" is used
                  to locate the template data. If specified and the secret or expected key is
                  not found, the default provider selection page is used. If the specified
                  template is not valid, the default provider selection page is used. If
                  unspecified, the default provider selection page is used. The namespace for
                  this secret is openshift-config.

            token_config(Dict[Any, Any]): tokenConfig contains options for authorization and access tokens

              FIELDS:
                accessTokenInactivityTimeout	<string>
                  accessTokenInactivityTimeout defines the token inactivity timeout for tokens
                  granted by any client. The value represents the maximum amount of time that
                  can occur between consecutive uses of the token. Tokens become invalid if
                  they are not used within this temporal window. The user will need to acquire
                  a new token to regain access once a token times out. Takes valid time
                  duration string such as "5m", "1.5h" or "2h45m". The minimum allowed value
                  for duration is 300s (5 minutes). If the timeout is configured per client,
                  then that value takes precedence. If the timeout value is not specified and
                  the client does not override the value, then tokens are valid until their
                  lifetime.
                   WARNING: existing tokens' timeout will not be affected (lowered) by
                  changing this value

                accessTokenInactivityTimeoutSeconds	<integer>
                  accessTokenInactivityTimeoutSeconds - DEPRECATED: setting this field has no
                  effect.

                accessTokenMaxAgeSeconds	<integer>
                  accessTokenMaxAgeSeconds defines the maximum age of access tokens

        """
        super().__init__(**kwargs)

        self.identity_providers = identity_providers
        self.templates = templates
        self.token_config = token_config

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.identity_providers:
                _spec["identityProviders"] = self.identity_providers

            if self.templates:
                _spec["templates"] = self.templates

            if self.token_config:
                _spec["tokenConfig"] = self.token_config
