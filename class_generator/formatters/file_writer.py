"""File writing and formatting utilities for generated code."""

import shlex
import shutil

from pyhelper_utils.shell import run_command
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def check_command_available(command: str) -> bool:
    """
    Check if a command is available in the system PATH.

    Args:
        command: Command to check for availability

    Returns:
        bool: True if command is available, False otherwise
    """
    return shutil.which(command) is not None


def write_and_format_rendered(filepath: str, output: str) -> None:
    """
    Write rendered content to file and format it with ruff.

    Args:
        filepath: Path to write the file to
        output: Content to write
    """
    with open(filepath, "w", encoding="utf-8") as fd:
        fd.write(output)

    # Check if uvx is available
    if not check_command_available("uvx"):
        LOGGER.warning("'uvx' command not found in PATH. Skipping code formatting.")
        return

    # Try to check if ruff is available via uvx
    try:
        rc, _, _ = run_command(
            command=shlex.split("uvx ruff --version"),
            verify_stderr=False,
            check=False,
        )
        if not rc:
            LOGGER.warning("'ruff' is not available via uvx. Skipping code formatting.")
            return
    except Exception as e:
        LOGGER.warning(f"Failed to check ruff availability: {e}. Skipping code formatting.")
        return

    # Run ruff formatting and checking
    for op in ("format", "check"):
        try:
            rc, stdout, stderr = run_command(
                command=shlex.split(f"uvx ruff {op} {filepath}"),
                verify_stderr=False,
                check=False,
            )

            if rc:
                LOGGER.debug(f"Successfully ran 'uvx ruff {op}' on {filepath}")
            else:
                LOGGER.warning(f"'uvx ruff {op}' failed for {filepath}")
                if stderr:
                    LOGGER.debug(f"stderr: {stderr}")
                if stdout:
                    LOGGER.debug(f"stdout: {stdout}")

        except Exception as e:
            LOGGER.error(f"Exception while running 'uvx ruff {op}' on {filepath}: {e}")
            # Continue to next operation or finish
