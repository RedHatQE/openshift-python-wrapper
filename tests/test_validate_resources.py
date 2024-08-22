# This test uses https://github.com/RedHatQE/openshift-resources-definitions to get resource definitions json file
# File: resources_definitions.json

from __future__ import annotations
import ast
import json
import os
from typing import Any, Dict, Generator, List, Tuple

import pytest

from ocp_resources.resource import Resource  # noqa


def _api_group_name(api_value: str) -> str:
    try:
        if api_value:
            return eval(f"Resource.ApiGroup.{api_value}")
    except AttributeError:
        return api_value


def _get_api_group_and_version(bodies: List[Any]) -> Tuple[str, str]:
    for targets in bodies:
        targets: ast.AnnAssign | ast.Attribute
        if isinstance(targets, ast.AnnAssign):
            api_type = targets.target.id
        else:
            api_type = targets.targets[0].id

        return api_type, getattr(targets.value, "attr", getattr(targets.value, "value", None))

    return "", ""


def validate_resource(
    cls: ast.ClassDef,
    resource_list: List[Dict[str, Any]],
    api_value: str,
    api_type: str,
) -> List[str]:
    errors = []

    if not api_type:
        errors.append(f"Resource {cls.name} must have api_group or api_version")

    for base in getattr(cls, "bases", []):
        namespaced = base.id == "NamespacedResource"
        api_group_name = _api_group_name(api_value=api_value)
        for resource_dict in resource_list:
            for group_version_kind in resource_dict["x-kubernetes-group-version-kind"]:
                if api_type == "api_group":
                    if (api_group := group_version_kind["group"]) == api_group_name:
                        # Check if resource is namespaced
                        if namespaced != resource_dict["namespaced"]:
                            errors.append(
                                f"Resource {cls.name} should be "
                                f"{'namespaced' if namespaced else 'in cluster scope (not namespaced)'}"
                            )

                        # If resource has api group but class has api version
                        if api_type == "api_version":
                            errors.append(
                                f"Resource {cls.name} have api_version {api_value} but should have api_group = "
                                f"{api_group.upper()}"
                            )

                else:
                    if (resource_api_version := group_version_kind["version"].lower()) != api_value.lower():
                        errors.append(
                            f"Resource {cls.name} have api_version {api_value} but should have api_version = "
                            f"{resource_api_version}"
                        )

    return errors


def _get_api_group(api_value: str, cls: ast.ClassDef, resource_dict: Dict[str, Any]) -> List[str]:
    errors = []
    api_group_name = _api_group_name(api_value=api_value)

    if api_group_name not in resource_dict["api_group"]:
        errors.append(f"Resource {cls.name} api_group should be {resource_dict['api_group']}. got {api_group_name}")
    return errors


def _resource_file() -> Generator[str, None, None]:
    ocp_resources_exclude_files = ["resource.py", "utils.py", "__init__.py"]
    for root, _, files in os.walk("ocp_resources"):
        for _file in files:
            if _file in ocp_resources_exclude_files or not _file.endswith(".py"):
                continue

            yield os.path.join(root, _file)


@pytest.fixture()
def resources_definitions() -> Generator[Dict[str, Any], None, None]:
    with open("class_generator/schema/__resources-mappings.json") as fd:
        yield json.load(fd)


@pytest.fixture()
def resources_definitions_errors(resources_definitions: Dict[str, Any]) -> List[str]:
    errors = []
    for _file in _resource_file():
        with open(_file) as fd:
            data = fd.read()
            if data.startswith(
                "# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md"
            ):
                continue

            tree = ast.parse(source=data)
            classes = [cls for cls in tree.body if isinstance(cls, ast.ClassDef)]
            for cls in classes:
                resource_list = resources_definitions.get(cls.name.lower())
                if not resource_list:
                    continue

                bodies = [body_ for body_ in getattr(cls, "body") if isinstance(body_, (ast.Assign, ast.AnnAssign))]
                api_type, api_value = _get_api_group_and_version(bodies=bodies)
                errors.extend(
                    validate_resource(
                        cls=cls,
                        resource_list=resource_list,
                        api_value=api_value,
                        api_type=api_type,
                    )
                )

    return errors


def test_resources_definitions(resources_definitions_errors):
    assert not resources_definitions_errors, "\n".join(resources_definitions_errors)
