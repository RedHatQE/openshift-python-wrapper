# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class DataScienceCluster(Resource):
    """
    DataScienceCluster is the Schema for the datascienceclusters API.

    API Link: https://github.com/opendatahub-io/opendatahub-operator/blob/incubation/apis/datasciencecluster/v1/datasciencecluster_types.go
    """

    api_group: str = Resource.ApiGroup.DATASCIENCECLUSTER_OPENDATAHUB_IO

    def __init__(
        self,
        components: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            components(Dict[Any, Any]): Override and fine tune specific component configurations.

              FIELDS:
                codeflare	<Object>
                  CodeFlare component configuration. If CodeFlare Operator has been installed
                  in the cluster, it should be uninstalled first before enabled component.

                dashboard	<Object>
                  Dashboard component configuration.

                datasciencepipelines	<Object>
                  DataServicePipeline component configuration. Require OpenShift Pipelines
                  Operator to be installed before enable component

                kserve	<Object>
                  Kserve component configuration. Require OpenShift Serverless and OpenShift
                  Service Mesh Operators to be installed before enable component Does not
                  support enabled ModelMeshServing at the same time

                kueue	<Object>
                  Kueue component configuration.

                modelmeshserving	<Object>
                  ModelMeshServing component configuration. Does not support enabled Kserve at
                  the same time

                ray	<Object>
                  Ray component configuration.

                trainingoperator	<Object>
                  Training Operator component configuration.

                trustyai	<Object>
                  TrustyAI component configuration.

                workbenches	<Object>
                  Workbenches component configuration.

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
