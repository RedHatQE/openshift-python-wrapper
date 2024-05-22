from typing import Any
from ocp_resources.resource import NamespacedResource


class IngressController(NamespacedResource):
    """
    https://github.com/Yaroksito/day2/blob/main/ingress/base/ingresscontrollers.operator.openshift.yaml
    """

    api_group = NamespacedResource.ApiGroup.OPERATOR_OPENSHIFT_IO

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    def to_dict(self) -> None:
        super().to_dict()
