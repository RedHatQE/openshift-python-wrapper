from scripts.resource.class_generator import (
    generate_resource_file_from_dict,
    parse_explain,
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
        {
            "name-from-explain": "activeDeadlineSeconds",
            "name-for-class-arg": "active_deadline_seconds",
            "type-for-class-arg": "active_deadline_seconds: Optional[int] = None",
            "required": False,
            "type": "int",
        },
        {
            "name-from-explain": "affinity",
            "name-for-class-arg": "affinity",
            "type-for-class-arg": "affinity: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "automountServiceAccountToken",
            "name-for-class-arg": "automount_service_account_token",
            "type-for-class-arg": "automount_service_account_token: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "containers",
            "name-for-class-arg": "containers",
            "type-for-class-arg": "containers: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "dnsConfig",
            "name-for-class-arg": "dns_config",
            "type-for-class-arg": "dns_config: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "dnsPolicy",
            "name-for-class-arg": "dns_policy",
            "type-for-class-arg": 'dns_policy: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "enableServiceLinks",
            "name-for-class-arg": "enable_service_links",
            "type-for-class-arg": "enable_service_links: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "ephemeralContainers",
            "name-for-class-arg": "ephemeral_containers",
            "type-for-class-arg": "ephemeral_containers: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "hostAliases",
            "name-for-class-arg": "host_aliases",
            "type-for-class-arg": "host_aliases: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "hostIPC",
            "name-for-class-arg": "host_ipc",
            "type-for-class-arg": "host_ipc: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "hostNetwork",
            "name-for-class-arg": "host_network",
            "type-for-class-arg": "host_network: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "hostPID",
            "name-for-class-arg": "host_pid",
            "type-for-class-arg": "host_pid: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "hostUsers",
            "name-for-class-arg": "host_users",
            "type-for-class-arg": "host_users: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "hostname",
            "name-for-class-arg": "hostname",
            "type-for-class-arg": 'hostname: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "imagePullSecrets",
            "name-for-class-arg": "image_pull_secrets",
            "type-for-class-arg": "image_pull_secrets: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "initContainers",
            "name-for-class-arg": "init_containers",
            "type-for-class-arg": "init_containers: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "nodeName",
            "name-for-class-arg": "node_name",
            "type-for-class-arg": 'node_name: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "nodeSelector",
            "name-for-class-arg": "node_selector",
            "type-for-class-arg": "node_selector: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "os",
            "name-for-class-arg": "os",
            "type-for-class-arg": "os: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "overhead",
            "name-for-class-arg": "overhead",
            "type-for-class-arg": "overhead: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "preemptionPolicy",
            "name-for-class-arg": "preemption_policy",
            "type-for-class-arg": 'preemption_policy: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "priority",
            "name-for-class-arg": "priority",
            "type-for-class-arg": "priority: Optional[int] = None",
            "required": False,
            "type": "int",
        },
        {
            "name-from-explain": "priorityClassName",
            "name-for-class-arg": "priority_class_name",
            "type-for-class-arg": 'priority_class_name: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "readinessGates",
            "name-for-class-arg": "readiness_gates",
            "type-for-class-arg": "readiness_gates: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "resourceClaims",
            "name-for-class-arg": "resource_claims",
            "type-for-class-arg": "resource_claims: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "restartPolicy",
            "name-for-class-arg": "restart_policy",
            "type-for-class-arg": 'restart_policy: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "runtimeClassName",
            "name-for-class-arg": "runtime_class_name",
            "type-for-class-arg": 'runtime_class_name: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "schedulerName",
            "name-for-class-arg": "scheduler_name",
            "type-for-class-arg": 'scheduler_name: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "schedulingGates",
            "name-for-class-arg": "scheduling_gates",
            "type-for-class-arg": "scheduling_gates: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "securityContext",
            "name-for-class-arg": "security_context",
            "type-for-class-arg": "security_context: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "serviceAccount",
            "name-for-class-arg": "service_account",
            "type-for-class-arg": 'service_account: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "serviceAccountName",
            "name-for-class-arg": "service_account_name",
            "type-for-class-arg": 'service_account_name: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "setHostnameAsFQDN",
            "name-for-class-arg": "set_hostname_as_fqdn",
            "type-for-class-arg": "set_hostname_as_fqdn: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "shareProcessNamespace",
            "name-for-class-arg": "share_process_namespace",
            "type-for-class-arg": "share_process_namespace: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "subdomain",
            "name-for-class-arg": "subdomain",
            "type-for-class-arg": 'subdomain: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
        {
            "name-from-explain": "terminationGracePeriodSeconds",
            "name-for-class-arg": "termination_grace_period_seconds",
            "type-for-class-arg": "termination_grace_period_seconds: Optional[int] = None",
            "required": False,
            "type": "int",
        },
        {
            "name-from-explain": "tolerations",
            "name-for-class-arg": "tolerations",
            "type-for-class-arg": "tolerations: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "topologySpreadConstraints",
            "name-for-class-arg": "topology_spread_constraints",
            "type-for-class-arg": "topology_spread_constraints: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
        {
            "name-from-explain": "volumes",
            "name-for-class-arg": "volumes",
            "type-for-class-arg": "volumes: Optional[List[Any]] = None",
            "required": False,
            "type": "List[Any]",
        },
    ],
    "FIELDS": [],
}


DEPLOYMENT_RES = {
    "BASE_CLASS": "NamespacedResource",
    "API_LINK": "https://deployment.explain",
    "GROUP": "apps",
    "KIND": "Deployment",
    "VERSION": "v1",
    "DESCRIPTION": "Deployment enables declarative updates for Pods and ReplicaSets.",
    "SPEC": [
        {
            "name-from-explain": "minReadySeconds",
            "name-for-class-arg": "min_ready_seconds",
            "type-for-class-arg": "min_ready_seconds: Optional[int] = None",
            "required": False,
            "type": "int",
        },
        {
            "name-from-explain": "paused",
            "name-for-class-arg": "paused",
            "type-for-class-arg": "paused: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "progressDeadlineSeconds",
            "name-for-class-arg": "progress_deadline_seconds",
            "type-for-class-arg": "progress_deadline_seconds: Optional[int] = None",
            "required": False,
            "type": "int",
        },
        {
            "name-from-explain": "replicas",
            "name-for-class-arg": "replicas",
            "type-for-class-arg": "replicas: Optional[int] = None",
            "required": False,
            "type": "int",
        },
        {
            "name-from-explain": "revisionHistoryLimit",
            "name-for-class-arg": "revision_history_limit",
            "type-for-class-arg": "revision_history_limit: Optional[int] = None",
            "required": False,
            "type": "int",
        },
        {
            "name-from-explain": "selector",
            "name-for-class-arg": "selector",
            "type-for-class-arg": "selector: Optional[Dict[str, Any]] = None",
            "required": True,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "strategy",
            "name-for-class-arg": "strategy",
            "type-for-class-arg": "strategy: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "template",
            "name-for-class-arg": "template",
            "type-for-class-arg": "template: Optional[Dict[str, Any]] = None",
            "required": True,
            "type": "Dict[Any, Any]",
        },
    ],
    "FIELDS": [],
}

SECRET_RES = {
    "BASE_CLASS": "NamespacedResource",
    "API_LINK": "https://secret.explain",
    "KIND": "Secret",
    "VERSION": "v1",
    "DESCRIPTION": "Secret holds secret data of a certain type. The total bytes of the values in\n    the Data field must be less than MaxSecretSize bytes.",
    "SPEC": [],
    "FIELDS": [
        {
            "name-from-explain": "data",
            "name-for-class-arg": "data",
            "type-for-class-arg": "data: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "immutable",
            "name-for-class-arg": "immutable",
            "type-for-class-arg": "immutable: Optional[bool] = None",
            "required": False,
            "type": "bool",
        },
        {
            "name-from-explain": "stringData",
            "name-for-class-arg": "string_data",
            "type-for-class-arg": "string_data: Optional[Dict[str, Any]] = None",
            "required": False,
            "type": "Dict[Any, Any]",
        },
        {
            "name-from-explain": "type",
            "name-for-class-arg": "type",
            "type-for-class-arg": 'type: Optional[str] = ""',
            "required": False,
            "type": "str",
        },
    ],
}


def test_resource_from_explain_file(tmp_path_factory):
    manifests_path = "scripts/resource/tests/manifests"
    pod_dict = parse_explain(
        file=f"{manifests_path}/pod.explain",
        namespaced=False,
        api_link="https://pod.explain",
    )
    deployment_dict = parse_explain(
        file=f"{manifests_path}/deployment.explain",
        namespaced=True,
        api_link="https://deployment.explain",
    )
    secret_dict = parse_explain(
        file=f"{manifests_path}/secret.explain",
        namespaced=True,
        api_link="https://secret.explain",
    )

    assert DeepDiff(pod_dict, POD_RES) == {}
    assert DeepDiff(deployment_dict, DEPLOYMENT_RES) == {}
    assert DeepDiff(secret_dict, SECRET_RES) == {}

    output_dir = tmp_path_factory.mktemp("class_generator")

    pod_res_file = generate_resource_file_from_dict(resource_dict=pod_dict, output_dir=output_dir)
    deployment_res_file = generate_resource_file_from_dict(resource_dict=deployment_dict, output_dir=output_dir)
    secret_res_file = generate_resource_file_from_dict(resource_dict=secret_dict, output_dir=output_dir)

    assert filecmp.cmp(pod_res_file, f"{manifests_path}/pod_expected_result.py")
    assert filecmp.cmp(
        deployment_res_file,
        f"{manifests_path}/deployment_expected_result.py",
    )
    assert filecmp.cmp(
        secret_res_file,
        f"{manifests_path}/secret_expected_result.py",
    )
