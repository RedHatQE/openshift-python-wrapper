"""Core generation logic for resource classes."""

import filecmp
import os
import shlex
import sys
from pathlib import Path
from typing import Any

from pyhelper_utils.shell import run_command
from rich.console import Console
from rich.syntax import Syntax
from simple_logger.logger import get_logger

from class_generator.constants import RESOURCES_MAPPING_FILE, TESTS_MANIFESTS_DIR
from class_generator.core.schema import read_resources_mapping_file, update_kind_schema
from class_generator.formatters.file_writer import write_and_format_rendered
from class_generator.formatters.template_renderer import render_jinja_template
from class_generator.parsers.explain_parser import parse_explain
from class_generator.parsers.user_code_parser import parse_user_code_from_file
from ocp_resources.utils.utils import convert_camel_case_to_snake_case

LOGGER = get_logger(name=__name__)


def generate_resource_file_from_dict(
    resource_dict: dict[str, Any],
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    add_tests: bool = False,
    output_file_suffix: str = "",
    output_dir: str = "",
) -> tuple[str, str]:
    """
    Generate a Python file from a resource dictionary.

    Args:
        resource_dict: Dictionary containing resource information
        overwrite: Whether to overwrite existing files
        dry_run: If True, only print the output without writing
        output_file: Specific output file path
        add_tests: Whether to generate test files
        output_file_suffix: Suffix to add to the output filename
        output_dir: Output directory (defaults to "ocp_resources")

    Returns:
        Tuple of (original_filename, generated_filename)
    """
    base_dir = output_dir or "ocp_resources"
    os.makedirs(base_dir, exist_ok=True)

    rendered = render_jinja_template(
        template_dict=resource_dict,
        template_dir="class_generator/manifests",
        template_name="class_generator_template.j2",
    )

    output = "# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md\n\n"
    formatted_kind_str = convert_camel_case_to_snake_case(name=resource_dict["kind"])
    _file_suffix: str = f"{'_' + output_file_suffix if output_file_suffix else ''}"

    if add_tests:
        overwrite = True
        tests_path = Path(TESTS_MANIFESTS_DIR) / resource_dict["kind"]
        os.makedirs(tests_path, exist_ok=True)

        _output_file = os.path.join(tests_path, f"{formatted_kind_str}{_file_suffix}.py")

    elif output_file:
        _output_file = output_file

    else:
        _output_file = os.path.join(base_dir, f"{formatted_kind_str}{_file_suffix}.py")

    _output_file_exists: bool = os.path.exists(_output_file)
    _user_code: str = ""
    _user_imports: str = ""

    if _output_file_exists and not add_tests:
        _user_code, _user_imports = parse_user_code_from_file(file_path=_output_file)

    orig_filename = _output_file
    if _output_file_exists:
        if overwrite:
            LOGGER.warning(f"Overwriting {_output_file}")

        else:
            temp_output_file = _output_file.replace(".py", "_TEMP.py")
            LOGGER.warning(f"{_output_file} already exists, using {temp_output_file}")
            _output_file = temp_output_file

    if _user_code.strip() or _user_imports.strip():
        output += f"{_user_imports}{rendered}{_user_code}"
    else:
        output += rendered

    if dry_run:
        _code = Syntax(code=output, lexer="python", line_numbers=True)
        Console().print(_code)

    else:
        write_and_format_rendered(filepath=_output_file, output=output)

    return orig_filename, _output_file


def class_generator(
    kind: str,
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    output_dir: str = "",
    add_tests: bool = False,
    called_from_cli: bool = True,
    update_schema_executed: bool = False,
) -> list[str]:
    """
    Generates a class for a given Kind.

    Args:
        kind: Kubernetes resource kind
        overwrite: Whether to overwrite existing files
        dry_run: If True, only print the output without writing
        output_file: Specific output file path
        output_dir: Output directory
        add_tests: Whether to generate test files
        called_from_cli: Whether called from CLI (enables prompts)
        update_schema_executed: Whether schema update was already executed

    Returns:
        List of generated file paths
    """
    LOGGER.info(f"Generating class for {kind}")
    kind = kind.lower()
    kind_and_namespaced_mappings = read_resources_mapping_file().get(kind)
    if not kind_and_namespaced_mappings:
        if called_from_cli:
            if update_schema_executed:
                LOGGER.error(f"{kind} not found in {RESOURCES_MAPPING_FILE} after update-schema executed.")
                sys.exit(1)

            # Use a loop to handle retries instead of recursion
            max_retries = 3
            retry_count = 0

            while retry_count < max_retries:
                # Validate user input with a loop
                while True:
                    run_update_schema = (
                        input(
                            f"{kind} not found in {RESOURCES_MAPPING_FILE}, Do you want to run --update-schema and retry? [Y/N]: "
                        )
                        .strip()
                        .lower()
                    )

                    if run_update_schema in ["y", "n"]:
                        break
                    else:
                        print("Invalid input. Please enter 'Y' or 'N'.")

                if run_update_schema == "n":
                    sys.exit(1)

                # User chose 'y' - update schema and retry
                LOGGER.info(f"Updating schema (attempt {retry_count + 1}/{max_retries})...")
                update_kind_schema()

                # Re-read the mapping file to check if kind is now available
                kind_and_namespaced_mappings = read_resources_mapping_file().get(kind)
                if kind_and_namespaced_mappings:
                    # Kind found, break out of retry loop to continue processing
                    break
                else:
                    retry_count += 1
                    if retry_count < max_retries:
                        LOGGER.warning(
                            f"{kind} still not found after schema update. Retry {retry_count}/{max_retries}."
                        )
                    else:
                        LOGGER.error(
                            f"{kind} not found in {RESOURCES_MAPPING_FILE} after {max_retries} update-schema attempts."
                        )
                        sys.exit(1)

        else:
            LOGGER.error(f"{kind} not found in {RESOURCES_MAPPING_FILE}, Please run --update-schema.")
            return []

    resources = parse_explain(kind=kind)

    # Check if we have resources from different API groups
    unique_groups = set()
    for resource in resources:
        # Use the original group name that we stored
        if "original_group" in resource and resource["original_group"]:
            unique_groups.add(resource["original_group"])

    use_output_file_suffix: bool = len(unique_groups) > 1
    generated_files: list[str] = []
    for resource_dict in resources:
        # Use the lowercase version of the original group name for suffix
        output_file_suffix = ""
        if use_output_file_suffix and "original_group" in resource_dict and resource_dict["original_group"]:
            output_file_suffix = resource_dict["original_group"].lower().replace(".", "_").replace("-", "_")

        orig_filename, generated_py_file = generate_resource_file_from_dict(
            resource_dict=resource_dict,
            overwrite=overwrite,
            dry_run=dry_run,
            output_file=output_file,
            add_tests=add_tests,
            output_file_suffix=output_file_suffix,
            output_dir=output_dir,
        )

        if not dry_run:
            try:
                rc, stdout, stderr = run_command(
                    command=shlex.split(f"uvx pre-commit run --files {generated_py_file}"),
                    verify_stderr=False,
                    check=False,
                )
                # Check if the command failed
                if not rc:
                    LOGGER.warning(
                        f"Pre-commit hooks failed for {generated_py_file}. "
                        f"This is non-fatal and generation will continue."
                    )
                    if stderr:
                        LOGGER.debug(f"Pre-commit stderr: {stderr}")
                    if stdout:
                        LOGGER.debug(f"Pre-commit stdout: {stdout}")
            except Exception as e:
                LOGGER.error(
                    f"Failed to run pre-commit hooks for {generated_py_file}: {e}. "
                    f"This is non-fatal and generation will continue."
                )

            if orig_filename != generated_py_file and filecmp.cmp(orig_filename, generated_py_file):
                LOGGER.warning(f"File {orig_filename} was not updated, deleting {generated_py_file}")
                Path.unlink(Path(generated_py_file))

        generated_files.append(generated_py_file)

    return generated_files
