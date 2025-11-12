# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class DNS(Resource):
    """
        DNS holds cluster-wide information about DNS. The canonical name is `cluster`

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        base_domain: str | None = None,
        platform: dict[str, Any] | None = None,
        private_zone: dict[str, Any] | None = None,
        public_zone: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            base_domain (str): baseDomain is the base domain of the cluster. All managed DNS records
              will be sub-domains of this base.  For example, given the base
              domain `openshift.example.com`, an API server DNS record may be
              created for `cluster-api.openshift.example.com`.  Once set, this
              field cannot be changed.

            platform (dict[str, Any]): platform holds configuration specific to the underlying infrastructure
              provider for DNS. When omitted, this means the user has no opinion
              and the platform is left to choose reasonable defaults. These
              defaults are subject to change over time.

            private_zone (dict[str, Any]): privateZone is the location where all the DNS records that are only
              available internally to the cluster exist.  If this field is nil,
              no private records should be created.  Once set, this field cannot
              be changed.

            public_zone (dict[str, Any]): publicZone is the location where all the DNS records that are publicly
              accessible to the internet exist.  If this field is nil, no public
              records should be created.  Once set, this field cannot be
              changed.

        """
        super().__init__(**kwargs)

        self.base_domain = base_domain
        self.platform = platform
        self.private_zone = private_zone
        self.public_zone = public_zone

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.base_domain is not None:
                _spec["baseDomain"] = self.base_domain

            if self.platform is not None:
                _spec["platform"] = self.platform

            if self.private_zone is not None:
                _spec["privateZone"] = self.private_zone

            if self.public_zone is not None:
                _spec["publicZone"] = self.public_zone

    # End of generated code
