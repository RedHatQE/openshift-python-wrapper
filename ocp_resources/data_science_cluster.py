# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class DataScienceCluster(Resource):
    """
    DataScienceCluster is the Schema for the datascienceclusters API.
    """

    api_group: str = Resource.ApiGroup.DATASCIENCECLUSTER_OPENDATAHUB_IO

    def __init__(
        self,
        components: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            components (Dict[str, Any]): Override and fine tune specific component configurations.

        """
        super().__init__(**kwargs)

        self.components = components

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.components:
                _spec["components"] = self.components

    # End of generated code
