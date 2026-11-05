"""Guard the AGENTS.md rule that resources are always constructed with an explicit client.

`examples/` is excluded from every pre-commit hook (see `.pre-commit-config.yaml`), so a
resource constructed without ``client=`` there fails only when a reader runs the example.
That is exactly how `examples/role.py` and `examples/node_network_configuration_policy.py`
were broken by the mandatory-client change while all checks stayed green.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import pkgutil
from pathlib import Path

import ocp_resources
from ocp_resources.resource import Resource

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"

# Classmethod APIs that take a client as well.
CLASSMETHOD_APIS = frozenset({"delete_events", "get", "get_all_cluster_resources", "list"})

# `examples/special_cases.py` imports `ocp_resources.network`, a module that does not
# exist, so it is already broken independently of the client contract.
SKIPPED_EXAMPLES = frozenset({"special_cases.py"})


def _resource_class_names() -> set[str]:
    """Return the names of every Resource/NamespacedResource subclass in the package."""
    names: set[str] = set()
    for module_info in pkgutil.iter_modules(ocp_resources.__path__):
        try:
            module = importlib.import_module(f"ocp_resources.{module_info.name}")
        except Exception:  # pragma: no cover - a module that cannot import cannot be scanned
            continue

        for name, obj in vars(module).items():
            if inspect.isclass(obj) and obj.__module__ == module.__name__ and issubclass(obj, Resource):
                names.add(name)

    return names


def _call_target(node: ast.Call, resource_names: set[str]) -> str:
    """Return the resource API name for the call, or an empty string when it is unrelated."""
    func = node.func

    if isinstance(func, ast.Name):
        return func.id if func.id in resource_names else ""

    # e.g. Pod.get(...) / Resource.get_all_cluster_resources(...)
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        if func.value.id in resource_names and func.attr in CLASSMETHOD_APIS:
            return f"{func.value.id}.{func.attr}"

    return ""


def _missing_client_calls(tree: ast.AST, resource_names: set[str]) -> list[str]:
    """Return `file:line` markers for resource calls that omit `client=`."""
    missing: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        target = _call_target(node=node, resource_names=resource_names)
        if not target:
            continue

        keywords = {keyword.arg for keyword in node.keywords}
        if None in keywords:  # **kwargs splat, cannot be checked statically
            continue

        if "client" not in keywords:
            missing.append(f"{target}(...)")

    return missing


def test_examples_construct_resources_with_client() -> None:
    """Every resource construction in examples/ must pass an explicit client."""
    resource_names = _resource_class_names()
    assert resource_names, "failed to discover any resource class"

    offenders: list[str] = []

    for path in sorted(EXAMPLES_DIR.glob("*.py")):
        if path.name in SKIPPED_EXAMPLES:
            continue

        for marker in _missing_client_calls(tree=ast.parse(path.read_text()), resource_names=resource_names):
            offenders.append(f"{path.name}: {marker}")

    assert not offenders, "resources constructed without client= in examples:\n" + "\n".join(offenders)
