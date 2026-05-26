import pytest
from benedict import benedict

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
    result = benedict(replace_key_with_hashed_value(resource_dict=vm_spec, key_name=key_name), keypath_separator=">")
    assert result[expected_key] == "*******"
    vm_spec_benedict = benedict(vm_spec, keypath_separator=">")
    result_benedict = benedict(result, keypath_separator=">")
    del vm_spec_benedict[expected_key]
    del result_benedict[expected_key]
    assert result_benedict == vm_spec_benedict


@pytest.mark.parametrize(
    "resource, key_name, expected_result",
    [
        # Empty dictionary
        pytest.param({}, "a>b", {}, id="test_replace_key_with_hashed_value_empty_dict"),
        # Non-existent key
        pytest.param(
            {"x": {"y": "z"}}, "a>b", {"x": {"y": "z"}}, id="test_replace_key_with_hashed_value_key_doesnt_exist"
        ),
        # Malformed key
        pytest.param(
            {"x": {"y": "z"}}, "x>y>", {"x": {"y": "z"}}, id="test_replace_key_with_hashed_value_malformed_key"
        ),
        # empty key path
        pytest.param({"x": {"y": "z"}}, "", {"x": {"y": "z"}}, id="test_replace_key_with_hashed_value_empty_key"),
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


@pytest.mark.parametrize(
    "resource, key_name, exception_type",
    [
        pytest.param(None, "a>b", TypeError, id="test_replace_key_with_hashed_value_empty_dict_valid_key"),
        pytest.param({}, None, TypeError, id="test_replace_key_with_hashed_value_empty_dict_no_key"),
        pytest.param({}, 123, TypeError, id="test_replace_key_with_hashed_value_empty_dict_invalid_key"),
        pytest.param("not_a_dict", "a>b", ValueError, id="test_replace_key_with_hashed_value_invalid_dict_valid_key"),
    ],
)
def test_replace_key_with_hashed_value_invalid_inputs(resource, key_name, exception_type):
    """Test that the function handles invalid inputs appropriately."""
    with pytest.raises(exception_type):
        replace_key_with_hashed_value(resource_dict=resource, key_name=key_name)
