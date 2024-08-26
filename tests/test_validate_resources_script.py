import pytest

from tests.scripts.validate_resources import parse_resource_file_for_errors

NO_BASE_CLASS = """
class Secret:
    pass
"""
NO_BASE_CLASS_ERRORS = ["Resource Secret must have Resource or NamespacedResource base class"]

WRONG_BASE_CLASS = """
class Secret(Wrong):
    pass
"""

WRONG_BASE_CLASS_ERRORS = ["Resource Secret must have Resource or NamespacedResource base class, got ['Wrong']"]

MULTI_BASE_CLASS = """
class Secret(Resource, NamespacedResource):
    pass
"""

MULTI_BASE_CLASS_ERRORS = ["Resource Secret must have only one of Resource or NamespacedResource base class"]

MULTI_VALID_BASE_CLASS = """
class Secret(NamespacedResource, Base1):
    pass
"""

MULTI_VALID_BASE_CLASS_ERRORS = ["Resource Secret must have api_group or api_version"]

NO_VERSION_AND_GROUP = """
class Secret(NamespacedResource):
    pass
"""

NO_VERSION_AND_GROUP_ERRORS = ["Resource Secret must have api_group or api_version"]

WRONG_BASE_CLASS = """
class Secret(Resource):
    api_version = "v1"
"""

WRONG_BASE_CLASS_ERRORS = ["Resource Secret base class is `Resource` but should have base class `NamespacedResource`"]

WRONG_API_VERSION = """
class Secret(NamespacedResource):
    api_version = "v2"
"""

WRONG_API_VERSION_ERRORS = ["Resource Secret have api_group v2 but should have api_version = v1"]

API_GROUP_RESOURCE_WITH_API_VERSION = """
class NMState(Resource):
    api_version = "v1"
"""

API_GROUP_RESOURCE_WITH_API_VERSION_ERRORS = ["Resource NMState have api_version v1 but should have api_group"]

WRONG_BASE_CLASS_WITOUT_API_TYPE = """
class Secret(Resource):
    pass
"""

WRONG_BASE_CLASS_WITOUT_API_TYPE_ERRORS = [
    "Resource Secret must have api_group or api_version",
    "Resource Secret base class is `Resource` but should have base class `NamespacedResource`",
]


ALL_WRONG = """
class NMState(NamespacedResource):
    api_version = "v1"
"""

ALL_WRONG_ERRORS = [
    "Resource NMState have api_version v1 but should have api_group",
    "Resource NMState base class is `NamespacedResource` but should have base class `Resource`",
]


@pytest.mark.parametrize(
    "class_data, errors",
    [
        pytest.param(NO_BASE_CLASS, NO_BASE_CLASS_ERRORS, id="class_without_base_class"),
        pytest.param(WRONG_BASE_CLASS, WRONG_BASE_CLASS_ERRORS, id="class_with_wrong_base_class"),
        pytest.param(
            MULTI_BASE_CLASS, MULTI_BASE_CLASS_ERRORS, id="class_with_both_resource_and_namespacedresource_base_class"
        ),
        pytest.param(MULTI_VALID_BASE_CLASS, MULTI_VALID_BASE_CLASS_ERRORS, id="class_with_multiple_base_class"),
        pytest.param(NO_VERSION_AND_GROUP, NO_VERSION_AND_GROUP_ERRORS, id="missing_api_group_and_version"),
        pytest.param(WRONG_BASE_CLASS, WRONG_BASE_CLASS_ERRORS, id="wrong_base_class"),
        pytest.param(WRONG_API_VERSION, WRONG_API_VERSION_ERRORS, id="wrong_api_version"),
        pytest.param(
            API_GROUP_RESOURCE_WITH_API_VERSION,
            API_GROUP_RESOURCE_WITH_API_VERSION_ERRORS,
            id="api_group_resource_with_api_version",
        ),
        pytest.param(
            WRONG_BASE_CLASS_WITOUT_API_TYPE,
            WRONG_BASE_CLASS_WITOUT_API_TYPE_ERRORS,
            id="wrong_base_class_and_api_version",
        ),
        pytest.param(ALL_WRONG, ALL_WRONG_ERRORS, id="wrong_base_class_and_api_version"),
    ],
)
def test_validate_resources_script(class_data, errors):
    err = parse_resource_file_for_errors(data=class_data)
    assert len(err) == len(errors)
    assert any(_err for _err in err if _err in errors)
