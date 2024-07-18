from scripts.resource.class_generator import (
    generate_resource_file_from_dict,
    resource_from_explain_file,
)
from deepdiff import DeepDiff
import filecmp

POD_RES = {
    "BASE_CLASS": "Resource",
    "API_LINK": "https://pod.explain",
    "KIND": "Pod",
    "VERSION": "v1",
    "DESCRIPTION": "Pod is a collection of containers that can run on a host. This resource is\n     created by clients and scheduled onto hosts.",
    "SPEC": [
        (
            "active_deadline_seconds",
            "active_deadline_seconds: Optional[int] = None",
            False,
            "int",
        ),
        (
            "affinity",
            "affinity: Optional[Dict[str, Any]] = None",
            False,
            "Dict[Any, Any]",
        ),
        (
            "automount_service_account_token",
            "automount_service_account_token: Optional[bool] = None",
            False,
            "bool",
        ),
        ("containers", "containers: Optional[List[Any]] = None", False, "List[Any]"),
        (
            "dns_config",
            "dns_config: Optional[Dict[str, Any]] = None",
            False,
            "Dict[Any, Any]",
        ),
        ("dns_policy", 'dns_policy: Optional[str] = ""', False, "str"),
        (
            "enable_service_links",
            "enable_service_links: Optional[bool] = None",
            False,
            "bool",
        ),
        (
            "ephemeral_containers",
            "ephemeral_containers: Optional[List[Any]] = None",
            False,
            "List[Any]",
        ),
        (
            "host_aliases",
            "host_aliases: Optional[List[Any]] = None",
            False,
            "List[Any]",
        ),
        ("host_ipc", "host_ipc: Optional[bool] = None", False, "bool"),
        ("host_network", "host_network: Optional[bool] = None", False, "bool"),
        ("host_pid", "host_pid: Optional[bool] = None", False, "bool"),
        ("host_users", "host_users: Optional[bool] = None", False, "bool"),
        ("hostname", 'hostname: Optional[str] = ""', False, "str"),
        (
            "image_pull_secrets",
            "image_pull_secrets: Optional[List[Any]] = None",
            False,
            "List[Any]",
        ),
        (
            "init_containers",
            "init_containers: Optional[List[Any]] = None",
            False,
            "List[Any]",
        ),
        ("node_name", 'node_name: Optional[str] = ""', False, "str"),
        (
            "node_selector",
            "node_selector: Optional[Dict[str, Any]] = None",
            False,
            "Dict[Any, Any]",
        ),
        ("os", "os: Optional[Dict[str, Any]] = None", False, "Dict[Any, Any]"),
        (
            "overhead",
            "overhead: Optional[Dict[str, Any]] = None",
            False,
            "Dict[Any, Any]",
        ),
        ("preemption_policy", 'preemption_policy: Optional[str] = ""', False, "str"),
        ("priority", "priority: Optional[int] = None", False, "int"),
        (
            "priority_class_name",
            'priority_class_name: Optional[str] = ""',
            False,
            "str",
        ),
        (
            "readiness_gates",
            "readiness_gates: Optional[List[Any]] = None",
            False,
            "List[Any]",
        ),
        (
            "resource_claims",
            "resource_claims: Optional[List[Any]] = None",
            False,
            "List[Any]",
        ),
        ("restart_policy", 'restart_policy: Optional[str] = ""', False, "str"),
        ("runtime_class_name", 'runtime_class_name: Optional[str] = ""', False, "str"),
        ("scheduler_name", 'scheduler_name: Optional[str] = ""', False, "str"),
        (
            "scheduling_gates",
            "scheduling_gates: Optional[List[Any]] = None",
            False,
            "List[Any]",
        ),
        (
            "security_context",
            "security_context: Optional[Dict[str, Any]] = None",
            False,
            "Dict[Any, Any]",
        ),
        ("service_account", 'service_account: Optional[str] = ""', False, "str"),
        (
            "service_account_name",
            'service_account_name: Optional[str] = ""',
            False,
            "str",
        ),
        (
            "set_hostname_as_fqdn",
            "set_hostname_as_fqdn: Optional[bool] = None",
            False,
            "bool",
        ),
        (
            "share_process_namespace",
            "share_process_namespace: Optional[bool] = None",
            False,
            "bool",
        ),
        ("subdomain", 'subdomain: Optional[str] = ""', False, "str"),
        (
            "termination_grace_period_seconds",
            "termination_grace_period_seconds: Optional[int] = None",
            False,
            "int",
        ),
        ("tolerations", "tolerations: Optional[List[Any]] = None", False, "List[Any]"),
        (
            "topology_spread_constraints",
            "topology_spread_constraints: Optional[List[Any]] = None",
            False,
            "List[Any]",
        ),
        ("volumes", "volumes: Optional[List[Any]] = None", False, "List[Any]"),
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
        ("min_ready_seconds", "min_ready_seconds: Optional[int] = None", False, "int"),
        ("paused", "paused: Optional[bool] = None", False, "bool"),
        (
            "progress_deadline_seconds",
            "progress_deadline_seconds: Optional[int] = None",
            False,
            "int",
        ),
        ("replicas", "replicas: Optional[int] = None", False, "int"),
        (
            "revision_history_limit",
            "revision_history_limit: Optional[int] = None",
            False,
            "int",
        ),
        ("selector", "selector: Dict[Any, Any]", True, "Dict[Any, Any]"),
        (
            "strategy",
            "strategy: Optional[Dict[str, Any]] = None",
            False,
            "Dict[Any, Any]",
        ),
        ("template", "template: Dict[Any, Any]", True, "Dict[Any, Any]"),
    ],
}


def test_resource_from_explain_file(tmp_path_factory):
    manifests_path = "scripts/resource/tests/manifests"
    pod_dict = resource_from_explain_file(
        file=f"{manifests_path}/pod.explain",
        namespaced=False,
        api_link="https://pod.explain",
    )
    deployment_dict = resource_from_explain_file(
        file=f"{manifests_path}/deployment.explain",
        namespaced=True,
        api_link="https://deployment.explain",
    )

    assert DeepDiff(pod_dict, POD_RES) == {}
    assert DeepDiff(deployment_dict, DEPLOYMENT_RES) == {}

    output_dir = tmp_path_factory.mktemp("class_generator")

    pod_res_file = generate_resource_file_from_dict(resource_dict=pod_dict, output_dir=output_dir)
    deployment_res_file = generate_resource_file_from_dict(resource_dict=deployment_dict, output_dir=output_dir)

    assert filecmp.cmp(pod_res_file, "scripts/resource/tests/manifests/pod_expected_result.py")
    assert filecmp.cmp(
        deployment_res_file,
        "scripts/resource/tests/manifests/deployment_expected_result.py",
    )
