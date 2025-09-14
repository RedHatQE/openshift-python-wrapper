"""File writing utilities for generated code."""

from pyhelper_utils.shell import run_command
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def write_and_format_rendered(filepath: str, output: str) -> None:
    """
    Write rendered content to file and format it with prek.

    Args:
        filepath: Path to write the file to
        output: Content to write
    """
    with open(filepath, "w", encoding="utf-8") as fd:
        fd.write(output)

    # Run prek on the file
    try:
        rc, stdout, stderr = run_command(
            command=["uvx", "prek", "run", "--files", filepath],
            verify_stderr=False,
            check=False,
            log_errors=False,
        )
        if not rc:
            if stderr:
                LOGGER.warning(f"Prek hooks failed for {filepath}. This is non-fatal and generation will continue.")
                LOGGER.debug(f"prek stderr: {stderr}")
            if stdout:
                LOGGER.info(f"{filepath} fixed by prek")
                LOGGER.debug(f"rek stdout: {stdout}")
    except Exception as e:
        LOGGER.error(f"Failed to run prek hooks for {filepath}: {e}. This is non-fatal and generation will continue.")
