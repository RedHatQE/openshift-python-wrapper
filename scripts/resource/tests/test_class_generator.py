# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md#adding-tests

import os
import filecmp

import pytest

from scripts.resource.class_generator import class_generator

MANIFESTS_PATH: str = "scripts/resource/tests/manifests"


@pytest.mark.parametrize(
    "kind, debug_file, result_file",
    (
        (
            "secret",
            os.path.join(MANIFESTS_PATH, "secret", "secret_debug.json"),
            os.path.join(MANIFESTS_PATH, "secret", "secret_res.py"),
        ),
        (
            "api_server",
            os.path.join(MANIFESTS_PATH, "api_server", "api_server_debug.json"),
            os.path.join(MANIFESTS_PATH, "api_server", "api_server_res.py"),
        ),
        (
            "config_map",
            os.path.join(MANIFESTS_PATH, "config_map", "config_map_debug.json"),
            os.path.join(MANIFESTS_PATH, "config_map", "config_map_res.py"),
        ),
        (
            "deployment",
            os.path.join(MANIFESTS_PATH, "deployment", "deployment_debug.json"),
            os.path.join(MANIFESTS_PATH, "deployment", "deployment_res.py"),
        ),
        (
            "pod",
            os.path.join(MANIFESTS_PATH, "pod", "pod_debug.json"),
            os.path.join(MANIFESTS_PATH, "pod", "pod_res.py"),
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
