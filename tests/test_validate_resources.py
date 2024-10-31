from typing import List
import pytest

from tests.scripts.validate_resources import parse_resource_file_for_errors, resource_file
from ocp_resources.resource import replace_key_with_hashed_value


@pytest.fixture()
def nested_dict():
    return {
        "a": {"b": "c"},
        "d": [
            {"b": {"c": "d"}},
            {
                "e": {"f": "g"},
            },
        ],
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


def test_replace_key_with_hashed_value_replace_key(nested_dict):
    assert replace_key_with_hashed_value(resource_dict=nested_dict, key_name="a>b") == {
        "a": {"b": "*******"},
        "d": [
            {"b": {"c": "d"}},
            {
                "e": {"f": "g"},
            },
        ],
    }


def test_replace_key_with_hashed_value_replace_key_in_list(nested_dict):
    assert replace_key_with_hashed_value(resource_dict=nested_dict, key_name="d[]>b>c") == {
        "a": {"b": "c"},
        "d": [
            {"b": {"c": "*******"}},
            {
                "e": {"f": "g"},
            },
        ],
    }


def test_replace_key_with_hashed_value_edge_cases():
    """Test edge cases for replace_key_with_hashed_value function."""
    # Empty dictionary
    assert replace_key_with_hashed_value(resource_dict={}, key_name="a>b") == {}

    # Non-existent key
    assert replace_key_with_hashed_value(resource_dict={"x": {"y": "z"}}, key_name="a>b") == {"x": {"y": "z"}}

    # Multiple occurrences
    data = {
        "a": [{"b": "sensitive"}, {"b": "also_sensitive"}],
    }
    result = replace_key_with_hashed_value(resource_dict=data, key_name="a[]>b")
    assert result["a"][0]["b"] == "*******"
    assert result["a"][1]["b"] == "*******"


def test_replace_key_with_hashed_value_invalid_inputs():
    """Test that the function handles invalid inputs appropriately."""
    with pytest.raises(TypeError):
        replace_key_with_hashed_value(resource_dict=None, key_name="a>b")
