# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any
from ocp_resources.resource import Resource


class Deployment(Resource):
    """
    Deployment enables declarative updates for Pods and ReplicaSets.
    """

    api_group: str = Resource.ApiGroup.APPS

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    # End of generated code
