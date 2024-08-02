# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md#adding-tests

import os
import filecmp

import pytest

from scripts.resource.class_generator import TESTS_MANIFESTS_DIR, class_generator


@pytest.mark.parametrize(
    "kind, debug_file, result_file",
    (
        (
            "api_server",
            os.path.join(TESTS_MANIFESTS_DIR, "api_server", "api_server_debug.json"),
            os.path.join(TESTS_MANIFESTS_DIR, "api_server", "api_server_res.py"),
        ),
        (
            "config_map",
            os.path.join(TESTS_MANIFESTS_DIR, "config_map", "config_map_debug.json"),
            os.path.join(TESTS_MANIFESTS_DIR, "config_map", "config_map_res.py"),
        ),
        (
            "deployment",
            os.path.join(TESTS_MANIFESTS_DIR, "deployment", "deployment_debug.json"),
            os.path.join(TESTS_MANIFESTS_DIR, "deployment", "deployment_res.py"),
        ),
        (
            "pod",
            os.path.join(TESTS_MANIFESTS_DIR, "pod", "pod_debug.json"),
            os.path.join(TESTS_MANIFESTS_DIR, "pod", "pod_res.py"),
        ),
        (
            "secret",
            os.path.join(TESTS_MANIFESTS_DIR, "secret", "secret_debug.json"),
            os.path.join(TESTS_MANIFESTS_DIR, "secret", "secret_res.py"),
        ),
        (
            "cluster_operator",
            os.path.join(TESTS_MANIFESTS_DIR, "cluster_operator", "cluster_operator_debug.json"),
            os.path.join(TESTS_MANIFESTS_DIR, "cluster_operator", "cluster_operator_res.py"),
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
