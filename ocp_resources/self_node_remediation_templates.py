# API reference: https://github.com/medik8s/self-node-remediation
from typing import Any

from ocp_resources.resource import NamespacedResource


class SelfNodeRemediationTemplate(NamespacedResource):
    """
    SelfNodeRemediationTemplate CRD
    """

    api_group = NamespacedResource.ApiGroup.SELF_NODE_REMEDIATION_MEDIK8S_IO

    def __init__(
        self,
        remediation_strategy: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Create SelfNodeRemediationTemplate object.

        Args:
            remediation_strategy (str, optional): The remediation method for unhealthy nodes.
        """
        super().__init__(
            **kwargs,
        )
        self.remediation_strategy = remediation_strategy

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            _spec = self.res["spec"] = {"template": {"spec": {}}}

            if self.remediation_strategy:
                _spec["template"]["spec"]["remediationStrategy"] = self.remediation_strategy
