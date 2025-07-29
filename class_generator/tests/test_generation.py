"""Test generation utilities for class generator."""

import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from simple_logger.logger import get_logger

from class_generator.constants import TESTS_MANIFESTS_DIR
from class_generator.formatters.template_renderer import render_jinja_template

LOGGER = get_logger(name=__name__)


def generate_class_generator_tests() -> None:
    """Generate test files for class generator."""
    tests_info: dict[str, list[dict[str, str]]] = {"template": []}
    dirs_to_ignore: list[str] = ["__pycache__"]

    for _dir in os.listdir(TESTS_MANIFESTS_DIR):
        dir_path = os.path.join(TESTS_MANIFESTS_DIR, _dir)
        if os.path.isdir(dir_path) and _dir not in dirs_to_ignore:
            test_data: dict[str, str] = {"kind": _dir}
            for _file in os.listdir(dir_path):
                if _file.endswith("_res.py"):
                    test_data["res_file"] = _file

            tests_info["template"].append(test_data)

    rendered = render_jinja_template(
        template_dict=tests_info,
        template_dir=TESTS_MANIFESTS_DIR,
        template_name="test_parse_explain.j2",
    )

    test_file_path = os.path.join(Path(TESTS_MANIFESTS_DIR).parent, "test_class_generator.py")
    with open(test_file_path, "w") as fd:
        fd.write(rendered)
    LOGGER.info(f"Generated test file: {test_file_path}")
    console = Console()
    console.print(Panel.fit(f"[green]Generated test file:[/green] [cyan]{test_file_path}[/cyan]"))
