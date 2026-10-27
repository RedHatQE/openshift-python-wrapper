"""Core generation logic for resource classes."""

import filecmp
import os
import re
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.syntax import Syntax
from simple_logger.logger import get_logger

from class_generator.constants import RESOURCES_MAPPING_FILE, TESTS_MANIFESTS_DIR
from class_generator.core.schema import read_resources_mapping_file, update_kind_schema
from class_generator.formatters.file_writer import verify_rendered, write_and_format_rendered
from class_generator.formatters.template_renderer import render_jinja_template
from class_generator.parsers.explain_parser import parse_explain
from class_generator.parsers.user_code_parser import parse_user_code_from_file
from ocp_resources.utils.utils import convert_camel_case_to_snake_case

LOGGER = get_logger(name=__name__)


GENERATED_FILES_HEADER = (
    "# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md"
)


def generate_resource_file_from_dict(
    resource_dict: dict[str, Any],
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    add_tests: bool = False,
    output_file_suffix: str = "",
    output_dir: str = "",
    verify: bool = False,
) -> tuple[str, str | list[str] | None]:
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
        verify: If True, verify the existing file matches the rendered output
            without writing anything

    Returns:
        Tuple of (original_filename, generated_filename). In verify mode,
        generated_filename is the original filename on match, or the list of
        drift categories when a drift (or a missing file) is detected.
    """
    base_dir = output_dir or "ocp_resources"
    os.makedirs(base_dir, exist_ok=True)

    rendered = render_jinja_template(
        template_dict=resource_dict,
        template_dir="class_generator/manifests",
        template_name="class_generator_template.j2",
    )

    output = f"{GENERATED_FILES_HEADER}\n\n"
    formatted_kind_str = convert_camel_case_to_snake_case(name=resource_dict["kind"])

    if re.search(r"_[a-z]_", formatted_kind_str):
        msg = (
            f"'{resource_dict['kind']}' produced invalid filename '{formatted_kind_str}.py'.\n"
            f"Add '{resource_dict['kind']}' acronym to 'normalize_acronyms' dict in:\n"
            f"  ocp_resources/utils/utils.py -> convert_camel_case_to_snake_case()"
        )
        LOGGER.error(msg)
        raise ValueError(msg)

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

    if _output_file_exists and not add_tests and not verify:
        # Only class-generator output may be overwritten: a hand-maintained resource
        # has no generated header and no end-of-generated-code marker, so rewriting
        # it silently deletes the hand-written implementation
        _existing_content = Path(_output_file).read_text(encoding="utf-8")
        if GENERATED_FILES_HEADER not in _existing_content:
            raise RuntimeError(
                f"{_output_file} is not a class-generator generated file "
                f"(missing the generated header). Refusing to overwrite a hand-maintained "
                f"resource - exclude its kind from the regeneration command."
            )

    if _output_file_exists and not add_tests:
        _user_code, _user_imports = parse_user_code_from_file(file_path=_output_file)

    orig_filename = _output_file
    if _output_file_exists and not verify:
        if overwrite:
            LOGGER.warning(f"Overwriting {_output_file}")

        else:
            if not dry_run:
                temp_output_file = _output_file.replace(".py", "_TEMP.py")
                LOGGER.warning(f"{_output_file} already exists, using {temp_output_file}")
                _output_file = temp_output_file

    if _user_code.strip() or _user_imports.strip():
        output += f"{_user_imports}{rendered}{_user_code}"
    else:
        output += rendered

    if verify:
        drift_categories = verify_rendered(filepath=_output_file, output=output)
        if drift_categories is None:
            return orig_filename, orig_filename

        LOGGER.error(f"Drift detected: {_output_file} does not match class-generator output")
        return orig_filename, drift_categories

    if dry_run:
        console = Console()
        console.print(f"\n[bold green]Would create file:[/bold green] {_output_file}")
        _code = Syntax(code=output, lexer="python", line_numbers=True)
        console.print(_code)

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
    called_from_test: bool = False,
    verify: bool = False,
) -> list[str] | list[tuple[str, list[str]]]:
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
        List of generated file paths. When verify=True, returns a list of
        (drifted_file_path, drift_categories) tuples, empty when all files
        match the generator output.
    """
    LOGGER.info(f"Generating class for {kind}")
    kind = kind.lower()
    kind_and_namespaced_mappings = read_resources_mapping_file().get(kind)
    if not called_from_test and not kind_and_namespaced_mappings:
        if called_from_cli:
            if update_schema_executed:
                error_msg = f"{kind} not found in {RESOURCES_MAPPING_FILE} after update-schema executed."
                LOGGER.error(error_msg)
                raise RuntimeError(error_msg)

            run_update_schema = (
                input(
                    f"{kind} not found in {RESOURCES_MAPPING_FILE}, Do you want to run --update-schema and retry? [Y/N]: "
                )
                .strip()
                .lower()
            )

            if run_update_schema != "y":
                raise RuntimeError(f"User declined to update schema for {kind}")

            # User chose 'y' - update schema and retry
            LOGGER.info("Updating schema")
            try:
                update_kind_schema()
            except (OSError, RuntimeError) as e:
                error_msg = f"Failed to update schema: {e}"
                LOGGER.error(error_msg)
                raise RuntimeError(error_msg) from e

            # Re-read the mapping file to check if kind is now available
            kind_and_namespaced_mappings = read_resources_mapping_file(skip_cache=True).get(kind)
            if kind_and_namespaced_mappings:
                return class_generator(
                    kind=kind,
                    overwrite=overwrite,
                    dry_run=dry_run,
                    output_file=output_file,
                    output_dir=output_dir,
                    add_tests=add_tests,
                    called_from_cli=called_from_cli,
                    update_schema_executed=True,
                )
            else:
                error_msg = f"{kind} not found in {RESOURCES_MAPPING_FILE} after update-schema attempt."
                LOGGER.error(error_msg)
                raise RuntimeError(error_msg)

        else:
            error_msg = f"{kind} not found in {RESOURCES_MAPPING_FILE}, Please run --update-schema."
            if verify:
                # A kind that cannot be found in the schema mapping cannot be verified;
                # failing loudly beats silently reporting it as clean
                raise RuntimeError(error_msg)
            LOGGER.error(error_msg)
            return []

    resources = parse_explain(kind=kind)

    # Check if we have resources from different API groups
    unique_groups = set()
    for resource in resources:
        # Use the original group name that we stored; the core group ("") counts
        # as a group too, so a kind existing in core and one other group gets
        # suffix-based file separation instead of resources overwriting each other
        unique_groups.add(resource.get("original_group") or "")

    use_output_file_suffix: bool = len(unique_groups) > 1
    drifted_files: list[tuple[str, list[str]]] = []
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
            verify=verify,
        )

        if verify:
            if isinstance(generated_py_file, list):
                drifted_files.append((orig_filename, generated_py_file))
            continue

        # In verify mode the loop continues above, so the file is always a str here
        assert isinstance(generated_py_file, str)

        if not dry_run and not called_from_test:
            if orig_filename != generated_py_file and filecmp.cmp(orig_filename, generated_py_file):
                LOGGER.warning(f"File {orig_filename} was not updated, deleting {generated_py_file}")
                Path.unlink(Path(generated_py_file))

        generated_files.append(generated_py_file)

    if verify:
        return drifted_files

    return generated_files
