"""File writing and formatting utilities for generated code."""

import shlex

from pyhelper_utils.shell import run_command


def write_and_format_rendered(filepath: str, output: str) -> None:
    """
    Write rendered content to file and format it with ruff.

    Args:
        filepath: Path to write the file to
        output: Content to write
    """
    with open(filepath, "w") as fd:
        fd.write(output)

    for op in ("format", "check"):
        run_command(
            command=shlex.split(f"uvx ruff {op} {filepath}"),
            verify_stderr=False,
            check=False,
        )
