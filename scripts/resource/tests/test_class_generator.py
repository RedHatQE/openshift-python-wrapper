import os
import filecmp

import pytest

from scripts.resource.class_generator import class_generator

MANIFESTS_PATH: str = "scripts/resource/tests/manifests"


@pytest.mark.parametrize(
    "debug_file, result_file",
    (
        (os.path.join(MANIFESTS_PATH, "Deployment-debug.json"), os.path.join(MANIFESTS_PATH, "deployment-res.py")),
        (os.path.join(MANIFESTS_PATH, "Pod-debug.json"), os.path.join(MANIFESTS_PATH, "pod-res.py")),
    ),
)
def test_parse_explain(tmpdir_factory, debug_file, result_file):
    output_dir = tmpdir_factory.mktemp("output-dir")
    output_file = class_generator(process_debug_file=debug_file, generated_file_output_dir=str(output_dir))
    assert filecmp.cmp(output_file, result_file)
