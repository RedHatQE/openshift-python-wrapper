# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class MLflow(Resource):
    """
    MLflow is the Schema for the mlflows API
    """

    api_group: str = Resource.ApiGroup.MLFLOW_OPENDATAHUB_IO

    def __init__(
        self,
        affinity: dict[str, Any] | None = None,
        artifacts_destination: str | None = None,
        backend_store_uri: str | None = None,
        backend_store_uri_from: dict[str, Any] | None = None,
        ca_bundle_config_map: dict[str, Any] | None = None,
        default_artifact_root: str | None = None,
        env: list[Any] | None = None,
        env_from: list[Any] | None = None,
        extra_allowed_origins: list[Any] | None = None,
        image: dict[str, Any] | None = None,
        network_policy_additional_egress_rules: list[Any] | None = None,
        node_selector: dict[str, Any] | None = None,
        pod_annotations: dict[str, Any] | None = None,
        pod_labels: dict[str, Any] | None = None,
        pod_security_context: dict[str, Any] | None = None,
        registry_store_uri: str | None = None,
        registry_store_uri_from: dict[str, Any] | None = None,
        replicas: int | None = None,
        resources: dict[str, Any] | None = None,
        security_context: dict[str, Any] | None = None,
        serve_artifacts: bool | None = None,
        service_account_name: str | None = None,
        storage: dict[str, Any] | None = None,
        tolerations: list[Any] | None = None,
        workers: int | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            affinity (dict[str, Any]): Affinity specifies the pod's scheduling constraints

            artifacts_destination (str): ArtifactsDestination is the server-side destination for MLflow
              artifacts (models, plots, files). This setting only applies when
              ServeArtifacts is enabled. When ServeArtifacts is disabled, this
              field is ignored and clients access artifact storage directly.
              Supported schemes: file://, s3://, gs://, wasbs://, hdfs://, etc.
              Examples:   - "file:///mlflow/artifacts" (requires Storage to be
              configured)   - "s3://my-bucket/mlflow/artifacts" (no Storage
              needed)   - "gs://my-bucket/mlflow/artifacts" (no Storage needed)
              If not specified when ServeArtifacts is enabled, defaults to
              "file:///mlflow/artifacts"  For cloud storage authentication, use
              EnvFrom to inject credentials from secrets or configmaps. Example
              for S3:   envFrom:   - secretRef:       name: aws-credentials  #
              Contains AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY Example for GCS:
              envFrom:   - secretRef:       name: gcp-credentials  # Contains
              GOOGLE_APPLICATION_CREDENTIALS path

            backend_store_uri (str): BackendStoreURI is the URI for the MLflow backend store (metadata).
              Supported schemes: file://, sqlite://, mysql://, postgresql://,
              etc. Examples:   - "sqlite:////mlflow/mlflow.db" (requires Storage
              to be configured) Note: For URIs containing credentials, prefer
              using BackendStoreURIFrom for security. This must be set
              explicitly unless BackendStoreURIFrom is provided.

            backend_store_uri_from (dict[str, Any]): BackendStoreURIFrom is a reference to a secret containing the backend
              store URI. Use this instead of BackendStoreURI when the URI
              contains credentials. Mutually exclusive with BackendStoreURI -
              the API rejects specs that set both.

            ca_bundle_config_map (dict[str, Any]): CABundleConfigMap specifies a ConfigMap containing a CA certificate
              bundle. The bundle will be mounted into the MLflow container and
              configured for use with TLS connections (e.g. PostgreSQL SSL, S3
              with custom certificates).

            default_artifact_root (str): DefaultArtifactRoot is the default artifact root path for MLflow runs
              on the server. This is required when serveArtifacts is false.
              Supported schemes: file://, s3://, gs://, wasbs://, hdfs://, etc.
              Examples:   - "s3://my-bucket/mlflow/artifacts"   - "gs://my-
              bucket/mlflow/artifacts"   - "file:///mlflow/artifacts"

            env (list[Any]): Env is a list of environment variables to set in the MLflow container

            env_from (list[Any]): EnvFrom is a list of sources to populate environment variables in the
              MLflow container

            extra_allowed_origins (list[Any]): ExtraAllowedOrigins is a list of additional origins to allow for CORS
              requests. The operator preconfigures safe defaults including
              Kubernetes service names, the data science gateway domain, and
              localhost. Use this field to add additional origins beyond the
              defaults. Each entry should be a full origin
              (scheme://host[:port]), e.g. "https://my-app.example.com".

            image (dict[str, Any]): Image specifies the MLflow container image. If not specified, use the
              default image via the MLFLOW_IMAGE environment variable in the
              operator.

            network_policy_additional_egress_rules (list[Any]): NetworkPolicyAdditionalEgressRules specifies additional egress rules
              to append to the default NetworkPolicy. The default policy permits
              DNS (53), HTTPS (443), Kubernetes API (6443), PostgreSQL (5432),
              MySQL (3306), and S3-compatible storage (MinIO 9000, SeaweedFS
              8333). Use this field when connecting to services on non-standard
              ports or when destination restrictions are needed.

            node_selector (dict[str, Any]): NodeSelector is a selector which must be true for the pod to fit on a
              node

            pod_annotations (dict[str, Any]): PodAnnotations are annotations to add only to the MLflow pod, not to
              other resources. Use this for pod-specific annotations like
              Prometheus scraping or sidecar configuration.

            pod_labels (dict[str, Any]): PodLabels are labels to add only to the MLflow pod, not to other
              resources. Use this for pod-specific labels like version,
              component-specific metadata, etc. For labels that should be
              applied to all resources (Service, Deployment, etc.), use
              commonLabels in values.yaml.

            pod_security_context (dict[str, Any]): PodSecurityContext specifies the security context for the MLflow pod

            registry_store_uri (str): RegistryStoreURI is the URI for the MLflow registry store (model
              registry metadata). Supported schemes: file://, sqlite://,
              mysql://, postgresql://, etc. Examples:   -
              "sqlite:////mlflow/mlflow.db" (requires Storage to be configured)
              If omitted, defaults to the same value as backendStoreUri. Note:
              For URIs containing credentials, prefer using RegistryStoreURIFrom
              for security.

            registry_store_uri_from (dict[str, Any]): RegistryStoreURIFrom is a reference to a secret containing the
              registry store URI. Use this instead of RegistryStoreURI when the
              URI contains credentials. Mutually exclusive with RegistryStoreURI
              - the API rejects specs that set both.

            replicas (int): Replicas is the number of MLflow pods to run

            resources (dict[str, Any]): Resources specifies the compute resources for the MLflow container

            security_context (dict[str, Any]): SecurityContext specifies the security context for the MLflow
              container

            serve_artifacts (bool): ServeArtifacts determines whether MLflow should serve artifacts. When
              enabled, adds the --serve-artifacts flag to the MLflow server and
              uses ArtifactsDestination to configure where artifacts are stored.
              This allows clients to log and retrieve artifacts through the
              MLflow server's REST API instead of directly accessing the
              artifact storage. When disabled, ArtifactsDestination is ignored
              and clients must have direct access to artifact storage.

            service_account_name (str): ServiceAccountName is the name of the ServiceAccount to use for the
              MLflow pod. If not specified, a default ServiceAccount will be
              "mlflow-sa"

            storage (dict[str, Any]): Storage specifies the persistent storage configuration using standard
              PVC spec. Only required if using SQLite backend/registry stores or
              file-based artifacts. Not needed when using remote storage (S3,
              PostgreSQL, etc.). When omitted, no PVC will be created - ensure
              backendStoreUri, registryStoreUri, and artifactsDestination point
              to remote storage. Example:   storage:     accessModes:
              ["ReadWriteOnce"]     resources:       requests:         storage:
              10Gi     storageClassName: fast-ssd

            tolerations (list[Any]): Tolerations are the pod's tolerations

            workers (int): Workers is the number of uvicorn worker processes for the MLflow
              server. Note: This is different from pod replicas. Each pod will
              run this many worker processes. Defaults to 1. For high-traffic
              deployments, consider increasing pod replicas instead.

        """
        super().__init__(**kwargs)

        self.affinity = affinity
        self.artifacts_destination = artifacts_destination
        self.backend_store_uri = backend_store_uri
        self.backend_store_uri_from = backend_store_uri_from
        self.ca_bundle_config_map = ca_bundle_config_map
        self.default_artifact_root = default_artifact_root
        self.env = env
        self.env_from = env_from
        self.extra_allowed_origins = extra_allowed_origins
        self.image = image
        self.network_policy_additional_egress_rules = network_policy_additional_egress_rules
        self.node_selector = node_selector
        self.pod_annotations = pod_annotations
        self.pod_labels = pod_labels
        self.pod_security_context = pod_security_context
        self.registry_store_uri = registry_store_uri
        self.registry_store_uri_from = registry_store_uri_from
        self.replicas = replicas
        self.resources = resources
        self.security_context = security_context
        self.serve_artifacts = serve_artifacts
        self.service_account_name = service_account_name
        self.storage = storage
        self.tolerations = tolerations
        self.workers = workers

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.artifacts_destination is not None:
                _spec["artifactsDestination"] = self.artifacts_destination

            if self.backend_store_uri is not None:
                _spec["backendStoreUri"] = self.backend_store_uri

            if self.backend_store_uri_from is not None:
                _spec["backendStoreUriFrom"] = self.backend_store_uri_from

            if self.ca_bundle_config_map is not None:
                _spec["caBundleConfigMap"] = self.ca_bundle_config_map

            if self.default_artifact_root is not None:
                _spec["defaultArtifactRoot"] = self.default_artifact_root

            if self.env is not None:
                _spec["env"] = self.env

            if self.env_from is not None:
                _spec["envFrom"] = self.env_from

            if self.extra_allowed_origins is not None:
                _spec["extraAllowedOrigins"] = self.extra_allowed_origins

            if self.image is not None:
                _spec["image"] = self.image

            if self.network_policy_additional_egress_rules is not None:
                _spec["networkPolicyAdditionalEgressRules"] = self.network_policy_additional_egress_rules

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

            if self.pod_annotations is not None:
                _spec["podAnnotations"] = self.pod_annotations

            if self.pod_labels is not None:
                _spec["podLabels"] = self.pod_labels

            if self.pod_security_context is not None:
                _spec["podSecurityContext"] = self.pod_security_context

            if self.registry_store_uri is not None:
                _spec["registryStoreUri"] = self.registry_store_uri

            if self.registry_store_uri_from is not None:
                _spec["registryStoreUriFrom"] = self.registry_store_uri_from

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.resources is not None:
                _spec["resources"] = self.resources

            if self.security_context is not None:
                _spec["securityContext"] = self.security_context

            if self.serve_artifacts is not None:
                _spec["serveArtifacts"] = self.serve_artifacts

            if self.service_account_name is not None:
                _spec["serviceAccountName"] = self.service_account_name

            if self.storage is not None:
                _spec["storage"] = self.storage

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

            if self.workers is not None:
                _spec["workers"] = self.workers

    # End of generated code
