# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import Resource


class Operator(Resource):
    """
    Operator represents a cluster operator.
    """

    api_group: str = Resource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    # End of generated code
