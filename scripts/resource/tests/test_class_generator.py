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
        pytest.param("Title", "title", id="title-word"),
        pytest.param("tolerations", "tolerations", id="lowercase-word"),
        pytest.param("UPPERCASEWORD", "uppercaseword", id="uppercase-word"),
        pytest.param("ipFamilies", "ip_families", id="combined-basic-with-two-words"),
        pytest.param(
            "allocateLoadBalancerNodePorts",
            "allocate_load_balancer_node_ports",
            id="combined-basic-with-mutliple-words",
        ),
        pytest.param("XMLHttpRequest", "xml_http_request", id="combined-uppercase-word-is-first"),
        pytest.param(
            "additionalCORSAllowedOS", "additional_cors_allowed_os", id="combined-uppercase-word-in-the-middle"
        ),
        pytest.param("hostIPC", "host_ipc", id="combined-uppercase-word-is-last"),
        pytest.param("clusterIPs", "cluster_ips", id="combined-uppercase-word-is-last-ends-with-lowercase"),
    ],
)
def test_convert_camel_case_to_snake_case(request, camel_case_str, expected):
    assert convert_camel_case_to_snake_case(string_=camel_case_str) == expected, f"Failed {request.node.callspec.id}"
