# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md#adding-tests

import os
import filecmp

import pytest

from class_generator.class_generator import TESTS_MANIFESTS_DIR, class_generator


@pytest.mark.parametrize(
    "kind, result_file",
    (
        (
            "ApiServer",
            os.path.join(TESTS_MANIFESTS_DIR, "ApiServer", "api_server_res.py"),
        ),
        (
            "ClusterOperator",
            os.path.join(TESTS_MANIFESTS_DIR, "ClusterOperator", "cluster_operator_res.py"),
        ),
        (
            "ConfigMap",
            os.path.join(TESTS_MANIFESTS_DIR, "ConfigMap", "config_map_res.py"),
        ),
        (
            "Deployment",
            os.path.join(TESTS_MANIFESTS_DIR, "Deployment", "deployment_res.py"),
        ),
        (
            "ImageContentSourcePolicy",
            os.path.join(TESTS_MANIFESTS_DIR, "ImageContentSourcePolicy", "image_content_source_policy_res.py"),
        ),
        (
            "Pod",
            os.path.join(TESTS_MANIFESTS_DIR, "Pod", "pod_res.py"),
        ),
        (
            "Secret",
            os.path.join(TESTS_MANIFESTS_DIR, "Secret", "secret_res.py"),
        ),
    ),
)
def test_parse_explain(tmpdir_factory, kind, result_file):
    output_dir = tmpdir_factory.mktemp("output-dir")
    output_file = class_generator(
        kind=kind,
        output_file=os.path.join(output_dir, f"{kind}.py"),
    )
    assert filecmp.cmp(output_file, result_file)
