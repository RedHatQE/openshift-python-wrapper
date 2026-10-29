"""Test generation utilities for class generator."""

import os
from typing import Any

from rich.console import Console
from rich.panel import Panel
from simple_logger.logger import get_logger

from class_generator.constants import TESTS_MANIFESTS_DIR
from class_generator.core.generator import generate_resource_file_from_dict
from class_generator.formatters.template_renderer import render_jinja_template

LOGGER = get_logger(name=__name__)


def render_class_generator_tests() -> str | None:
    """
    Render the class-generator test file from the manifests and the Jinja template.

    Returns:
        Rendered file content, or None when the template or manifests cannot be read
    """
    tests_info: dict[str, list[dict[str, Any]]] = {"template": []}
    dirs_to_ignore: list[str] = ["__pycache__"]

    try:
        dir_contents = os.listdir(str(TESTS_MANIFESTS_DIR))
    except OSError as e:
        LOGGER.error(f"Failed to list directory {TESTS_MANIFESTS_DIR}: {e}")
        return None

    for _dir in dir_contents:
        dir_path = TESTS_MANIFESTS_DIR / _dir

        try:
            if not dir_path.is_dir() or _dir in dirs_to_ignore:
                continue
        except OSError as e:
            LOGGER.warning(f"Failed to check if {dir_path} is a directory: {e}")
            continue

        test_data: dict[str, Any] = {"kind": _dir, "res_files": []}

        try:
            file_contents = os.listdir(str(dir_path))
        except OSError as e:
            LOGGER.warning(f"Failed to list files in {dir_path}: {e}")
            continue

        # Collect all files ending with ".py"
        for _file in file_contents:
            if _file.endswith(".py") and not _file.startswith("__"):
                test_data["res_files"].append(_file)

        # Only append test_data if at least one valid Python file (ending with ".py" and not starting with "__") was found
        if test_data["res_files"]:
            tests_info["template"].append(test_data)

    try:
        rendered = render_jinja_template(
            template_dict=tests_info,
            template_dir=str(TESTS_MANIFESTS_DIR),
            template_name="test_parse_explain.j2",
        )
    except FileNotFoundError as e:
        LOGGER.error(f"Template file 'test_parse_explain.j2' not found: {e}")
        return None
    except Exception as e:
        LOGGER.error(
            f"Failed to render template 'test_parse_explain.j2': {e}. "
            f"This may be due to template syntax errors or missing variables."
        )
        return None

    return rendered


def generate_class_generator_tests() -> None:
    """Generate test files for class generator."""
    rendered = render_class_generator_tests()
    if rendered is None:
        return

    test_file_path = TESTS_MANIFESTS_DIR.parent / "test_class_generator.py"

    try:
        with open(test_file_path, "w", encoding="utf-8") as fd:
            fd.write(rendered)
            if not rendered.endswith("\n"):
                fd.write("\n")
    except OSError as e:
        LOGGER.error(f"Failed to write test file to {test_file_path}: {e}")
        return

    LOGGER.info(f"Generated test file: {test_file_path}")
    console = Console()
    console.print(Panel.fit(f"[green]Generated test file:[/green] [cyan]{test_file_path}[/cyan]"))


class TestHandWrittenFileConversion:
    """A hand-maintained resource can be converted into a generated one."""

    def test_hand_written_file_is_converted_not_blocked(self, tmp_path, caplog, monkeypatch):
        hand_written = tmp_path / "node_network_configuration_policy.py"
        hand_written.write_text("import re\n\n\nclass NodeNetworkConfigurationPolicy:\n    pass\n")

        resource_dict = {
            "kind": "NodeNetworkConfigurationPolicy",
            "base_class": "Resource",
            "group": "nmstate.io",
            "api_version": "v1",
            "version": "v1",
            "api_group": "nmstate.io",
            "description": "NodeNetworkConfigurationPolicy is a hand-maintained resource.",
            "namespaced": False,
            "fields": [],
            "spec": [],
        }

        # keep prek out of the tmp dir (hooks are repo-scoped)
        monkeypatch.setattr(
            "class_generator.core.generator.write_and_format_rendered",
            lambda filepath, output: __import__("pathlib").Path(filepath).write_text(output),
        )

        _orig, generated = generate_resource_file_from_dict(
            resource_dict=resource_dict,
            overwrite=True,
            output_file=str(hand_written),
        )

        # overwritten with generated output instead of being refused
        assert generated == str(hand_written)
        converted = hand_written.read_text()
        assert "class NodeNetworkConfigurationPolicy" in converted
        assert "hand-maintained" in caplog.text


class TestGeneratedTestFile:
    """The generated test file must always match its template (issue #2840)."""

    def test_rendered_template_matches_committed_test(self) -> None:
        rendered = render_class_generator_tests()

        assert rendered is not None, "template could not be rendered"
        if not rendered.endswith("\n"):
            rendered += "\n"

        committed_path = TESTS_MANIFESTS_DIR.parent / "test_class_generator.py"
        assert rendered == committed_path.read_text(encoding="utf-8"), (
            "test_class_generator.py does not match test_parse_explain.j2 - "
            "regenerate it with --add-tests instead of editing the generated file"
        )

    def test_template_guards_against_str_unpack(self) -> None:
        """A drift result is a str when clean and a tuple when drifted; never unpack blindly."""
        template = (TESTS_MANIFESTS_DIR / "test_parse_explain.j2").read_text(encoding="utf-8")

        assert "for drifted_file, _categories in drifted_files" not in template
        assert "isinstance(drifted, tuple)" in template
