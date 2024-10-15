# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class MariadbOperator(NamespacedResource):
    """
    MariadbOperator is the Schema for the mariadboperators API
    """

    api_group: str = NamespacedResource.ApiGroup.HELM_MARIADB_MMONTES_IO

    def __init__(
        self,
        affinity: Optional[Dict[str, Any]] = None,
        cert_controller: Optional[Dict[str, Any]] = None,
        cluster_name: Optional[str] = None,
        extr_args: Optional[List[str]] = None,
        extra_volume_mounts: Optional[List[Dict[str, Any]]] = None,
        extra_volumes: Optional[List[Dict[str, Any]]] = None,
        fullname_override: Optional[str] = None,
        ha: Optional[Dict[str, Any]] = None,
        image: Optional[Dict[str, Any]] = None,
        image_pull_secrets: Optional[List[Dict[str, Any]]] = None,
        log_level: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None,
        name_override: Optional[str] = None,
        node_selector: Optional[Dict[str, str]] = None,
        pod_annotations: Optional[Dict[str, str]] = None,
        pod_security_context: Optional[Dict[str, Any]] = None,
        rbac: Optional[Dict[str, Any]] = None,
        resources: Optional[Dict[str, Any]] = None,
        security_context: Optional[Dict[str, Any]] = None,
        service_account: Optional[Dict[str, Any]] = None,
        tolerations: Optional[List[Dict[str, Any]]] = None,
        webhook: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            affinity (Dict[str, Any]): Node affinity settings for the operator.
            cert_controller (Dict[str, Any]): Configuration for the certificate controller.
            cluster_name (str): Name of the Kubernetes cluster.
            extr_args (List[str]): Additional arguments for the operator.
            extra_volume_mounts (List[Dict[str, Any]]): Additional volume mounts for the operator.
            extra_volumes (List[Dict[str, Any]]): Additional volumes for the operator.
            fullname_override (str): Override for the full name of resources.
            ha (Dict[str, Any]): High availability configuration.
            image (Dict[str, Any]): Container image configuration.
            image_pull_secrets (List[Dict[str, Any]]): Secrets for pulling container images.
            log_level (str): Logging level for the operator.
            metrics (Dict[str, Any]): Metrics collection configuration.
            name_override (str): Override for the name of resources.
            node_selector (Dict[str, str]): Node selection criteria.
            pod_annotations (Dict[str, str]): Annotations for the operator pod.
            pod_security_context (Dict[str, Any]): Security context for the operator pod.
            rbac (Dict[str, Any]): RBAC configuration.
            resources (Dict[str, Any]): Resource requirements for the operator.
            security_context (Dict[str, Any]): Security context for the operator container.
            service_account (Dict[str, Any]): Service account configuration.
            tolerations (List[Dict[str, Any]]): Tolerations for node taints.
            webhook (Dict[str, Any]): Webhook configuration.
        """
        super().__init__(**kwargs)

        self.affinity = affinity
        self.cert_controller = cert_controller
        self.cluster_name = cluster_name
        self.extr_args = extr_args
        self.extra_volume_mounts = extra_volume_mounts
        self.extra_volumes = extra_volumes
        self.fullname_override = fullname_override
        self.ha = ha
        self.image = image
        self.image_pull_secrets = image_pull_secrets
        self.log_level = log_level
        self.metrics = metrics
        self.name_override = name_override
        self.node_selector = node_selector
        self.pod_annotations = pod_annotations
        self.pod_security_context = pod_security_context
        self.rbac = rbac
        self.resources = resources
        self.security_context = security_context
        self.service_account = service_account
        self.tolerations = tolerations
        self.webhook = webhook

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.affinity is not None:
                _spec["affinity"] = self.affinity
            if self.cert_controller is not None:
                _spec["certController"] = self.cert_controller
            if self.cluster_name is not None:
                _spec["clusterName"] = self.cluster_name
            if self.extr_args is not None:
                _spec["extrArgs"] = self.extr_args
            if self.extra_volume_mounts is not None:
                _spec["extraVolumeMounts"] = self.extra_volume_mounts
            if self.extra_volumes is not None:
                _spec["extraVolumes"] = self.extra_volumes
            if self.fullname_override is not None:
                _spec["fullnameOverride"] = self.fullname_override
            if self.ha is not None:
                _spec["ha"] = self.ha
            if self.image is not None:
                _spec["image"] = self.image
            if self.image_pull_secrets is not None:
                _spec["imagePullSecrets"] = self.image_pull_secrets
            if self.log_level is not None:
                _spec["logLevel"] = self.log_level
            if self.metrics is not None:
                _spec["metrics"] = self.metrics
            if self.name_override is not None:
                _spec["nameOverride"] = self.name_override
            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector
            if self.pod_annotations is not None:
                _spec["podAnnotations"] = self.pod_annotations
            if self.pod_security_context is not None:
                _spec["podSecurityContext"] = self.pod_security_context
            if self.rbac is not None:
                _spec["rbac"] = self.rbac
            if self.resources is not None:
                _spec["resources"] = self.resources
            if self.security_context is not None:
                _spec["securityContext"] = self.security_context
            if self.service_account is not None:
                _spec["serviceAccount"] = self.service_account
            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations
            if self.webhook is not None:
                _spec["webhook"] = self.webhook

    # End of generated code
