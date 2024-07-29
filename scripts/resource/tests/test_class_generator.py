import os
import filecmp

import pytest

from scripts.resource.class_generator import (
    class_generator,
    convert_camel_case_to_snake_case,
)

MANIFESTS_PATH: str = "scripts/resource/tests/manifests"


@pytest.mark.parametrize(
    "kind, debug_file, result_file",
    (
        (
            "Deployment",
            os.path.join(MANIFESTS_PATH, "deployment_debug.json"),
            os.path.join(MANIFESTS_PATH, "deployment_res.py"),
        ),
        (
            "Pod",
            os.path.join(MANIFESTS_PATH, "pod_debug.json"),
            os.path.join(MANIFESTS_PATH, "pod_res.py"),
        ),
        (
            "ConfigMap",
            os.path.join(MANIFESTS_PATH, "config_map_debug.json"),
            os.path.join(MANIFESTS_PATH, "config_map_res.py"),
        ),
        (
            "APIServer",
            os.path.join(MANIFESTS_PATH, "api_server_debug.json"),
            os.path.join(MANIFESTS_PATH, "api_server_res.py"),
        ),
    ),
)
def test_parse_explain(tmpdir_factory, kind, debug_file, result_file):
    output_dir = tmpdir_factory.mktemp("output-dir")
    output_file = class_generator(
        process_debug_file=debug_file,
        output_file=os.path.join(output_dir, f"{kind}.py"),
    )
    assert filecmp.cmp(output_file, result_file)


@pytest.mark.parametrize(
    "description, camel_case_str, expected",
    (
        ("Title word", "Title", "title"),
        ("Lower case word", "tolerations", "tolerations"),
        ("Upper case word", "UPPERCASEWORD", "uppercaseword"),
        ("Combined - basic with 2 words", "ipFamilies", "ip_families"),
        ("Combined - basic with mutliple words", "allocateLoadBalancerNodePorts", "allocate_load_balancer_node_ports"),
        ("Combined - upper case word is first", "XMLHttpRequest", "xml_http_request"),
        ("Combined - upper case word is in the middle", "additionalCORSAllowedOS", "additional_cors_allowed_os"),
        ("Combined - upper case word is last", "hostIPC", "host_ipc"),
        ("Combined - upper case word is last, ends with lowercase", "clusterIPs", "cluster_ips"),
    ),
)
def test_convert_camel_case_to_snake_case(description, camel_case_str, expected):
    assert convert_camel_case_to_snake_case(string_=camel_case_str) == expected, f"Failed {description}"
