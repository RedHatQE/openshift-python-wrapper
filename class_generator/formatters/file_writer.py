"""File writing utilities for generated code."""

from pathlib import Path

from pyhelper_utils.shell import run_command
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)

# Project root directory (contains pyproject.toml and .pre-commit-config.yaml)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def write_and_format_rendered(filepath: str, output: str) -> None:
    """
    Write rendered content to file and format with prek, falling back to ruff.

    Args:
        filepath: Path to write the file to
        output: Content to write
    """
    with open(filepath, "w", encoding="utf-8") as fd:
        fd.write(output)

    pre_commit_config = str(_PROJECT_ROOT / ".pre-commit-config.yaml")
    pyproject_toml = str(_PROJECT_ROOT / "pyproject.toml")

    # Try prek first (runs all pre-commit hooks including ruff)
    prek_success = False
    try:
        rc, stdout, stderr = run_command(
            command=["uvx", "prek", "-c", pre_commit_config, "run", "--files", filepath],
            verify_stderr=False,
            check=False,
            log_errors=False,
        )
        if not rc:
            if stderr:
                LOGGER.warning(f"Prek hooks failed for {filepath}, falling back to ruff.")
                LOGGER.debug(f"prek stderr: {stderr}")
            else:
                prek_success = True

            if stdout:
                LOGGER.info(f"{filepath} fixed by prek")
                LOGGER.debug(f"prek stdout: {stdout}")
    except Exception as e:
        LOGGER.warning(f"Failed to run prek for {filepath}, falling back to ruff: {e}")

    if not prek_success:
        _run_ruff_fallback(filepath=filepath, pyproject_toml=pyproject_toml)


def _run_ruff_fallback(filepath: str, pyproject_toml: str) -> None:
    """Run ruff check --fix and ruff format as fallback when prek fails."""
    for ruff_cmd in (
        ["uvx", "ruff", "check", "--fix", "--config", pyproject_toml, filepath],
        ["uvx", "ruff", "format", "--config", pyproject_toml, filepath],
    ):
        try:
            _, stdout, _ = run_command(
                command=ruff_cmd,
                verify_stderr=False,
                check=False,
                log_errors=False,
            )
            if stdout:
                LOGGER.info(f"{filepath} fixed by ruff")
                LOGGER.debug(f"ruff stdout: {stdout}")
        except Exception as e:
            LOGGER.error(f"Ruff fallback failed for {filepath}: {e}")
