# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class DataSciencePipelinesApplication(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.DATASCIENCEPIPELINESAPPLICATIONS_OPENDATAHUB_IO

    def __init__(
        self,
        api_server: dict[str, Any] | None = None,
        database: dict[str, Any] | None = None,
        dsp_version: str | None = None,
        mlmd: dict[str, Any] | None = None,
        mlpipeline_ui: dict[str, Any] | None = None,
        object_storage: dict[str, Any] | None = None,
        persistence_agent: dict[str, Any] | None = None,
        pod_to_pod_tls: bool | None = None,
        scheduled_workflow: dict[str, Any] | None = None,
        workflow_controller: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            api_server (dict[str, Any]): DS Pipelines API Server configuration.

            database (dict[str, Any]): Database specifies database configurations, used for DS Pipelines
              metadata tracking. Specify either the default MariaDB deployment,
              or configure your own External SQL DB.

            dsp_version (str): No field description from API

            mlmd (dict[str, Any]): No field description from API

            mlpipeline_ui (dict[str, Any]): Deploy the KFP UI with DS Pipelines UI. This feature is unsupported,
              and primarily used for exploration, testing, and development
              purposes.

            object_storage (dict[str, Any]): ObjectStorage specifies Object Store configurations, used for DS
              Pipelines artifact passing and storage. Specify either the your
              own External Storage (e.g. AWS S3), or use the default Minio
              deployment (unsupported, primarily for development, and testing) .

            persistence_agent (dict[str, Any]): DS Pipelines PersistenceAgent configuration.

            pod_to_pod_tls (bool): PodToPodTLS Set to "true" or "false" to enable or disable TLS
              communication between DSPA components (pods). Defaults to "true"
              to enable TLS between all pods. Only supported in DSP V2 on
              OpenShift.

            scheduled_workflow (dict[str, Any]): DS Pipelines Scheduled Workflow configuration.

            workflow_controller (dict[str, Any]): WorkflowController is an argo-specific component that manages a DSPA's
              Workflow objects and handles the orchestration of them with the
              central Argo server

        """
        super().__init__(**kwargs)

        self.api_server = api_server
        self.database = database
        self.dsp_version = dsp_version
        self.mlmd = mlmd
        self.mlpipeline_ui = mlpipeline_ui
        self.object_storage = object_storage
        self.persistence_agent = persistence_agent
        self.pod_to_pod_tls = pod_to_pod_tls
        self.scheduled_workflow = scheduled_workflow
        self.workflow_controller = workflow_controller

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.object_storage is None:
                raise MissingRequiredArgumentError(argument="self.object_storage")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["objectStorage"] = self.object_storage

            if self.api_server is not None:
                _spec["apiServer"] = self.api_server

            if self.database is not None:
                _spec["database"] = self.database

            if self.dsp_version is not None:
                _spec["dspVersion"] = self.dsp_version

            if self.mlmd is not None:
                _spec["mlmd"] = self.mlmd

            if self.mlpipeline_ui is not None:
                _spec["mlpipelineUI"] = self.mlpipeline_ui

            if self.persistence_agent is not None:
                _spec["persistenceAgent"] = self.persistence_agent

            if self.pod_to_pod_tls is not None:
                _spec["podToPodTLS"] = self.pod_to_pod_tls

            if self.scheduled_workflow is not None:
                _spec["scheduledWorkflow"] = self.scheduled_workflow

            if self.workflow_controller is not None:
                _spec["workflowController"] = self.workflow_controller

    # End of generated code
