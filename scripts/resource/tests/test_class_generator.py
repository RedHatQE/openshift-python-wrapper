from scripts.resource.class_generator import parse_explain
from deepdiff import DeepDiff
import pytest
from scripts.resource.tests.manifests.results import DATASCIENCECLUSTER, DEPLOYMENT, POD

MANIFESTS_PATH: str = "scripts/resource/tests/manifests"


# TODO: Fix tests to work without cluster
@pytest.mark.parametrize(
    "explain_file, result_dict",
    (
        ("DataScienceCluster.explain", DATASCIENCECLUSTER),
        ("Deployment.explain", DEPLOYMENT),
        ("Pod.explain", POD),
    ),
)
def test_parse_explain(explain_file, result_dict):
    output: str = ""
    with open(f"{MANIFESTS_PATH}/{explain_file}") as fd:
        output = fd.read()

    res = parse_explain(api_link="https://test.explain", output=output, namespaced=True)
    assert not DeepDiff(res, result_dict)
