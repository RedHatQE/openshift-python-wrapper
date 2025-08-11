# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any
from ocp_resources.resource import NamespacedResource


class Pod(NamespacedResource):
    """
    Pod is a collection of containers that can run on a host. This resource is created by clients and scheduled onto hosts.
    """

    api_version: str = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        active_deadline_seconds: int | None = None,
        affinity: dict[str, Any] | None = None,
        automount_service_account_token: bool | None = None,
        containers: list[Any] | None = None,
        dns_config: dict[str, Any] | None = None,
        dns_policy: str | None = None,
        enable_service_links: bool | None = None,
        ephemeral_containers: list[Any] | None = None,
        host_aliases: list[Any] | None = None,
        host_ipc: bool | None = None,
        host_network: bool | None = None,
        host_pid: bool | None = None,
        host_users: bool | None = None,
        hostname: str | None = None,
        image_pull_secrets: list[Any] | None = None,
        init_containers: list[Any] | None = None,
        node_name: str | None = None,
        node_selector: dict[str, Any] | None = None,
        os: dict[str, Any] | None = None,
        overhead: dict[str, Any] | None = None,
        preemption_policy: str | None = None,
        priority: int | None = None,
        priority_class_name: str | None = None,
        readiness_gates: list[Any] | None = None,
        resource_claims: list[Any] | None = None,
        resources: dict[str, Any] | None = None,
        restart_policy: str | None = None,
        runtime_class_name: str | None = None,
        scheduler_name: str | None = None,
        scheduling_gates: list[Any] | None = None,
        security_context: dict[str, Any] | None = None,
        service_account: str | None = None,
        service_account_name: str | None = None,
        set_hostname_as_fqdn: bool | None = None,
        share_process_namespace: bool | None = None,
        subdomain: str | None = None,
        termination_grace_period_seconds: int | None = None,
        tolerations: list[Any] | None = None,
        topology_spread_constraints: list[Any] | None = None,
        volumes: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            active_deadline_seconds (int): No field description from API

            affinity (dict[str, Any]): No field description from API

            automount_service_account_token (bool): No field description from API

            containers (list[Any]): No field description from API

            dns_config (dict[str, Any]): No field description from API

            dns_policy (str): No field description from API

            enable_service_links (bool): No field description from API

            ephemeral_containers (list[Any]): No field description from API

            host_aliases (list[Any]): No field description from API

            host_ipc (bool): No field description from API

            host_network (bool): No field description from API

            host_pid (bool): No field description from API

            host_users (bool): No field description from API

            hostname (str): No field description from API

            image_pull_secrets (list[Any]): No field description from API

            init_containers (list[Any]): No field description from API

            node_name (str): No field description from API

            node_selector (dict[str, Any]): No field description from API

            os (dict[str, Any]): No field description from API

            overhead (dict[str, Any]): No field description from API

            preemption_policy (str): No field description from API

            priority (int): No field description from API

            priority_class_name (str): No field description from API

            readiness_gates (list[Any]): No field description from API

            resource_claims (list[Any]): No field description from API

            resources (dict[str, Any]): No field description from API

            restart_policy (str): No field description from API

            runtime_class_name (str): No field description from API

            scheduler_name (str): No field description from API

            scheduling_gates (list[Any]): No field description from API

            security_context (dict[str, Any]): No field description from API

            service_account (str): No field description from API

            service_account_name (str): No field description from API

            set_hostname_as_fqdn (bool): No field description from API

            share_process_namespace (bool): No field description from API

            subdomain (str): No field description from API

            termination_grace_period_seconds (int): No field description from API

            tolerations (list[Any]): No field description from API

            topology_spread_constraints (list[Any]): No field description from API

            volumes (list[Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.active_deadline_seconds = active_deadline_seconds
        self.affinity = affinity
        self.automount_service_account_token = automount_service_account_token
        self.containers = containers
        self.dns_config = dns_config
        self.dns_policy = dns_policy
        self.enable_service_links = enable_service_links
        self.ephemeral_containers = ephemeral_containers
        self.host_aliases = host_aliases
        self.host_ipc = host_ipc
        self.host_network = host_network
        self.host_pid = host_pid
        self.host_users = host_users
        self.hostname = hostname
        self.image_pull_secrets = image_pull_secrets
        self.init_containers = init_containers
        self.node_name = node_name
        self.node_selector = node_selector
        self.os = os
        self.overhead = overhead
        self.preemption_policy = preemption_policy
        self.priority = priority
        self.priority_class_name = priority_class_name
        self.readiness_gates = readiness_gates
        self.resource_claims = resource_claims
        self.resources = resources
        self.restart_policy = restart_policy
        self.runtime_class_name = runtime_class_name
        self.scheduler_name = scheduler_name
        self.scheduling_gates = scheduling_gates
        self.security_context = security_context
        self.service_account = service_account
        self.service_account_name = service_account_name
        self.set_hostname_as_fqdn = set_hostname_as_fqdn
        self.share_process_namespace = share_process_namespace
        self.subdomain = subdomain
        self.termination_grace_period_seconds = termination_grace_period_seconds
        self.tolerations = tolerations
        self.topology_spread_constraints = topology_spread_constraints
        self.volumes = volumes

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.active_deadline_seconds is not None:
                _spec["activeDeadlineSeconds"] = self.active_deadline_seconds

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.automount_service_account_token is not None:
                _spec["automountServiceAccountToken"] = self.automount_service_account_token

            if self.containers is not None:
                _spec["containers"] = self.containers

            if self.dns_config is not None:
                _spec["dnsConfig"] = self.dns_config

            if self.dns_policy is not None:
                _spec["dnsPolicy"] = self.dns_policy

            if self.enable_service_links is not None:
                _spec["enableServiceLinks"] = self.enable_service_links

            if self.ephemeral_containers is not None:
                _spec["ephemeralContainers"] = self.ephemeral_containers

            if self.host_aliases is not None:
                _spec["hostAliases"] = self.host_aliases

            if self.host_ipc is not None:
                _spec["hostIPC"] = self.host_ipc

            if self.host_network is not None:
                _spec["hostNetwork"] = self.host_network

            if self.host_pid is not None:
                _spec["hostPID"] = self.host_pid

            if self.host_users is not None:
                _spec["hostUsers"] = self.host_users

            if self.hostname is not None:
                _spec["hostname"] = self.hostname

            if self.image_pull_secrets is not None:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.init_containers is not None:
                _spec["initContainers"] = self.init_containers

            if self.node_name is not None:
                _spec["nodeName"] = self.node_name

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

            if self.os is not None:
                _spec["os"] = self.os

            if self.overhead is not None:
                _spec["overhead"] = self.overhead

            if self.preemption_policy is not None:
                _spec["preemptionPolicy"] = self.preemption_policy

            if self.priority is not None:
                _spec["priority"] = self.priority

            if self.priority_class_name is not None:
                _spec["priorityClassName"] = self.priority_class_name

            if self.readiness_gates is not None:
                _spec["readinessGates"] = self.readiness_gates

            if self.resource_claims is not None:
                _spec["resourceClaims"] = self.resource_claims

            if self.resources is not None:
                _spec["resources"] = self.resources

            if self.restart_policy is not None:
                _spec["restartPolicy"] = self.restart_policy

            if self.runtime_class_name is not None:
                _spec["runtimeClassName"] = self.runtime_class_name

            if self.scheduler_name is not None:
                _spec["schedulerName"] = self.scheduler_name

            if self.scheduling_gates is not None:
                _spec["schedulingGates"] = self.scheduling_gates

            if self.security_context is not None:
                _spec["securityContext"] = self.security_context

            if self.service_account is not None:
                _spec["serviceAccount"] = self.service_account

            if self.service_account_name is not None:
                _spec["serviceAccountName"] = self.service_account_name

            if self.set_hostname_as_fqdn is not None:
                _spec["setHostnameAsFQDN"] = self.set_hostname_as_fqdn

            if self.share_process_namespace is not None:
                _spec["shareProcessNamespace"] = self.share_process_namespace

            if self.subdomain is not None:
                _spec["subdomain"] = self.subdomain

            if self.termination_grace_period_seconds is not None:
                _spec["terminationGracePeriodSeconds"] = self.termination_grace_period_seconds

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

            if self.topology_spread_constraints is not None:
                _spec["topologySpreadConstraints"] = self.topology_spread_constraints

            if self.volumes is not None:
                _spec["volumes"] = self.volumes

    # End of generated code
