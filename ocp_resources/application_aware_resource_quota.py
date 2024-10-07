# API reference: https://github.com/kubevirt/application-aware-quota/tree/main/staging/src/kubevirt.io/application-aware-quota-api/pkg/apis/core/v1alpha1
# TODO: update API reference when OCP doc is available
from __future__ import annotations
from typing import Dict, Any, List

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class ApplicationAwareResourceQuota(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.AAQ_KUBEVIRT_IO

    def __init__(
        self,
        hard: Dict[str, Any] | None = None,
        scope_selector: Dict[str, Any] | None = None,
        scopes: List[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Create ApplicationAwareResourceQuota object.

        Args:
            hard (dict): set of desired hard limits
                example: {"pod": 3, "requests.cpu": "500m", "requests.memory/vmi": "4Gi", "requests.instances/vmi": 2}
            scope_selector (dict, optional): collection of filters
                example: {"matchExpressions": [{"operator": "In", "scopeName": "PriorityClass", "values": ["low"]}]}
            scopes (list, optional): collection of filters
                example: ["Terminating", "PriorityClass"]
        """
        super().__init__(**kwargs)
        self.hard = hard
        self.scope_selector = scope_selector
        self.scopes = scopes

    def to_dict(self):
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.hard:
                raise MissingRequiredArgumentError(argument="hard")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["hard"] = self.hard

            if self.scope_selector:
                _spec["scopeSelector"] = self.scope_selector

            if self.scopes:
                _spec["scopes"] = self.scopes
