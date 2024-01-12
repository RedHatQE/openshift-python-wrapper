from ocp_resources.resource import Resource


class DataScienceCluster(Resource):
    """
    DataScienceCluster Resource for RHOAI operator

    https://access.redhat.com/documentation/en-us/red_hat_openshift_ai_self-managed/2.5/html/installing_and_uninstalling_openshift_ai_self-managed/index
    """

    api_group = Resource.ApiGroup.DATASCIENCE_CLUSTER

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
        name=None,
        client=None,
        yaml_file=None,
        codeflare_state=ManagementState.REMOVED,
        dashboard_state=ManagementState.MANAGED,
        datasciencepipelines_state=ManagementState.REMOVED,
        kserve_state=ManagementState.REMOVED,
        modelmeshserving_state=ManagementState.REMOVED,
        ray_state=ManagementState.REMOVED,
        trustyai_state=ManagementState.REMOVED,
        workbenches_state=ManagementState.REMOVED,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the DataScienceCluster
            client (DynamicClient): DynamicClient to use.
            yaml_file (yaml, default: None): yaml file for the resource.
            codeflare_state (str, default: Removed): State of codeflare Component.
            dashboard_state (str, default: Managed): State of dashboard Component.
            datasciencepipelines_state (str, default: Removed): State of datasciencepipelines Component.
            kserve_state (str, default: Removed): State of kserve Component.
            modelmeshserving_state (str, default: Removed): State of modelmeshserving Component.
            ray_state (str, default: Removed): State of ray Component.
            trustyai_state (str, default: Removed): State of trustyai Component.
            workbenches_state (str, default: Removed): State of workbenches Component.

        """
        super().__init__(
            name=name,
            client=client,
            yaml_file=yaml_file,
            **kwargs,
        )
        self.codeflare_state = codeflare_state
        self.dashboard_state = dashboard_state
        self.datasciencepipelines_state = datasciencepipelines_state
        self.kserve_state = kserve_state
        self.modelmeshserving_state = modelmeshserving_state
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
