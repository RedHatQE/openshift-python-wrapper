# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class OpenTelemetryCollector(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.OPENTELEMETRY_IO

    def __init__(
        self,
        additional_containers: list[Any] | None = None,
        affinity: dict[str, Any] | None = None,
        args: dict[str, Any] | None = None,
        autoscaler: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        config_versions: int | None = None,
        configmaps: list[Any] | None = None,
        daemon_set_update_strategy: dict[str, Any] | None = None,
        deployment_update_strategy: dict[str, Any] | None = None,
        env: list[Any] | None = None,
        env_from: list[Any] | None = None,
        host_network: bool | None = None,
        image: str | None = None,
        image_pull_policy: str | None = None,
        ingress: dict[str, Any] | None = None,
        init_containers: list[Any] | None = None,
        ip_families: list[Any] | None = None,
        ip_family_policy: str | None = None,
        lifecycle: dict[str, Any] | None = None,
        liveness_probe: dict[str, Any] | None = None,
        management_state: str | None = None,
        mode: str | None = None,
        node_selector: dict[str, Any] | None = None,
        observability: dict[str, Any] | None = None,
        persistent_volume_claim_retention_policy: dict[str, Any] | None = None,
        pod_annotations: dict[str, Any] | None = None,
        pod_disruption_budget: dict[str, Any] | None = None,
        pod_dns_config: dict[str, Any] | None = None,
        pod_security_context: dict[str, Any] | None = None,
        ports: list[Any] | None = None,
        priority_class_name: str | None = None,
        readiness_probe: dict[str, Any] | None = None,
        replicas: int | None = None,
        resources: dict[str, Any] | None = None,
        security_context: dict[str, Any] | None = None,
        service_account: str | None = None,
        share_process_namespace: bool | None = None,
        target_allocator: dict[str, Any] | None = None,
        termination_grace_period_seconds: int | None = None,
        tolerations: list[Any] | None = None,
        topology_spread_constraints: list[Any] | None = None,
        upgrade_strategy: str | None = None,
        volume_claim_templates: list[Any] | None = None,
        volume_mounts: list[Any] | None = None,
        volumes: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            additional_containers (list[Any]): No field description from API

            affinity (dict[str, Any]): No field description from API

            args (dict[str, Any]): No field description from API

            autoscaler (dict[str, Any]): No field description from API

            config (dict[str, Any]): No field description from API

            config_versions (int): No field description from API

            configmaps (list[Any]): No field description from API

            daemon_set_update_strategy (dict[str, Any]): No field description from API

            deployment_update_strategy (dict[str, Any]): No field description from API

            env (list[Any]): No field description from API

            env_from (list[Any]): No field description from API

            host_network (bool): No field description from API

            image (str): No field description from API

            image_pull_policy (str): No field description from API

            ingress (dict[str, Any]): No field description from API

            init_containers (list[Any]): No field description from API

            ip_families (list[Any]): No field description from API

            ip_family_policy (str): No field description from API

            lifecycle (dict[str, Any]): No field description from API

            liveness_probe (dict[str, Any]): No field description from API

            management_state (str): No field description from API

            mode (str): No field description from API

            node_selector (dict[str, Any]): No field description from API

            observability (dict[str, Any]): No field description from API

            persistent_volume_claim_retention_policy (dict[str, Any]): No field description from API

            pod_annotations (dict[str, Any]): No field description from API

            pod_disruption_budget (dict[str, Any]): No field description from API

            pod_dns_config (dict[str, Any]): No field description from API

            pod_security_context (dict[str, Any]): No field description from API

            ports (list[Any]): No field description from API

            priority_class_name (str): No field description from API

            readiness_probe (dict[str, Any]): No field description from API

            replicas (int): No field description from API

            resources (dict[str, Any]): No field description from API

            security_context (dict[str, Any]): No field description from API

            service_account (str): No field description from API

            share_process_namespace (bool): No field description from API

            target_allocator (dict[str, Any]): No field description from API

            termination_grace_period_seconds (int): No field description from API

            tolerations (list[Any]): No field description from API

            topology_spread_constraints (list[Any]): No field description from API

            upgrade_strategy (str): No field description from API

            volume_claim_templates (list[Any]): No field description from API

            volume_mounts (list[Any]): No field description from API

            volumes (list[Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.additional_containers = additional_containers
        self.affinity = affinity
        self.args = args
        self.autoscaler = autoscaler
        self.config = config
        self.config_versions = config_versions
        self.configmaps = configmaps
        self.daemon_set_update_strategy = daemon_set_update_strategy
        self.deployment_update_strategy = deployment_update_strategy
        self.env = env
        self.env_from = env_from
        self.host_network = host_network
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.ingress = ingress
        self.init_containers = init_containers
        self.ip_families = ip_families
        self.ip_family_policy = ip_family_policy
        self.lifecycle = lifecycle
        self.liveness_probe = liveness_probe
        self.management_state = management_state
        self.mode = mode
        self.node_selector = node_selector
        self.observability = observability
        self.persistent_volume_claim_retention_policy = persistent_volume_claim_retention_policy
        self.pod_annotations = pod_annotations
        self.pod_disruption_budget = pod_disruption_budget
        self.pod_dns_config = pod_dns_config
        self.pod_security_context = pod_security_context
        self.ports = ports
        self.priority_class_name = priority_class_name
        self.readiness_probe = readiness_probe
        self.replicas = replicas
        self.resources = resources
        self.security_context = security_context
        self.service_account = service_account
        self.share_process_namespace = share_process_namespace
        self.target_allocator = target_allocator
        self.termination_grace_period_seconds = termination_grace_period_seconds
        self.tolerations = tolerations
        self.topology_spread_constraints = topology_spread_constraints
        self.upgrade_strategy = upgrade_strategy
        self.volume_claim_templates = volume_claim_templates
        self.volume_mounts = volume_mounts
        self.volumes = volumes

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.config is None:
                raise MissingRequiredArgumentError(argument="self.config")

            if self.management_state is None:
                raise MissingRequiredArgumentError(argument="self.management_state")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["config"] = self.config
            _spec["managementState"] = self.management_state

            if self.additional_containers is not None:
                _spec["additionalContainers"] = self.additional_containers

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.args is not None:
                _spec["args"] = self.args

            if self.autoscaler is not None:
                _spec["autoscaler"] = self.autoscaler

            if self.config_versions is not None:
                _spec["configVersions"] = self.config_versions

            if self.configmaps is not None:
                _spec["configmaps"] = self.configmaps

            if self.daemon_set_update_strategy is not None:
                _spec["daemonSetUpdateStrategy"] = self.daemon_set_update_strategy

            if self.deployment_update_strategy is not None:
                _spec["deploymentUpdateStrategy"] = self.deployment_update_strategy

            if self.env is not None:
                _spec["env"] = self.env

            if self.env_from is not None:
                _spec["envFrom"] = self.env_from

            if self.host_network is not None:
                _spec["hostNetwork"] = self.host_network

            if self.image is not None:
                _spec["image"] = self.image

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.ingress is not None:
                _spec["ingress"] = self.ingress

            if self.init_containers is not None:
                _spec["initContainers"] = self.init_containers

            if self.ip_families is not None:
                _spec["ipFamilies"] = self.ip_families

            if self.ip_family_policy is not None:
                _spec["ipFamilyPolicy"] = self.ip_family_policy

            if self.lifecycle is not None:
                _spec["lifecycle"] = self.lifecycle

            if self.liveness_probe is not None:
                _spec["livenessProbe"] = self.liveness_probe

            if self.mode is not None:
                _spec["mode"] = self.mode

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

            if self.observability is not None:
                _spec["observability"] = self.observability

            if self.persistent_volume_claim_retention_policy is not None:
                _spec["persistentVolumeClaimRetentionPolicy"] = self.persistent_volume_claim_retention_policy

            if self.pod_annotations is not None:
                _spec["podAnnotations"] = self.pod_annotations

            if self.pod_disruption_budget is not None:
                _spec["podDisruptionBudget"] = self.pod_disruption_budget

            if self.pod_dns_config is not None:
                _spec["podDnsConfig"] = self.pod_dns_config

            if self.pod_security_context is not None:
                _spec["podSecurityContext"] = self.pod_security_context

            if self.ports is not None:
                _spec["ports"] = self.ports

            if self.priority_class_name is not None:
                _spec["priorityClassName"] = self.priority_class_name

            if self.readiness_probe is not None:
                _spec["readinessProbe"] = self.readiness_probe

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.resources is not None:
                _spec["resources"] = self.resources

            if self.security_context is not None:
                _spec["securityContext"] = self.security_context

            if self.service_account is not None:
                _spec["serviceAccount"] = self.service_account

            if self.share_process_namespace is not None:
                _spec["shareProcessNamespace"] = self.share_process_namespace

            if self.target_allocator is not None:
                _spec["targetAllocator"] = self.target_allocator

            if self.termination_grace_period_seconds is not None:
                _spec["terminationGracePeriodSeconds"] = self.termination_grace_period_seconds

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

            if self.topology_spread_constraints is not None:
                _spec["topologySpreadConstraints"] = self.topology_spread_constraints

            if self.upgrade_strategy is not None:
                _spec["upgradeStrategy"] = self.upgrade_strategy

            if self.volume_claim_templates is not None:
                _spec["volumeClaimTemplates"] = self.volume_claim_templates

            if self.volume_mounts is not None:
                _spec["volumeMounts"] = self.volume_mounts

            if self.volumes is not None:
                _spec["volumes"] = self.volumes

    # End of generated code
