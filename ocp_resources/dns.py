# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class DNS(Resource):
    """
    DNS holds cluster-wide information about DNS. The canonical name is
    `cluster`
     Compatibility level 1: Stable within a major release for a minimum of 12
    months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        base_domain: Optional[str] = "",
        platform: Optional[Dict[str, Any]] = None,
        private_zone: Optional[Dict[str, Any]] = None,
        public_zone: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            base_domain(str): baseDomain is the base domain of the cluster. All managed DNS records will
              be sub-domains of this base.
               For example, given the base domain `openshift.example.com`, an API server
              DNS record may be created for `cluster-api.openshift.example.com`.
               Once set, this field cannot be changed.

            platform(Dict[Any, Any]): platform holds configuration specific to the underlying infrastructure
              provider for DNS. When omitted, this means the user has no opinion and the
              platform is left to choose reasonable defaults. These defaults are subject
              to change over time.

              FIELDS:
                aws	<Object>
                  aws contains DNS configuration specific to the Amazon Web Services cloud
                  provider.

                type	<string> -required-
                  type is the underlying infrastructure provider for the cluster. Allowed
                  values: "", "AWS".
                   Individual components may not support all platforms, and must handle
                  unrecognized platforms with best-effort defaults.

            private_zone(Dict[Any, Any]): privateZone is the location where all the DNS records that are only
              available internally to the cluster exist.
               If this field is nil, no private records should be created.
               Once set, this field cannot be changed.

              FIELDS:
                id	<string>
                  id is the identifier that can be used to find the DNS hosted zone.
                   on AWS zone can be fetched using `ID` as id in [1] on Azure zone can be
                  fetched using `ID` as a pre-determined name in [2], on GCP zone can be
                  fetched using `ID` as a pre-determined name in [3].
                   [1]:
                  https://docs.aws.amazon.com/cli/latest/reference/route53/get-hosted-zone.html#options
                  [2]:
                  https://docs.microsoft.com/en-us/cli/azure/network/dns/zone?view=azure-cli-latest#az-network-dns-zone-show
                  [3]: https://cloud.google.com/dns/docs/reference/v1/managedZones/get

                tags	<map[string]string>
                  tags can be used to query the DNS hosted zone.
                   on AWS, resourcegroupstaggingapi [1] can be used to fetch a zone using
                  `Tags` as tag-filters,
                   [1]:
                  https://docs.aws.amazon.com/cli/latest/reference/resourcegroupstaggingapi/get-resources.html#options

            public_zone(Dict[Any, Any]): publicZone is the location where all the DNS records that are publicly
              accessible to the internet exist.
               If this field is nil, no public records should be created.
               Once set, this field cannot be changed.

              FIELDS:
                id	<string>
                  id is the identifier that can be used to find the DNS hosted zone.
                   on AWS zone can be fetched using `ID` as id in [1] on Azure zone can be
                  fetched using `ID` as a pre-determined name in [2], on GCP zone can be
                  fetched using `ID` as a pre-determined name in [3].
                   [1]:
                  https://docs.aws.amazon.com/cli/latest/reference/route53/get-hosted-zone.html#options
                  [2]:
                  https://docs.microsoft.com/en-us/cli/azure/network/dns/zone?view=azure-cli-latest#az-network-dns-zone-show
                  [3]: https://cloud.google.com/dns/docs/reference/v1/managedZones/get

                tags	<map[string]string>
                  tags can be used to query the DNS hosted zone.
                   on AWS, resourcegroupstaggingapi [1] can be used to fetch a zone using
                  `Tags` as tag-filters,
                   [1]:
                  https://docs.aws.amazon.com/cli/latest/reference/resourcegroupstaggingapi/get-resources.html#options

        """
        super().__init__(**kwargs)

        self.base_domain = base_domain
        self.platform = platform
        self.private_zone = private_zone
        self.public_zone = public_zone

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.base_domain:
                _spec["baseDomain"] = self.base_domain

            if self.platform:
                _spec["platform"] = self.platform

            if self.private_zone:
                _spec["privateZone"] = self.private_zone

            if self.public_zone:
                _spec["publicZone"] = self.public_zone
