from typing import List
import pytest
from benedict import benedict

from tests.scripts.validate_resources import parse_resource_file_for_errors, resource_file
from ocp_resources.resource import replace_key_with_hashed_value


@pytest.fixture()
def vm_spec():
    return {
        "spec": {
            "template": {
                "features": {"someNewFeature": {"someNewData": "sensitive information"}},
                "spec": {
                    "volumes": [
                        {"name": "volume1", "userData": "sensitive-data"},
                    ]
                },
            }
        }
    }


@pytest.fixture()
def resources_definitions_errors() -> List[str]:
    errors = []
    for _file in resource_file():
        with open(_file) as fd:
            data = fd.read()

        errors.extend(parse_resource_file_for_errors(data=data))

    return errors


def test_resources_definitions(resources_definitions_errors):
    assert not resources_definitions_errors, "\n".join(resources_definitions_errors)


@pytest.mark.parametrize(
    "key_name, expected_key",
    [
        pytest.param(
            "spec>template>features>someNewFeature>someNewData",
            "spec>template>features>someNewFeature>someNewData",
            id="test_replace_key_with_hashed_value_replace_key",
        ),
        pytest.param(
            "spec>template>spec>volumes[]>userData",
            "spec>template>spec>volumes[0]>userData",
            id="test_replace_key_with_hashed_value_replace_key_in_list",
        ),
    ],
)
def test_replace_key_with_hashed_value(vm_spec, key_name, expected_key):
    assert (
        benedict(replace_key_with_hashed_value(resource_dict=vm_spec, key_name=key_name), keypath_separator=">")[
            expected_key
        ]
        == "*******"
    )


@pytest.mark.parametrize(
    "resource, key_name, expected_result",
    [
        # Empty dictionary
        pytest.param({}, "a>b", {}, id="test_replace_key_with_hashed_value_empty_dict"),
        # Non-existent key
        pytest.param(
            {"x": {"y": "z"}}, "a>b", {"x": {"y": "z"}}, id="test_replace_key_with_hashed_value_key_doesnt_exist"
        ),
    ],
)
def test_replace_key_with_hashed_value_edge_cases(resource, key_name, expected_result):
    """Test edge cases for replace_key_with_hashed_value function."""
    assert replace_key_with_hashed_value(resource_dict=resource, key_name=key_name) == expected_result


def test_replace_key_with_hashed_value_multiple_occurances(vm_spec):
    vm_spec["spec"]["template"]["spec"]["volumes"].append({"name": "volume2", "userData": "more sensitive-data"})
    result = replace_key_with_hashed_value(resource_dict=vm_spec, key_name="spec>template>spec>volumes[]>userData")
    for volume in result["spec"]["template"]["spec"]["volumes"]:
        assert volume["userData"] == "*******"


def test_replace_key_with_hashed_value_invalid_inputs():
    """Test that the function handles invalid inputs appropriately."""
    with pytest.raises(TypeError):
        replace_key_with_hashed_value(resource_dict=None, key_name="a>b")
