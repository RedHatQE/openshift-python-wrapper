from scripts.resource.class_generator import resource_from_explain_file
from deepdiff import DeepDiff

POD_RES = {
    "BASE_CLASS": "Resource",
    "API_LINK": "https://pod.explain",
    "KIND": "Pod",
    "VERSION": "v1",
    "DESCRIPTION": "Pod is a collection of containers that can run on a host. This resource is\n     created by clients and scheduled onto hosts.",
    "SPEC": [
        ("active_deadline_seconds", "active_deadline_seconds: Option[int] = None", False),
        ("affinity", "affinity: Option[Dict[str, Any]] = None", False),
        ("automount_service_account_token", "automount_service_account_token: Option[bool] = None", False),
        ("containers", "containers: Option[List[Any]] = None", False),
        ("dns_config", "dns_config: Option[Dict[str, Any]] = None", False),
        ("dns_policy", "dns_policy: Option[str] = ''", False),
        ("enable_service_links", "enable_service_links: Option[bool] = None", False),
        ("ephemeral_containers", "ephemeral_containers: Option[List[Any]] = None", False),
        ("host_aliases", "host_aliases: Option[List[Any]] = None", False),
        ("host_ipc", "host_ipc: Option[bool] = None", False),
        ("host_network", "host_network: Option[bool] = None", False),
        ("host_pid", "host_pid: Option[bool] = None", False),
        ("host_users", "host_users: Option[bool] = None", False),
        ("hostname", "hostname: Option[str] = ''", False),
        ("image_pull_secrets", "image_pull_secrets: Option[List[Any]] = None", False),
        ("init_containers", "init_containers: Option[List[Any]] = None", False),
        ("node_name", "node_name: Option[str] = ''", False),
        ("node_selector", "node_selector: Option[Dict[str, Any]] = None", False),
        ("os", "os: Option[Dict[str, Any]] = None", False),
        ("overhead", "overhead: Option[Dict[str, Any]] = None", False),
        ("preemption_policy", "preemption_policy: Option[str] = ''", False),
        ("priority", "priority: Option[int] = None", False),
        ("priority_class_name", "priority_class_name: Option[str] = ''", False),
        ("readiness_gates", "readiness_gates: Option[List[Any]] = None", False),
        ("resource_claims", "resource_claims: Option[List[Any]] = None", False),
        ("restart_policy", "restart_policy: Option[str] = ''", False),
        ("runtime_class_name", "runtime_class_name: Option[str] = ''", False),
        ("scheduler_name", "scheduler_name: Option[str] = ''", False),
        ("scheduling_gates", "scheduling_gates: Option[List[Any]] = None", False),
        ("security_context", "security_context: Option[Dict[str, Any]] = None", False),
        ("service_account", "service_account: Option[str] = ''", False),
        ("service_account_name", "service_account_name: Option[str] = ''", False),
        ("set_hostname_as_fqdn", "set_hostname_as_fqdn: Option[bool] = None", False),
        ("share_process_namespace", "share_process_namespace: Option[bool] = None", False),
        ("subdomain", "subdomain: Option[str] = ''", False),
        ("termination_grace_period_seconds", "termination_grace_period_seconds: Option[int] = None", False),
        ("tolerations", "tolerations: Option[List[Any]] = None", False),
        ("topology_spread_constraints", "topology_spread_constraints: Option[List[Any]] = None", False),
        ("volumes", "volumes: Option[List[Any]] = None", False),
    ],
}
DEPLOYMENT_RES = {
    "BASE_CLASS": "NamespacedResource",
    "API_LINK": "https://deployment.explain",
    "GROUP": "apps",
    "KIND": "Deployment",
    "VERSION": "v1",
    "DESCRIPTION": "Deployment enables declarative updates for Pods and ReplicaSets.",
    "SPEC": [
        ("selector", "selector: Dict[Any, Any]", True),
        ("template", "template: Dict[Any, Any]", True),
        ("min_ready_seconds", "min_ready_seconds: Option[int] = None", False),
        ("paused", "paused: Option[bool] = None", False),
        ("progress_deadline_seconds", "progress_deadline_seconds: Option[int] = None", False),
        ("replicas", "replicas: Option[int] = None", False),
        ("revision_history_limit", "revision_history_limit: Option[int] = None", False),
        ("strategy", "strategy: Option[Dict[str, Any]] = None", False),
    ],
}


def test_resource_from_explain_file():
    manifests_path = "scripts/resource/tests/manifests"
    pod = resource_from_explain_file(
        file=f"{manifests_path}/pod.explain", namespaced=False, api_link="https://pod.explain"
    )
    deployment = resource_from_explain_file(
        file=f"{manifests_path}/deployment.explain", namespaced=True, api_link="https://deployment.explain"
    )
    assert DeepDiff(pod, POD_RES) == {}
    assert DeepDiff(deployment, DEPLOYMENT_RES) == {}
