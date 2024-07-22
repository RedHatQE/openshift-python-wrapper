import pytest
from scripts.resource.class_generator import (
    generate_resource_file_from_dict,
    parse_explain,
)
from deepdiff import DeepDiff
import filecmp

from scripts.resource.tests.manifests.deployment_explain_parsed import DEPLOYMENT_RES
from scripts.resource.tests.manifests.secret_explain_parsed import SECRET_RES


MANIFESTS_PATH = "scripts/resource/tests/manifests"


@pytest.mark.parametrize(
    "kind, namespaced, expected",
    [
        ("deployment", True, DEPLOYMENT_RES),
        ("secret", True, SECRET_RES),
    ],
)
def test_resource_from_explain_file(tmp_path_factory, kind, namespaced, expected):
    res_dict = parse_explain(
        file=f"{MANIFESTS_PATH}/{kind}.explain",
        namespaced=namespaced,
        api_link="https://example.explain",
    )

    assert DeepDiff(res_dict, expected) == {}

    output_dir = tmp_path_factory.mktemp("class_generator")
    res_file = generate_resource_file_from_dict(resource_dict=res_dict, output_dir=output_dir)

    assert filecmp.cmp(res_file, f"{MANIFESTS_PATH}/{kind}_expected_result.py")
