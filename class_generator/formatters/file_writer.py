"""File writing and formatting utilities for generated code."""

import shlex
import shutil
import subprocess

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
    except FileNotFoundError:
        LOGGER.warning("'uvx' command not found when checking ruff availability. Skipping code formatting.")
        return
    except subprocess.CalledProcessError as e:
        LOGGER.warning(f"Failed to check ruff availability (exit code {e.returncode}). Skipping code formatting.")
        return
    except OSError as e:
        LOGGER.warning(f"OS error while checking ruff availability: {e}. Skipping code formatting.")
        return
    except Exception as e:
        LOGGER.warning(f"Unexpected error while checking ruff availability: {e}. Skipping code formatting.")
        return

    # Run ruff formatting and checking
    def run_ruff_operation(operation: str, filepath: str) -> None:
        """
        Run a ruff operation (format or check) on the specified file.

        Args:
            operation: The ruff operation to run ('format' or 'check')
            filepath: Path to the file to process
        """
        try:
            command = shlex.split(f"uvx ruff {operation} {filepath}")
            rc, stdout, stderr = run_command(
                command=command,
                verify_stderr=False,
                check=False,
            )

            if rc:
                LOGGER.debug(f"Successfully ran 'uvx ruff {operation}' on {filepath}")
            else:
                LOGGER.warning(f"'uvx ruff {operation}' failed for {filepath}")
                if stderr:
                    LOGGER.debug(f"stderr: {stderr}")
                if stdout:
                    LOGGER.debug(f"stdout: {stdout}")

        except FileNotFoundError as e:
            LOGGER.error(f"Command not found while running 'uvx ruff {operation}': {e}")
        except subprocess.CalledProcessError as e:
            LOGGER.error(
                f"Command failed with error code {e.returncode} while running 'uvx ruff {operation}' on {filepath}"
            )
            if e.stderr:
                LOGGER.debug(f"stderr: {e.stderr}")
        except OSError as e:
            LOGGER.error(f"OS error while running 'uvx ruff {operation}' on {filepath}: {e}")
        except Exception as e:
            LOGGER.error(f"Unexpected error while running 'uvx ruff {operation}' on {filepath}: {e}")

    # Execute ruff operations in sequence
    for operation in ("format", "check"):
        run_ruff_operation(operation=operation, filepath=filepath)
