import ast
import os
from typing import List, Set
from deepdiff.diff import difflib
import pytest


def test_api_group_order():
    file_path = os.path.join("ocp_resources", "resource.py")
    try:
        with open(file_path) as fd:
            content = fd.read()
    except IOError as exp:
        pytest.fail(f"Failed to read {file_path}: {str(exp)}")

    tree = ast.parse(source=content)
    api_group_class: List[ast.ClassDef] = [
        node for node in ast.walk(tree) if isinstance(node, ast.ClassDef) and node.name == "ApiGroup"
    ]
    if not api_group_class:
        pytest.fail("ApiGroup class not found in resource.py")

    api_groups = api_group_class[0]
    api_group_names = [node.target.id for node in api_groups.body]
    sorted_api_group_names = sorted(api_group_names, key=lambda x: x.replace("_", " "))
    errors: Set[str] = set()
    for _diff in difflib.Differ().compare(api_group_names, sorted_api_group_names):
        if _diff.startswith("-") or _diff.startswith("+") or _diff.startswith("?"):
            _err_diff = _diff.split(" ")[-1]
            errors.add(_err_diff)

    assert not errors, (
        f"ApiGroup class should be sorted alphabetically. Missed places ApiGroups: {'\n'.join(list(errors))}"
    )
