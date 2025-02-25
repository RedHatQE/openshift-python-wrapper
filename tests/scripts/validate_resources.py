from __future__ import annotations
import ast
import json
import os
from typing import Any, Dict, Generator, List, Tuple


from ocp_resources.resource import Resource  # noqa


def _get_api_value_by_type(api_value: str, api_type: str) -> str:
    try:
        if api_value:
            if api_type == "api_version":
                return eval(f"Resource.ApiVersion.{api_value}")

            elif api_type == "api_group":
                return eval(f"Resource.ApiGroup.{api_value}")

    except AttributeError:
        pass

    return api_value


def _get_api_group_and_version(bodies: List[Any]) -> Tuple[str, str]:
    for targets in bodies:
        targets: ast.AnnAssign | ast.Attribute
        if isinstance(targets, ast.AnnAssign):
            api_type = targets.target.id
        else:
            api_type = targets.targets[0].id

        if api_type in ("api_version", "api_group"):
            return api_type, getattr(targets.value, "attr", getattr(targets.value, "value", None))

    return "", ""


def validate_resource(
    cls: ast.ClassDef,
    resource_list: List[Dict[str, Any]],
    api_value: str,
    api_type: str,
) -> List[str]:
    errors: List[str] = []
    resource_str: str = "Resource"
    namespaced_resource_str: str = "NamespacedResource"
    _base_class_error: str = f"Resource {cls.name} must have {resource_str} or {namespaced_resource_str} base class"
    _api_type_group: bool = api_type == "api_group"
    _api_type_version: bool = api_type == "api_version"

    bases = getattr(cls, "bases", [])
    if not bases:
        return [_base_class_error]

    base_class_from = [_base for _base in bases if _base.id in (resource_str, namespaced_resource_str)]
    if not base_class_from:
        return [f"{_base_class_error}, got {[_base.id for _base in bases]}"]

    if len(base_class_from) > 1:
        return [f"Resource {cls.name} must have only one of {resource_str} or {namespaced_resource_str} base class"]

    if not api_type:
        errors.append(f"Resource {cls.name} must have api_group or api_version")

    namespaced_based: bool = base_class_from[0].id == namespaced_resource_str
    api_value_name = _get_api_value_by_type(api_value=api_value, api_type=api_type)
    matched_resource: Dict[str, Any] = {}

    for resource_dict in resource_list:
        _x_kind = resource_dict["x-kubernetes-group-version-kind"]

        if _api_type_group and api_value_name:
            if api_group_resource := [_data for _data in _x_kind if _data["group"] == api_value_name]:
                matched_resource.update(api_group_resource[0])
                matched_resource["namespaced"] = resource_dict["namespaced"]
                break

        else:
            matched_resource.update([_data for _data in _x_kind if _data["version"]][0])
            matched_resource["namespaced"] = resource_dict["namespaced"]
            break

    if not matched_resource:
        print(f"Warning: Resource {cls.name} not found in resources definitions")
        return errors

    if _api_type_version and matched_resource.get("group"):
        errors.append(f"Resource {cls.name} have api_version {api_value} but should have api_group")

    elif _api_type_version and matched_resource["version"] != api_value_name:
        errors.append(
            f"Resource {cls.name} have api_group {api_value_name} but should have api_version = "
            f"{matched_resource['version']}"
        )

    if namespaced_based != matched_resource["namespaced"]:
        errors.append(
            f"Resource {cls.name} base class is `{base_class_from[0].id}` but should have base class `{namespaced_resource_str if matched_resource['namespaced'] else resource_str}`"
        )

    return errors


def resource_file() -> Generator[str, None, None]:
    ocp_resources_exclude_files = ["resource.py", "utils.py", "__init__.py"]
    for root, _, files in os.walk("ocp_resources"):
        for _file in files:
            if _file in ocp_resources_exclude_files or not _file.endswith(".py"):
                continue

            yield os.path.join(root, _file)


def parse_resource_file_for_errors(data) -> List[str]:
    errors: List[str] = []
    _resources_definitions = resources_definitions()

    if data.startswith(
        "# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md"
    ):
        return []

    tree = ast.parse(source=data)
    classes = [cls for cls in tree.body if isinstance(cls, ast.ClassDef)]
    classes_to_skip = "Event"
    for cls in classes:
        if cls.name in classes_to_skip:
            continue

        resource_list = _resources_definitions.get(cls.name.lower())
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


def resources_definitions() -> Dict[str, Any]:
    with open("class_generator/schema/__resources-mappings.json") as fd:
        return json.load(fd)
