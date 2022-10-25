# This test uses https://github.com/RedHatQE/openshift-resources-definitions to get resource definitions json file
# File: resources_definitions.json

import ast
import json
import os

import pytest
import requests

from ocp_resources.resource import Resource  # noqa


def _api_group_name(api_value):
    try:
        return eval(f"Resource.ApiGroup.{api_value}")
    except AttributeError:
        return api_value


def _api_group_dict(resource_dict, api_group_name):
    resource_dict_api_group = resource_dict["api_group"]
    api_group = resource_dict_api_group.get(api_group_name)
    if not api_group:
        try:
            api_group = resource_dict_api_group["null"]
        except KeyError:
            api_group = resource_dict_api_group[[*resource_dict_api_group][0]]

    return api_group


def _process_api_type(api_type, api_value, resource_dict, cls):
    if api_type == "api_group":
        return _get_api_group(
            api_value=api_value,
            cls=cls,
            resource_dict=resource_dict,
        )

    if api_type == "api_version":
        return _get_api_version(
            api_value=api_value,
            cls=cls,
            resource_dict=resource_dict,
        )

    return [f"Resource {cls.name} must have api_group or api_version"]


def _get_api_group_and_version(bodies):
    for targets in bodies:
        api_type = targets.targets[0].id
        return api_type, targets.value.attr


def _get_namespaced(cls, resource_dict, api_value):
    errors = []
    for base in getattr(cls, "bases", []):
        api_group_name = _api_group_name(api_value=api_value)
        namespaced = base.id == "NamespacedResource"
        api_group = _api_group_dict(
            resource_dict=resource_dict, api_group_name=api_group_name
        )
        should_be_namespaced = api_group["namespaced"] == "true"

        if namespaced != should_be_namespaced:
            errors.append(
                f"Resource {cls.name} should be "
                f"{'namespaced' if should_be_namespaced else 'in cluster scope (not namespaced)'}"
            )
    return errors


def _get_api_group(api_value, cls, resource_dict):
    errors = []
    api_group_name = _api_group_name(api_value=api_value)

    if api_group_name not in resource_dict["api_group"]:
        errors.append(
            f"Resource {cls.name} api_group should be "
            f"{resource_dict['api_group']}. got {api_group_name}"
        )
    return errors


def _get_api_version(api_value, cls, resource_dict):
    errors = []
    api_group_name = _api_group_name(api_value=api_value)
    api_group = _api_group_dict(
        resource_dict=resource_dict, api_group_name=api_group_name
    )
    if api_value.lower() != api_group["api_version"]:
        desire_api_group = resource_dict["api_version"].split("/")[0]
        errors.append(
            f"Resource {cls.name} have api_version {api_value} "
            f"but should have api_group = {desire_api_group}"
        )

    return errors


def _resource_file():
    ocp_resources_exclude_files = ["resource.py", "utils.py", "__init__.py"]
    for root, dirs, files in os.walk("ocp_resources"):
        for _file in files:
            if _file in ocp_resources_exclude_files or not _file.endswith(".py"):
                continue
            yield os.path.join(root, _file)


@pytest.fixture()
def resources_definitions():
    file_ = (
        "https://raw.githubusercontent.com/RedHatQE/"
        "openshift-resources-definitions/main/resources_definitions.json"
    )
    content = requests.get(file_).content
    return json.loads(content)


@pytest.fixture()
def resources_definitions_errors(resources_definitions):
    errors = []
    for _file in _resource_file():
        with open(_file, "r") as fd:
            tree = ast.parse(source=fd.read())
            classes = [cls for cls in tree.body if isinstance(cls, ast.ClassDef)]
            for cls in classes:
                resource_dict = resources_definitions.get(cls.name)
                if not resource_dict:
                    continue

                bodies = [
                    body_
                    for body_ in getattr(cls, "body")
                    if isinstance(body_, ast.Assign)
                ]
                api_type, api_value = _get_api_group_and_version(bodies=bodies)
                errors.extend(
                    _get_namespaced(
                        cls=cls, resource_dict=resource_dict, api_value=api_value
                    )
                )
                errors.extend(
                    _process_api_type(
                        api_type=api_type,
                        api_value=api_value,
                        resource_dict=resource_dict,
                        cls=cls,
                    )
                )
    return errors


def test_resources_definitions(resources_definitions_errors):
    assert not resources_definitions_errors, "\n".join(resources_definitions_errors)
