# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, Resource


class ClusterResourceQuota(Resource):
    """
        ClusterResourceQuota mirrors ResourceQuota at a cluster scope.  This object is easily convertible to
    synthetic ResourceQuota object to allow quota evaluation re-use.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.QUOTA_OPENSHIFT_IO

    def __init__(
        self,
        quota: dict[str, Any] | None = None,
        selector: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            quota (dict[str, Any]): quota defines the desired quota

            selector (dict[str, Any]): selector is the selector used to match projects. It should only select
              active projects on the scale of dozens (though it can select many
              more less active projects).  These projects will contend on object
              creation through this resource.

        """
        super().__init__(**kwargs)

        self.quota = quota
        self.selector = selector

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.quota is None:
                raise MissingRequiredArgumentError(argument="self.quota")

            if self.selector is None:
                raise MissingRequiredArgumentError(argument="self.selector")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["quota"] = self.quota
            _spec["selector"] = self.selector

    # End of generated code
