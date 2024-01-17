from ocp_resources.resource import Resource


class DataScienceCluster(Resource):
    """
    DataScienceCluster Resource for RHOAI operator

    https://access.redhat.com/documentation/en-us/red_hat_openshift_ai_self-managed/2.5/html/installing_and_uninstalling_openshift_ai_self-managed/installing-and-managing-openshift-ai-components_component-install

    https://github.com/opendatahub-io/opendatahub-operator/blob/incubation/config/crd/bases/datasciencecluster.opendatahub.io_datascienceclusters.yaml

    https://github.com/opendatahub-io/opendatahub-operator/blob/incubation/apis/datasciencecluster/v1/datasciencecluster_types.go
    """

    api_group = Resource.ApiGroup.DATA_SCIENCE_CLUSTER

    class Condition(Resource.Condition):
        DASHBOARD_READY = "dashboardReady"
        WORKBENCHES_READY = "workbenchesReady"
        MODEL_MESH_READY = "model-meshReady"
        DATA_SCIENCE_PIPELINES_READY = "data-science-pipelines-operatorReady"
        KSERVE_READY = "kserveReady"
        CODEFLARE_READY = "codeflareReady"
        RAY_READY = "rayReady"
        TRUSTYAI_READY = "trustyaiReady"

        class Reason:
            RECONCILE_COMPLETED_WITH_COMPONENT_ERRORS = "ReconcileCompletedWithComponentErrors"
            RECONCILE_FAILED = "ReconcileFailed"
            RECONCILE_COMPLETED = "ReconcileCompleted"


    class ManagementState:
        """
        Supported Management States of components of DataScienceCluster.

        Managed: The Operator actively manages the component, installs it, and tries to keep it active.
        The Operator will upgrade the component only if it is safe to do so.

        Removed: The Operator actively manages the component but does not install it. If the component is
        already installed, the Operator will try to remove it.
        """

        MANAGED = "Managed"
        REMOVED = "Removed"

    def __init__(
        self,
        codeflare_state=None,
        dashboard_state=None,
        data_science_pipelines_state=None,
        kserve_state=None,
        model_mesh_state=None,
        ray_state=None,
        trustyai_state=None,
        workbenches_state=None,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the DataScienceCluster
            client (DynamicClient): DynamicClient to use.
            yaml_file (yaml, default: None): yaml file for the resource.
            codeflare_state (str): ManagementState of codeflare Component.
            dashboard_state (str): ManagementState of dashboard Component.
            data_science_pipelines_state (str): ManagementState of datasciencepipelines Component.
            kserve_state (str): ManagementState of kserve Component.
            model_mesh_state (str): ManagementState of modelmeshserving Component.
            ray_state (str): ManagementState of ray Component.
            trustyai_state (str): ManagementState of trustyai Component.
            workbenches_state (str): ManagementState of workbenches Component.

        """
        super().__init__(
            **kwargs,
        )
        self.codeflare_state = codeflare_state
        self.dashboard_state = dashboard_state
        self.datasciencepipelines_state = data_science_pipelines_state
        self.kserve_state = kserve_state
        self.modelmeshserving_state = model_mesh_state
        self.ray_state = ray_state
        self.trustyai_state = trustyai_state
        self.workbenches_state = workbenches_state

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update({
                "spec": {
                    "components": {
                        "codeflare": {"managementState": self.codeflare_state},
                        "dashboard": {"managementState": self.dashboard_state},
                        "datasciencepipelines": {"managementState": self.datasciencepipelines_state},
                        "kserve": {"managementState": self.kserve_state},
                        "modelmeshserving": {"managementState": self.modelmeshserving_state},
                        "ray": {"managementState": self.ray_state},
                        "trustyai": {"managementState": self.trustyai_state},
                        "workbenches": {"managementState": self.workbenches_state},
                    }
                }
            })
