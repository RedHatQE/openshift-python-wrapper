from typing import Any
from ocp_resources.resource import Resource


class Proxy(Resource):
    """
    https://github.com/Yaroksito/day2/blob/main/ingress/base/proxies.config.openshift.yaml
    """

    api_group = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    def to_dict(self) -> None:
        super().to_dict()
