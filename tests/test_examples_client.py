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

# Classmethod APIs that take a client as their first positional argument.
CLASSMETHOD_APIS = frozenset({"delete_events", "get", "get_all_cluster_resources", "list"})

# Client-requiring API classes that are not Resource subclasses, so they only need a
# client on the classmethods above - constructing them takes no client at all.
CLASSMETHOD_ONLY_CLASSES = frozenset({Event.__name__})

# Class discovery must find at least this many classes. Measured 248 Resource subclasses
# on 2026-11-04; a drop below the floor means discovery broke and the guard stopped
# covering the affected resources.
MIN_DISCOVERED_CLASSES = 240


def _resource_class_names() -> set[str]:
    """Collect every Resource/NamespacedResource subclass name.

    Returns:
        set[str]: Names of the resource classes the examples may instantiate.

    Raises:
        RuntimeError: If a module or package cannot be imported, if fewer modules were
            imported than walked, or if discovery is implausibly small. Each of those
            would silently shrink the set of checked names.
    """
    names: set[str] = set()
    import_failures: list[str] = []
    walked = 0
    imported = 0

    for module_info in pkgutil.walk_packages(
        ocp_resources.__path__,
        prefix="ocp_resources.",
        # Without onerror, a package that fails to import is skipped silently and its
        # submodules are never yielded, so the failure would never be recorded.
        onerror=lambda name: import_failures.append(f"{name}: package import failed"),
    ):
        walked += 1

        try:
            module = importlib.import_module(module_info.name)
        except Exception as err:
            import_failures.append(f"{module_info.name}: {err!r}")
            continue

        imported += 1

        for name, obj in vars(module).items():
            if inspect.isclass(obj) and obj.__module__ == module.__name__ and issubclass(obj, Resource):
                names.add(name)

    if import_failures:
        raise RuntimeError(f"cannot discover resource classes, failed to import: {import_failures}")

    if imported != walked:
        raise RuntimeError(f"imported {imported} of {walked} walked modules: discovery is incomplete")

    if len(names) <= MIN_DISCOVERED_CLASSES:
        raise RuntimeError(
            f"discovered only {len(names)} resource classes, expected more than {MIN_DISCOVERED_CLASSES}:"
            " class discovery is broken"
        )

    return names


def _import_aliases(tree: ast.AST, resource_names: set[str]) -> tuple[dict[str, str], set[str]]:
    """Resolve the local names a module binds for resource classes and the package.

    Args:
        tree: Parsed module.
        resource_names: Known resource class names.

    Returns:
        tuple[dict[str, str], set[str]]: Local alias to resource class name, e.g.
            ``{"R": "Role"}``, and the local names bound to ``ocp_resources`` or one of
            its modules, e.g. ``{"ocp_resources", "r"}``.
    """
    class_aliases: dict[str, str] = {}
    module_names: set[str] = {"ocp_resources"}

    known_api_names = resource_names | CLASSMETHOD_ONLY_CLASSES

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("ocp_resources"):
            for alias in node.names:
                if alias.name in known_api_names and alias.asname:
                    class_aliases[alias.asname] = alias.name
                elif node.module == "ocp_resources":
                    module_names.add(alias.asname or alias.name)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "ocp_resources" or alias.name.startswith("ocp_resources."):
                    module_names.add(alias.asname or alias.name.split(".")[0])

    return class_aliases, module_names


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


def _call_target(
    node: ast.Call,
    resource_names: set[str],
    class_aliases: dict[str, str],
    module_names: set[str],
) -> tuple[str, bool]:
    """Identify whether a call targets a client-requiring resource API.

    Args:
        node: Call node to inspect.
        resource_names: Known resource class names.
        class_aliases: Local alias to resource class name mapping.
        module_names: Local names bound to the ocp_resources package or its modules.

    Returns:
        tuple[str, bool]: The API name (empty when unrelated) and whether it is a
            classmethod, where the client may also be passed positionally.
    """
    func = node.func

    if isinstance(func, ast.Name):
        name = class_aliases.get(func.id, func.id)
        return (name, False) if name in resource_names else ("", False)

    if isinstance(func, ast.Attribute):
        chain = _attribute_chain(node=func)

        if len(chain) < 2:
            return "", False

        owner = class_aliases.get(chain[-2], chain[-2])

        if chain[-1] in CLASSMETHOD_APIS and (owner in resource_names or owner in CLASSMETHOD_ONLY_CLASSES):
            return f"{owner}.{chain[-1]}", True

        # Only module-qualified access counts as a constructor; `self.Pod(...)` or
        # `factory.Secret(...)` just happen to share a name with a resource class.
        if chain[-1] in resource_names and chain[0] in module_names:
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
    class_aliases, module_names = _import_aliases(tree=tree, resource_names=resource_names)
    missing: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        target, is_classmethod = _call_target(
            node=node, resource_names=resource_names, class_aliases=class_aliases, module_names=module_names
        )
        if not target:
            continue

        keywords = {keyword.arg for keyword in node.keywords}
        if None in keywords or any(isinstance(arg, ast.Starred) for arg in node.args):
            continue

        # Constructors take client as a required keyword; classmethods take it first,
        # because `get`/`list`/`delete_events` declare client as their first parameter.
        # Classmethods declare client as their first parameter, so any non-literal
        # positional expression may be a client; literals cannot be DynamicClients.
        positional_client = is_classmethod and node.args and not isinstance(node.args[0], (ast.Constant, ast.Starred))
        if "client" in keywords or positional_client:
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
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for marker in _missing_client_calls(tree=tree, resource_names=resource_names):
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
        pytest.param("Secret.get(client_obj)", [], id="classmethod-client-object"),
        pytest.param("Secret.get(get_client())", [], id="classmethod-client-factory"),
        pytest.param('Secret.get("name")', ["1: Secret.get(...)"], id="classmethod-non-client-positional"),
        pytest.param("Secret.get(*args)", [], id="classmethod-starred-args-is-skipped"),
        pytest.param("Resource.get_all_cluster_resources(c)", [], id="cluster-resources-positional-client"),
        pytest.param("Event.get()", ["1: Event.get(...)"], id="event-api-without-client"),
        pytest.param("Event.list()", ["1: Event.list(...)"], id="event-list-without-client"),
        pytest.param("Event.delete_events(client=c)", [], id="event-api-with-client"),
        pytest.param("Event()", [], id="event-construction-needs-no-client"),
        pytest.param("from ocp_resources.role import Role as R\nR(name='n')", ["2: Role(...)"], id="aliased-import"),
        pytest.param(
            'from ocp_resources.pod import Pod as P\nP.get(label_selector="a")',
            ["2: Pod.get(...)"],
            id="aliased-classmethod",
        ),
        pytest.param(
            "import ocp_resources.role\nocp_resources.role.Role(name='n')", ["2: Role(...)"], id="qualified-import"
        ),
        pytest.param('import ocp_resources.role as r\nr.Role(name="n")', ["2: Role(...)"], id="module-alias-import"),
        pytest.param("from ocp_resources import role\nrole.Role(name='n')", ["2: Role(...)"], id="from-package-module"),
        pytest.param(
            "from ocp_resources import pod as p\np.Pod(name='n')", ["2: Pod(...)"], id="from-package-module-alias"
        ),
        pytest.param("from ocp_resources.event import Event as E\nE.get()", ["2: Event.get(...)"], id="event-alias"),
        pytest.param('self.Secret(name="n")', [], id="attribute-named-like-a-resource-is-not-a-constructor"),
        pytest.param('factory.Role(name="n")', [], id="foreign-object-attribute-is-not-a-constructor"),
        pytest.param("Secret(**kwargs)", [], id="kwargs-splat-is-skipped"),
        pytest.param("print(Secret.__name__)", [], id="non-call-is-ignored"),
    ],
)
def test_missing_client_detection(source: str, expected: list[str]) -> None:
    """The detector must flag every client-less resource call and nothing else.

    Args:
        source: Python source snippet to parse.
        expected: Expected ``<line>: <API>(...)`` markers, empty when no client is missing.
    """
    resource_names = {"Secret", "Resource", "Role", "Pod"}

    assert _missing_client_calls(tree=ast.parse(source), resource_names=resource_names) == expected
