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
