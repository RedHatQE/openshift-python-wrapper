from typing import List
import pytest

from tests.scripts.validate_resources import parse_resource_file_for_errors, resource_file


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
