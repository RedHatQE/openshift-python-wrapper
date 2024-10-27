# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md#adding-tests

import os
import filecmp
from pathlib import Path
import pytest

from class_generator.class_generator import TESTS_MANIFESTS_DIR, class_generator


@pytest.mark.parametrize(
    "kind",
    (
        "APIServer",
        "ClusterOperator",
        "ConfigMap",
        "DNS",
        "Deployment",
        "Image",
        "ImageContentSourcePolicy",
        "Machine",
        "NMState",
        "OAuth",
        "Pod",
        "Secret",
        "ServiceMeshMember",
        "ServingRuntime",
        "Pipeline",
    ),
)
def test_parse_explain(tmpdir_factory, kind):
    output_dir = tmpdir_factory.mktemp("output-dir")
    output_files = class_generator(
        kind=kind,
        output_dir=output_dir,
    )
    for output_file in output_files:
        assert filecmp.cmp(output_file, f"{os.path.join(TESTS_MANIFESTS_DIR, kind, Path(output_file).parts[-1])}")
