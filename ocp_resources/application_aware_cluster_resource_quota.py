# API reference: https://github.com/kubevirt/application-aware-quota/tree/main/staging/src/kubevirt.io/application-aware-quota-api/pkg/apis/core/v1alpha1
# TODO: update API reference when OCP doc is available
from __future__ import annotations
from typing import Dict, Any

from ocp_resources.resource import MissingRequiredArgumentError, Resource


class ApplicationAwareClusterResourceQuota(Resource):
    api_group = Resource.ApiGroup.AAQ_KUBEVIRT_IO

    def __init__(
        self,
        quota: Dict[str, Any] | None = None,
        selector: Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Create ApplicationAwareClusterResourceQuota object.

        Args:
            quota (dict): defines the desired quota
                example: {"hard": {"pod": 3, "requests.cpu": "500m"}}
            selector (dict): Dict of Namespace labels/annotations to match
                example: {"annotations": {"acrq-annotation": "true"}, "labels": {"matchLabels": {"acrq-label": "true"}}}
        """
        super().__init__(**kwargs)
        self.quota = quota
        self.selector = selector

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if not (self.quota or self.selector):
                raise MissingRequiredArgumentError(argument="'quota' or 'selector'")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["quota"] = self.quota
            _spec["selector"] = self.selector
