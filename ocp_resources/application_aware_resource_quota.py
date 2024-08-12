# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource


class ApplicationAwareResourceQuota(NamespacedResource):
    """
    ApplicationAwareResourceQuota defines resources that should be reserved for
    a VMI migration
    """

    api_group: str = NamespacedResource.ApiGroup.AAQ_KUBEVIRT_IO

    def __init__(
        self,
        hard: Optional[Dict[str, Any]] = None,
        scope_selector: Optional[Dict[str, Any]] = None,
        scopes: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            hard(Dict[str, Any]): hard is the set of desired hard limits for each named resource. More info:
              https://kubernetes.io/docs/concepts/policy/resource-quotas/
              example: {"pod": 3, "requests.cpu": "500m", "requests.memory/vmi": "4Gi", "requests.instances/vmi": 2}

            scope_selector(Dict[str, Any]): scopeSelector is also a collection of filters like scopes that must match
              each object tracked by a quota but expressed using ScopeSelectorOperator in
              combination with possible values. For a resource to match, both scopes AND
              scopeSelector (if specified in spec), must be matched.
              example: {"matchExpressions": [{"operator": "In", "scopeName": "PriorityClass", "values": ["low"]}]}

              FIELDS:
                matchExpressions	<[]Object>
                  A list of scope selector requirements by scope of the resources.

            scopes(str): A collection of filters that must match each object tracked by a quota. If
              not specified, the quota matches all objects.
              A ResourceQuotaScope defines a filter that must match each object tracked by
              a quota
              example: ["Terminating", "PriorityClass"]

        """
        super().__init__(**kwargs)

        self.hard = hard
        self.scope_selector = scope_selector
        self.scopes = scopes

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.hard:
                _spec["hard"] = self.hard

            if self.scope_selector:
                _spec["scopeSelector"] = self.scope_selector

            if self.scopes:
                _spec["scopes"] = self.scopes
