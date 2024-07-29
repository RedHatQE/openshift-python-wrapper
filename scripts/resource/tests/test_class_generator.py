import os
import filecmp

import pytest

from scripts.resource.class_generator import class_generator

MANIFESTS_PATH: str = "scripts/resource/tests/manifests"


@pytest.mark.parametrize(
    "kind, debug_file, result_file",
    (
        (
            "Deployment",
            os.path.join(MANIFESTS_PATH, "deployment_debug.json"),
            os.path.join(MANIFESTS_PATH, "deployment_res.py"),
        ),
        ("Pod", os.path.join(MANIFESTS_PATH, "pod_debug.json"), os.path.join(MANIFESTS_PATH, "pod_res.py")),
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
    output_file = class_generator(process_debug_file=debug_file, output_file=os.path.join(output_dir, f"{kind}.py"))
    assert filecmp.cmp(output_file, result_file)
