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
    "camel_case_str, expected",
    [
        pytest.param("Title", "title", id="title_word"),
        pytest.param("tolerations", "tolerations", id="lowercase_word"),
        pytest.param("UPPERCASEWORD", "uppercaseword", id="uppercase_word"),
        pytest.param("ipFamilies", "ip_families", id="combined_basic_with_two_words"),
        pytest.param(
            "allocateLoadBalancerNodePorts",
            "allocate_load_balancer_node_ports",
            id="combined_basic_with_multiple_words",
        ),
        pytest.param("XMLHttpRequest", "xml_http_request", id="combined_uppercase_word_is_first"),
        pytest.param(
            "additionalCORSAllowedOS", "additional_cors_allowed_os", id="combined_uppercase_word_in_the_middle"
        ),
        pytest.param("hostIPC", "host_ipc", id="combined_uppercase_word_is_last"),
        pytest.param("clusterIPs", "cluster_ips", id="combined_uppercase_word_is_last_ends_with_lowercase"),
    ],
)
def test_convert_camel_case_to_snake_case(camel_case_str, expected):
    assert convert_camel_case_to_snake_case(string_=camel_case_str) == expected
