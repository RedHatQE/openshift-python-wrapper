# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class DataScienceCluster(Resource):
    """
    DataScienceCluster is the Schema for the datascienceclusters API.

    API Link: https://github.com/opendatahub-io/opendatahub-operator/blob/incubation/apis/datasciencecluster/v1/datasciencecluster_types.go
    """

    api_version: str = "datasciencecluster.opendatahub.io/v1"

    def __init__(
        self,
        components: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            components(Dict[Any, Any]): Components of the DataScienceCluster"""
        super().__init__(**kwargs)

        self.components = components

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.components:
                self.res["components"] = self.components
