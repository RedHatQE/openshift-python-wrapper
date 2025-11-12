# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class OAuth(Resource):
    """
        OAuth holds cluster-wide information about OAuth.  The canonical name is `cluster`.
    It is used to configure the integrated OAuth server.
    This configuration is only honored when the top level Authentication config has type set to IntegratedOAuth.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        identity_providers: list[Any] | None = None,
        templates: dict[str, Any] | None = None,
        token_config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            identity_providers (list[Any]): identityProviders is an ordered list of ways for a user to identify
              themselves. When this list is empty, no identities are provisioned
              for users.

            templates (dict[str, Any]): templates allow you to customize pages like the login page.

            token_config (dict[str, Any]): tokenConfig contains options for authorization and access tokens

        """
        super().__init__(**kwargs)

        self.identity_providers = identity_providers
        self.templates = templates
        self.token_config = token_config

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.identity_providers is not None:
                _spec["identityProviders"] = self.identity_providers

            if self.templates is not None:
                _spec["templates"] = self.templates

            if self.token_config is not None:
                _spec["tokenConfig"] = self.token_config

    # End of generated code
