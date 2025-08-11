"""Test generation utilities for class generator."""

import os
from typing import Any

from rich.console import Console
from rich.panel import Panel
from simple_logger.logger import get_logger

from class_generator.constants import TESTS_MANIFESTS_DIR
from class_generator.formatters.template_renderer import render_jinja_template

LOGGER = get_logger(name=__name__)


def generate_class_generator_tests() -> None:
    """Generate test files for class generator."""
    tests_info: dict[str, list[dict[str, Any]]] = {"template": []}
    dirs_to_ignore: list[str] = ["__pycache__"]

    try:
        dir_contents = os.listdir(str(TESTS_MANIFESTS_DIR))
    except OSError as e:
        LOGGER.error(f"Failed to list directory {TESTS_MANIFESTS_DIR}: {e}")
        return

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
        return
    except Exception as e:
        LOGGER.error(
            f"Failed to render template 'test_parse_explain.j2': {e}. "
            f"This may be due to template syntax errors or missing variables."
        )
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
