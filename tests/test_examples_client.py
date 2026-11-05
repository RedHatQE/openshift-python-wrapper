"""Guard the AGENTS.md rule that every resource is built with an explicit client.

`examples/` is excluded from the mypy hook (`.pre-commit-config.yaml`), and mypy cannot
catch this class of break anyway: the wrappers accept `client` through `**kwargs`, so
`Role(name=..., rules=...)` type-checks clean and fails only at runtime. That is how
`examples/role.py` and `examples/node_network_configuration_policy.py` were broken by the
mandatory-client change while every check stayed green.

This test therefore checks the examples statically: every construction of a
Resource/NamespacedResource subclass - and every `get`/`list`/`get_all_cluster_resources`/
`delete_events` call on one, plus the `Event` APIs - must receive a client, either as the
`client=` keyword or as the first positional argument of a classmethod.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import pkgutil
from pathlib import Path

import pytest

import ocp_resources
from ocp_resources.event import Event
from ocp_resources.resource import Resource

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"

# Classmethod APIs that require a client as their first argument.
CLASSMETHOD_APIS = frozenset({"delete_events", "get", "get_all_cluster_resources", "list"})

# Class discovery must find at least this many classes; a drop means discovery broke and
# the guard silently stopped covering the affected resources.
MIN_DISCOVERED_CLASSES = 200


def _resource_class_names() -> set[str]:
    """Collect every resource class name the examples may instantiate.

    Returns:
        set[str]: Names of the Resource/NamespacedResource subclasses, plus the names of
            the non-Resource API classes that take a client (``Event``).

    Raises:
        AssertionError: If a module cannot be imported or discovery is implausibly small,
            both of which would silently shrink the set of checked names.
    """
    names: set[str] = {Event.__name__}
    import_failures: list[str] = []

    for module_info in pkgutil.walk_packages(ocp_resources.__path__, prefix="ocp_resources."):
        try:
            module = importlib.import_module(module_info.name)
        except Exception as err:
            import_failures.append(f"{module_info.name}: {err!r}")
            continue

        for name, obj in vars(module).items():
            if inspect.isclass(obj) and obj.__module__ == module.__name__ and issubclass(obj, Resource):
                names.add(name)

    assert not import_failures, f"cannot discover resource classes, failed to import: {import_failures}"
    assert len(names) > MIN_DISCOVERED_CLASSES, (
        f"discovered only {len(names)} resource classes, expected more than {MIN_DISCOVERED_CLASSES}:"
        " class discovery is broken"
    )

    return names


def _import_aliases(tree: ast.AST, resource_names: set[str]) -> dict[str, str]:
    """Map local import aliases back to the resource class they refer to.

    Args:
        tree: Parsed module.
        resource_names: Known resource class names.

    Returns:
        dict[str, str]: Local name to resource class name, e.g. ``{"R": "Role"}`` for
            ``from ocp_resources.role import Role as R``.
    """
    aliases: dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("ocp_resources"):
            for alias in node.names:
                if alias.name in resource_names and alias.asname:
                    aliases[alias.asname] = alias.name

    return aliases


def _attribute_chain(node: ast.expr) -> list[str]:
    """Flatten an attribute chain into its dotted parts.

    Args:
        node: Expression to flatten.

    Returns:
        list[str]: Parts of the chain, e.g. ``["ocp_resources", "role", "Role", "get"]``.
    """
    parts: list[str] = []

    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value

    if isinstance(node, ast.Name):
        parts.append(node.id)

    return list(reversed(parts))


def _call_target(node: ast.Call, resource_names: set[str], aliases: dict[str, str]) -> tuple[str, bool]:
    """Identify whether a call targets a client-requiring resource API.

    Args:
        node: Call node to inspect.
        resource_names: Known resource class names.
        aliases: Local alias to resource class name mapping.

    Returns:
        tuple[str, bool]: The API name (empty when unrelated) and whether it is a
            classmethod, where the client may also be passed positionally.
    """
    func = node.func

    if isinstance(func, ast.Name):
        name = aliases.get(func.id, func.id)
        return (name, False) if name in resource_names else ("", False)

    if isinstance(func, ast.Attribute):
        chain = _attribute_chain(node=func)

        if len(chain) >= 2:
            owner = aliases.get(chain[-2], chain[-2])

            if owner in resource_names and chain[-1] in CLASSMETHOD_APIS:
                return f"{owner}.{chain[-1]}", True

            # Qualified access such as `ocp_resources.role.Role(...)`.
            if chain[-1] in resource_names:
                return chain[-1], False

    return "", False


def _missing_client_calls(tree: ast.AST, resource_names: set[str]) -> list[str]:
    """Find resource calls that do not receive a client.

    Args:
        tree: Parsed module.
        resource_names: Known resource class names.

    Returns:
        list[str]: One ``"<line>: <API>(...)"`` marker per offending call.
    """
    aliases = _import_aliases(tree=tree, resource_names=resource_names)
    missing: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        target, is_classmethod = _call_target(node=node, resource_names=resource_names, aliases=aliases)
        if not target:
            continue

        keywords = {keyword.arg for keyword in node.keywords}
        if None in keywords:  # **kwargs splat, cannot be checked statically
            continue

        # Constructors take client as a required keyword; classmethods take it first.
        if "client" in keywords or (is_classmethod and node.args):
            continue

        missing.append(f"{node.lineno}: {target}(...)")

    return missing


def test_examples_construct_resources_with_client() -> None:
    """Every resource call in examples/ must receive an explicit client."""
    resource_names = _resource_class_names()
    example_paths = sorted(EXAMPLES_DIR.rglob("*.py"))
    assert example_paths, f"no example files found under {EXAMPLES_DIR}"

    offenders: list[str] = []

    for path in example_paths:
        for marker in _missing_client_calls(tree=ast.parse(path.read_text()), resource_names=resource_names):
            offenders.append(f"{path.relative_to(EXAMPLES_DIR.parent)}:{marker}")

    assert not offenders, "resource calls without a client in examples:\n" + "\n".join(offenders)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        pytest.param('Secret(name="s")', ["1: Secret(...)"], id="constructor-without-client"),
        pytest.param('Secret(client=c, name="s")', [], id="constructor-with-client"),
        pytest.param('Secret.get(label_selector="a=b")', ["1: Secret.get(...)"], id="classmethod-without-client"),
        pytest.param('Secret.get(client=c, label_selector="a=b")', [], id="classmethod-with-client"),
        pytest.param("Secret.get(c)", [], id="classmethod-positional-client"),
        pytest.param("Resource.get_all_cluster_resources(c)", [], id="cluster-resources-positional-client"),
        pytest.param("Event.get()", ["1: Event.get(...)"], id="event-api-without-client"),
        pytest.param("Event.delete_events(client=c)", [], id="event-api-with-client"),
        pytest.param("from ocp_resources.role import Role as R\nR(name='n')", ["2: Role(...)"], id="aliased-import"),
        pytest.param(
            "import ocp_resources.role\nocp_resources.role.Role(name='n')", ["2: Role(...)"], id="qualified-import"
        ),
        pytest.param("Secret(**kwargs)", [], id="kwargs-splat-is-skipped"),
        pytest.param("print(Secret.__name__)", [], id="non-call-is-ignored"),
    ],
)
def test_missing_client_detection(source: str, expected: list[str]) -> None:
    """The detector must flag every client-less resource call and nothing else."""
    resource_names = {"Secret", "Resource", "Role", "Event"}

    assert _missing_client_calls(tree=ast.parse(source), resource_names=resource_names) == expected
