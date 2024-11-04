# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import NamespacedResource


class Pipeline(NamespacedResource):
    """
    No field description from API; please add description
    """

    api_group: str = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    # End of generated code
