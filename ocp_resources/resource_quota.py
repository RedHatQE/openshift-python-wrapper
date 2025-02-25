# API reference: https://kubernetes.io/docs/reference/kubernetes-api/policy-resources/resource-quota-v1/

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class ResourceQuota(NamespacedResource):
    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        hard=None,
        scope_selector=None,
        scopes=None,
        **kwargs,
    ):
        """
        Create ResourceQuota object.

        Args:
            hard (dict): set of desired hard limits
                example: {"requests.cpu": "500m", "limits.cpu": 2}
            scope_selector (dict, optional): collection of filters
                example: {"matchExpressions": [{"operator": "In", "scopeName": "PriorityClass", "values": ["low"]}]}
            scopes (list, optional): collection of filters
                example: ["Terminating", "PriorityClass"]
        """
        super().__init__(**kwargs)
        self.hard = hard
        self.scope_selector = scope_selector
        self.scopes = scopes

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.hard:
                raise MissingRequiredArgumentError(argument="hard")

            spec = self.res.setdefault("spec", {})
            spec["hard"] = self.hard

            if self.scope_selector:
                spec["scopeSelector"] = self.scope_selector

            if self.scopes:
                spec["scopes"] = self.scopes
