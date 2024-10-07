# API reference: https://kubernetes.io/docs/reference/kubernetes-api/policy-resources/limit-range-v1/

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class LimitRange(NamespacedResource):
    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        limits=None,
        **kwargs,
    ):
        """
        Create LimitRange object.

        Args:
            limits (list of dict): List of limits
                example: [{"type": "Container", "default": {"cpu": "2"}, "max": {"cpu": "5"}}]
        """
        super().__init__(**kwargs)
        self.limits = limits

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.limits:
                raise MissingRequiredArgumentError(argument="limits")

            self.res.setdefault("spec", {})["limits"] = self.limits
