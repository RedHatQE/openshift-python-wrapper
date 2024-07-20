# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import Resource


class Pod(Resource):
    """
    Pod is a collection of containers that can run on a host. This resource is
     created by clients and scheduled onto hosts.

    API Link: https://pod.explain
    """

    api_version: str = "v1"

    def __init__(
        self,
        active_deadline_seconds: Optional[int] = None,
        affinity: Optional[Dict[str, Any]] = None,
        automount_service_account_token: Optional[bool] = None,
        containers: Optional[List[Any]] = None,
        dns_config: Optional[Dict[str, Any]] = None,
        dns_policy: Optional[str] = "",
        enable_service_links: Optional[bool] = None,
        ephemeral_containers: Optional[List[Any]] = None,
        host_aliases: Optional[List[Any]] = None,
        host_ipc: Optional[bool] = None,
        host_network: Optional[bool] = None,
        host_pid: Optional[bool] = None,
        host_users: Optional[bool] = None,
        hostname: Optional[str] = "",
        image_pull_secrets: Optional[List[Any]] = None,
        init_containers: Optional[List[Any]] = None,
        node_name: Optional[str] = "",
        node_selector: Optional[Dict[str, Any]] = None,
        os: Optional[Dict[str, Any]] = None,
        overhead: Optional[Dict[str, Any]] = None,
        preemption_policy: Optional[str] = "",
        priority: Optional[int] = None,
        priority_class_name: Optional[str] = "",
        readiness_gates: Optional[List[Any]] = None,
        resource_claims: Optional[List[Any]] = None,
        restart_policy: Optional[str] = "",
        runtime_class_name: Optional[str] = "",
        scheduler_name: Optional[str] = "",
        scheduling_gates: Optional[List[Any]] = None,
        security_context: Optional[Dict[str, Any]] = None,
        service_account: Optional[str] = "",
        service_account_name: Optional[str] = "",
        set_hostname_as_fqdn: Optional[bool] = None,
        share_process_namespace: Optional[bool] = None,
        subdomain: Optional[str] = "",
        termination_grace_period_seconds: Optional[int] = None,
        tolerations: Optional[List[Any]] = None,
        topology_spread_constraints: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            active_deadline_seconds (int): <please add description>
            affinity (Dict[Any, Any]): <please add description>
            automount_service_account_token (bool): <please add description>
            containers (List[Any]): <please add description>
            dns_config (Dict[Any, Any]): <please add description>
            dns_policy (str): <please add description>
            enable_service_links (bool): <please add description>
            ephemeral_containers (List[Any]): <please add description>
            host_aliases (List[Any]): <please add description>
            host_ipc (bool): <please add description>
            host_network (bool): <please add description>
            host_pid (bool): <please add description>
            host_users (bool): <please add description>
            hostname (str): <please add description>
            image_pull_secrets (List[Any]): <please add description>
            init_containers (List[Any]): <please add description>
            node_name (str): <please add description>
            node_selector (Dict[Any, Any]): <please add description>
            os (Dict[Any, Any]): <please add description>
            overhead (Dict[Any, Any]): <please add description>
            preemption_policy (str): <please add description>
            priority (int): <please add description>
            priority_class_name (str): <please add description>
            readiness_gates (List[Any]): <please add description>
            resource_claims (List[Any]): <please add description>
            restart_policy (str): <please add description>
            runtime_class_name (str): <please add description>
            scheduler_name (str): <please add description>
            scheduling_gates (List[Any]): <please add description>
            security_context (Dict[Any, Any]): <please add description>
            service_account (str): <please add description>
            service_account_name (str): <please add description>
            set_hostname_as_fqdn (bool): <please add description>
            share_process_namespace (bool): <please add description>
            subdomain (str): <please add description>
            termination_grace_period_seconds (int): <please add description>
            tolerations (List[Any]): <please add description>
            topology_spread_constraints (List[Any]): <please add description>
            volumes (List[Any]): <please add description>
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

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.active_deadline_seconds:
                _spec["active_deadline_seconds"] = self.active_deadline_seconds
            if self.affinity:
                _spec["affinity"] = self.affinity
            if self.automount_service_account_token is not None:
                _spec["automount_service_account_token"] = self.automount_service_account_token
            if self.containers:
                _spec["containers"] = self.containers
            if self.dns_config:
                _spec["dns_config"] = self.dns_config
            if self.dns_policy:
                _spec["dns_policy"] = self.dns_policy
            if self.enable_service_links is not None:
                _spec["enable_service_links"] = self.enable_service_links
            if self.ephemeral_containers:
                _spec["ephemeral_containers"] = self.ephemeral_containers
            if self.host_aliases:
                _spec["host_aliases"] = self.host_aliases
            if self.host_ipc is not None:
                _spec["host_ipc"] = self.host_ipc
            if self.host_network is not None:
                _spec["host_network"] = self.host_network
            if self.host_pid is not None:
                _spec["host_pid"] = self.host_pid
            if self.host_users is not None:
                _spec["host_users"] = self.host_users
            if self.hostname:
                _spec["hostname"] = self.hostname
            if self.image_pull_secrets:
                _spec["image_pull_secrets"] = self.image_pull_secrets
            if self.init_containers:
                _spec["init_containers"] = self.init_containers
            if self.node_name:
                _spec["node_name"] = self.node_name
            if self.node_selector:
                _spec["node_selector"] = self.node_selector
            if self.os:
                _spec["os"] = self.os
            if self.overhead:
                _spec["overhead"] = self.overhead
            if self.preemption_policy:
                _spec["preemption_policy"] = self.preemption_policy
            if self.priority:
                _spec["priority"] = self.priority
            if self.priority_class_name:
                _spec["priority_class_name"] = self.priority_class_name
            if self.readiness_gates:
                _spec["readiness_gates"] = self.readiness_gates
            if self.resource_claims:
                _spec["resource_claims"] = self.resource_claims
            if self.restart_policy:
                _spec["restart_policy"] = self.restart_policy
            if self.runtime_class_name:
                _spec["runtime_class_name"] = self.runtime_class_name
            if self.scheduler_name:
                _spec["scheduler_name"] = self.scheduler_name
            if self.scheduling_gates:
                _spec["scheduling_gates"] = self.scheduling_gates
            if self.security_context:
                _spec["security_context"] = self.security_context
            if self.service_account:
                _spec["service_account"] = self.service_account
            if self.service_account_name:
                _spec["service_account_name"] = self.service_account_name
            if self.set_hostname_as_fqdn is not None:
                _spec["set_hostname_as_fqdn"] = self.set_hostname_as_fqdn
            if self.share_process_namespace is not None:
                _spec["share_process_namespace"] = self.share_process_namespace
            if self.subdomain:
                _spec["subdomain"] = self.subdomain
            if self.termination_grace_period_seconds:
                _spec["termination_grace_period_seconds"] = self.termination_grace_period_seconds
            if self.tolerations:
                _spec["tolerations"] = self.tolerations
            if self.topology_spread_constraints:
                _spec["topology_spread_constraints"] = self.topology_spread_constraints
            if self.volumes:
                _spec["volumes"] = self.volumes
