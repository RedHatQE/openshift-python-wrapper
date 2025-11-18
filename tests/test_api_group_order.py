import ast
import os

import pytest
from deepdiff.diff import difflib


def test_api_group_order():
    file_path = os.path.join("ocp_resources", "resource.py")
    try:
        with open(file_path) as fd:
            content = fd.read()
    except OSError as exp:
        pytest.fail(f"Failed to read {file_path}: {str(exp)}")

    tree = ast.parse(source=content)
    api_group_class: list[ast.ClassDef] = [
        node for node in ast.walk(tree) if isinstance(node, ast.ClassDef) and node.name == "ApiGroup"
    ]
    if not api_group_class:
        pytest.fail("ApiGroup class not found in resource.py")

    api_groups = api_group_class[0]
    api_group_names: list[str] = []

    for _api in api_groups.body:
        try:
            # When defined with type `IO_OCP: str = "io.openshiftapi"`
            api_group_names.append(_api.target.id)
        except AttributeError:
            # When defined without type `IO_OCP = "io.openshiftapi"`
            api_group_names.append(_api.targets[0].id)

    sorted_api_group_names = sorted(api_group_names, key=lambda x: x.replace("_", " "))
    errors: set[str] = set()
    for _diff in difflib.Differ().compare(api_group_names, sorted_api_group_names):
        if _diff.startswith("-") or _diff.startswith("+") or _diff.startswith("?"):
            _err_diff = _diff.split(" ")[-1]
            errors.add(_err_diff)

    _errors_str = "\n".join(list(errors))
    assert not errors, f"ApiGroup class should be sorted alphabetically. Missed places ApiGroups: {_errors_str}"
