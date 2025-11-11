"""Command-line interface for the class generator."""

import fnmatch
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import cloup
from cloup.constraints import If, IsSet, accept_none, require_one
from simple_logger.logger import get_logger

from class_generator.constants import TESTS_MANIFESTS_DIR
from class_generator.core.coverage import analyze_coverage, generate_report
from class_generator.core.discovery import discover_generated_resources
from class_generator.core.generator import class_generator
from class_generator.core.schema import ClusterVersionError, update_kind_schema
from class_generator.tests.test_generation import generate_class_generator_tests
from class_generator.utils import execute_parallel_tasks
from ocp_resources.utils.utils import convert_camel_case_to_snake_case

LOGGER = get_logger(name=__name__)


def validate_actions(
    kind: str | None,
    update_schema: bool,
    discover_missing: bool,
    coverage_report: bool,
    generate_missing: bool,
    regenerate_all: bool,
) -> None:
    """Validate that at least one action is specified."""
    actions = [kind, update_schema, discover_missing, coverage_report, generate_missing, regenerate_all]
    if not any(actions):
        LOGGER.error(
            "At least one action must be specified (--kind, --update-schema, --discover-missing, --coverage-report, --generate-missing, or --regenerate-all)"
        )
        sys.exit(1)


def handle_schema_update(update_schema: bool, generate_missing: bool) -> bool:
    """
    Handle schema update operations.

    Args:
        update_schema: Whether to update the schema
        generate_missing: Whether to generate missing resources after update

    Returns:
        True if processing should continue, False if it should exit
    """
    if update_schema:
        LOGGER.info("Updating resource schema...")
        try:
            update_kind_schema()
        except (OSError, RuntimeError, ClusterVersionError) as e:
            LOGGER.exception(f"Failed to update schema: {e}")
            sys.exit(1)

        # If only updating schema (not generating), exit
        if not generate_missing:
            return False

        LOGGER.info("Schema updated. Proceeding with resource generation...")

    return True


def handle_coverage_analysis_and_reporting(
    coverage_report: bool,
    discover_missing: bool,
    generate_missing: bool,
    json_output: bool,
) -> dict[str, Any]:
    """
    Handle coverage analysis and reporting.

    Args:
        coverage_report: Whether to generate a coverage report
        discover_missing: Whether to discover missing resources
        generate_missing: Whether to generate missing resources
        json_output: Whether to output in JSON format

    Returns:
        Coverage analysis data
    """
    # Analyze coverage (now based on schema mapping, not cluster discovery)
    coverage_analysis = analyze_coverage()

    # Generate report if requested
    if coverage_report or discover_missing or generate_missing:
        output_format = "json" if json_output else None
        report = generate_report(coverage_data=coverage_analysis, output_format=output_format)
        if report is not None:  # Only print if report is not None (json format)
            print(report)

    return coverage_analysis


def handle_missing_resources_generation(
    generate_missing: bool,
    coverage_analysis: dict[str, Any],
    overwrite: bool,
    dry_run: bool,
) -> None:
    """
    Handle generation of missing resources.

    Args:
        generate_missing: Whether to generate missing resources
        coverage_analysis: Coverage analysis data containing missing resources
        overwrite: Whether to overwrite existing files
        dry_run: Whether this is a dry run
    """
    if generate_missing and coverage_analysis["missing_resources"]:
        LOGGER.info(f"Generating {len(coverage_analysis['missing_resources'])} missing resources...")
        for resource_kind in coverage_analysis["missing_resources"]:
            # Extract kind from dict (missing_resources entries are now always dicts)
            kind_to_generate = resource_kind["kind"]

            try:
                class_generator(
                    kind=kind_to_generate,
                    output_file="",
                    overwrite=overwrite,
                    add_tests=False,
                    dry_run=dry_run,
                )
                if not dry_run:
                    LOGGER.info(f"Generated {kind_to_generate}")
            except Exception as e:
                LOGGER.exception(f"Failed to generate {kind_to_generate}: {e}")


def create_backup_if_needed(target_file: Path, backup_dir: Path | None) -> None:
    """
    Create a backup of the target file if backup_dir is set and file exists.

    Args:
        target_file: The file to backup
        backup_dir: The directory where backups should be stored
    """
    if backup_dir and target_file.exists():
        # Preserve directory structure in backup
        if target_file.is_absolute():
            try:
                relative_path = target_file.relative_to(Path.cwd())
            except ValueError:
                # File is outside current directory, use just the filename
                relative_path = Path(target_file.name)
        else:
            # Path is already relative, use as-is
            relative_path = target_file
        backup_path = backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target_file, backup_path)
        LOGGER.info(f"Backed up {target_file}")


def handle_regenerate_all(
    regenerate_all: bool,
    backup: bool,
    dry_run: bool,
    filter_pattern: str | None,
) -> bool:
    """
    Handle regeneration of all generated resources.

    Args:
        regenerate_all: Whether to regenerate all resources
        backup: Whether to create backups
        dry_run: Whether this is a dry run
        filter_pattern: Optional filter pattern for resource names

    Returns:
        True if regeneration was performed and main should exit, False to continue
    """
    if not regenerate_all:
        return False

    LOGGER.info("Starting batch regeneration of all generated resources...")

    # Create backup if requested
    backup_dir = None
    if backup and not dry_run:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_root = Path(".backups")
        backup_root.mkdir(exist_ok=True)
        backup_dir = backup_root / f"backup-{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        LOGGER.info(f"Creating backup in {backup_dir}")

    # Discover all generated resources
    discovered = discover_generated_resources()
    LOGGER.info(f"Found {len(discovered)} generated resources")

    # Filter resources if pattern provided
    if filter_pattern:
        filtered = []
        for resource in discovered:
            if fnmatch.fnmatch(resource["kind"], filter_pattern):
                filtered.append(resource)
        discovered = filtered
        LOGGER.info(f"Filtered to {len(discovered)} resources matching '{filter_pattern}'")

    # Regenerate each resource
    success_count = 0
    error_count = 0

    # Define function to process a single resource
    def regenerate_single_resource(resource: dict[str, Any]) -> tuple[str, bool, str | None]:
        """
        Regenerate a single resource.

        Returns:
            Tuple of (resource_kind, success, error_message)
        """
        resource_kind = resource["kind"]
        resource_file = resource["path"]

        try:
            LOGGER.info(f"Regenerating {resource_kind}...")

            # Create backup of original file if requested
            create_backup_if_needed(target_file=Path(resource_file), backup_dir=backup_dir)

            # Regenerate the resource
            result = class_generator(
                kind=resource_kind,
                overwrite=True,  # Always overwrite in regenerate mode
                dry_run=dry_run,
                output_file=resource_file,
                add_tests=False,
                called_from_cli=False,  # Don't prompt for missing resources during batch regeneration
            )

            # Check if generation was successful (empty list means failure)
            if result:
                if not dry_run:
                    LOGGER.info(f"Successfully regenerated {resource_kind}")
                return resource_kind, True, None
            else:
                LOGGER.warning(f"Skipped {resource_kind}: Not found in schema mapping")
                return resource_kind, False, "Not found in schema mapping"
        except Exception as e:
            LOGGER.exception(f"Failed to regenerate {resource_kind}: {e}")
            return resource_kind, False, str(e)

    # Process results from parallel execution
    def process_regeneration_result(_resource: dict[str, Any], result: tuple[str, bool, str | None]) -> None:
        nonlocal success_count, error_count
        _resource_kind, success, _error = result
        if success:
            success_count += 1
        else:
            error_count += 1

    # Handle executor-level exceptions that bypass result processing
    def handle_regeneration_error(resource: dict[str, Any], exc: Exception) -> None:
        nonlocal error_count
        resource_kind = resource.get("kind", "unknown")
        LOGGER.exception(f"Executor-level failure for {resource_kind}: {exc}")
        error_count += 1

    # Process resources in parallel
    execute_parallel_tasks(
        tasks=discovered,
        task_func=regenerate_single_resource,
        max_workers=10,
        task_name="regeneration",
        result_processor=process_regeneration_result,
        error_handler=handle_regeneration_error,
    )

    # Print summary
    if not dry_run:
        LOGGER.info(f"\nRegeneration complete: {success_count} succeeded, {error_count} failed")
        if backup_dir:
            LOGGER.info(f"Backup files stored in: {backup_dir}")
    else:
        LOGGER.info(f"\nDry run complete: would regenerate {len(discovered)} resources")

    return True


def handle_normal_kind_generation(
    kind: str,
    overwrite: bool,
    output_file: str,
    dry_run: bool,
    add_tests: bool,
    backup: bool,
) -> None:
    """
    Handle normal kind generation with -k/--kind option.

    Args:
        kind: Comma-separated list of kinds to generate
        overwrite: Whether to overwrite existing files
        output_file: Optional output file path
        dry_run: Whether this is a dry run
        add_tests: Whether to add tests
        backup: Whether to create backups
    """
    # Generate class files for specified kinds
    kind_list: list[str] = kind.split(",")

    # Create backup directory if backup is requested with overwrite
    backup_dir = None
    if backup and overwrite and not dry_run:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_root = Path(".backups")
        backup_root.mkdir(exist_ok=True)
        backup_dir = backup_root / f"backup-{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        LOGGER.info(f"Creating backup in {backup_dir}")

    if len(kind_list) == 1:
        # Single kind - run directly
        # First get the output file path to check if it exists
        if overwrite and backup_dir:
            # Determine the output file path
            if output_file:
                target_file = Path(output_file)
            else:
                # Default output path based on kind
                formatted_kind = convert_camel_case_to_snake_case(name=kind)
                target_file = Path("ocp_resources") / f"{formatted_kind}.py"

            # Create backup if file exists
            create_backup_if_needed(target_file=target_file, backup_dir=backup_dir)

        try:
            class_generator(
                kind=kind,
                overwrite=overwrite,
                dry_run=dry_run,
                output_file=output_file,
                add_tests=add_tests,
            )
        except Exception as e:
            LOGGER.exception(f"Failed to generate {kind}: {e}")
            sys.exit(1)

        if backup_dir and not dry_run:
            LOGGER.info(f"Backup files stored in: {backup_dir}")
    else:
        # Multiple kinds - run in parallel with result tracking
        success_count = 0
        error_count = 0
        failed_kinds = []

        def generate_with_backup(kind_to_generate: str) -> tuple[str, bool, str | None]:
            """
            Generate a single kind with optional backup.

            Returns:
                Tuple of (kind, success, error_message)
            """
            if overwrite and backup_dir:
                # Determine the output file path for this kind
                formatted_kind = convert_camel_case_to_snake_case(name=kind_to_generate)
                target_file = Path("ocp_resources") / f"{formatted_kind}.py"

                # Create backup if file exists
                create_backup_if_needed(target_file=target_file, backup_dir=backup_dir)

            try:
                result = class_generator(
                    kind=kind_to_generate,
                    overwrite=overwrite,
                    dry_run=dry_run,
                    output_file=output_file,
                    add_tests=add_tests,
                    called_from_cli=False,  # Don't prompt for missing resources during batch generation
                )
                # Check if generation was successful (empty list means failure)
                if result:
                    if not dry_run:
                        LOGGER.info(f"Successfully generated {kind_to_generate}")
                    return kind_to_generate, True, None
                else:
                    LOGGER.warning(f"Skipped {kind_to_generate}: Not found in schema mapping")
                    return kind_to_generate, False, "Not found in schema mapping"
            except Exception as e:
                LOGGER.exception(f"Failed to generate {kind_to_generate}: {e}")
                return kind_to_generate, False, str(e)

        # Process results from parallel execution
        def process_generation_result(_kind_to_generate: str, result: tuple[str, bool, str | None]) -> None:
            nonlocal success_count, error_count, failed_kinds
            kind_name, success, error = result
            if success:
                success_count += 1
            else:
                error_count += 1
                failed_kinds.append({"kind": kind_name, "error": error})

        # Handle executor-level exceptions that bypass result processing
        def handle_generation_error(kind_to_generate: str, exc: Exception) -> None:
            nonlocal error_count, failed_kinds
            LOGGER.exception(f"Executor-level failure for {kind_to_generate}: {exc}")
            error_count += 1
            failed_kinds.append({"kind": kind_to_generate, "error": str(exc)})

        # Generate all kinds in parallel
        execute_parallel_tasks(
            tasks=kind_list,
            task_func=generate_with_backup,
            max_workers=10,
            task_name="generation",
            result_processor=process_generation_result,
            error_handler=handle_generation_error,
        )

        # Print summary and handle failures
        if not dry_run:
            LOGGER.info(f"\nGeneration complete: {success_count} succeeded, {error_count} failed")
            if backup_dir:
                LOGGER.info(f"Backup files stored in: {backup_dir}")
        else:
            LOGGER.info(f"\nDry run complete: would generate {len(kind_list)} kinds")

        # Log detailed failure information
        if failed_kinds:
            LOGGER.error(f"\nFailed to generate {len(failed_kinds)} kind(s):")
            for failure in failed_kinds:
                LOGGER.error(f"  - {failure['kind']}: {failure['error']}")

            # Exit with non-zero status if any failures occurred
            sys.exit(1)


def handle_test_generation(add_tests: bool) -> None:
    """
    Handle test generation and execution.

    Args:
        add_tests: Whether to generate and run tests
    """
    if add_tests:
        generate_class_generator_tests()

        # Run the generated test file
        LOGGER.info("Running generated tests...")
        test_file = "class_generator/tests/test_class_generator.py"
        exit_code = os.system(f"uv run pytest {test_file}")

        # os.system returns the exit status shifted left by 8 bits
        if exit_code != 0:
            LOGGER.error(f"Tests failed with exit code {exit_code >> 8}")


@cloup.command("Resource class generator", show_constraints=True)
@cloup.option(
    "-k",
    "--kind",
    type=cloup.STRING,
    help="""
    \b
    The Kind to generate the class for, Needs working cluster with admin privileges.
    multiple kinds can be sent separated by comma (without spaces)
    Example: -k Deployment,Pod,ConfigMap
""",
)
@cloup.option(
    "-o",
    "--output-file",
    help="The full filename path to generate a python resource file. If not sent, resource kind will be used",
    type=cloup.Path(),
)
@cloup.option(
    "--overwrite",
    is_flag=True,
    help="Output file overwrite existing file if passed",
)
@cloup.option("--dry-run", is_flag=True, help="Run the script without writing to file")
@cloup.option(
    "--add-tests",
    help=f"Add a test to `test_class_generator.py` and test files to `{TESTS_MANIFESTS_DIR}` dir",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--update-schema",
    help="Update kind schema files",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--discover-missing",
    help="Discover resources in the cluster that don't have wrapper classes",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--coverage-report",
    help="Generate a coverage report of implemented vs discovered resources",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--json",
    "json_output",
    help="Output reports in JSON format",
    is_flag=True,
    default=False,
    show_default=True,
)
@cloup.option(
    "--generate-missing",
    help="Generate classes for all missing resources after discovery",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--regenerate-all",
    help="Regenerate all existing generated resource classes with latest schemas",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--backup",
    help="Create timestamped backup before regeneration or overwriting files",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--filter",
    help="Filter resources to regenerate using glob pattern (e.g., 'Pod*', '*Service')",
    type=cloup.STRING,
    default=None,
)
@cloup.option(
    "-v",
    "--verbose",
    help="Enable verbose output with debug logs",
    is_flag=True,
    show_default=True,
)
@cloup.constraint(
    If(IsSet("update_schema") & ~IsSet("generate_missing"), then=accept_none),
    [
        "kind",
        "discover_missing",
        "coverage_report",
        "dry_run",
        "overwrite",
        "output_file",
        "add_tests",
        "regenerate_all",
    ],
)
@cloup.constraint(
    If(IsSet("backup"), then=require_one),
    ["regenerate_all", "overwrite"],
)
@cloup.constraint(
    If(IsSet("filter"), then=require_one),
    ["regenerate_all"],
)
def main(
    kind: str | None,
    overwrite: bool,
    output_file: str,
    dry_run: bool,
    add_tests: bool,
    discover_missing: bool,
    coverage_report: bool,
    generate_missing: bool,
    regenerate_all: bool,
    backup: bool,
    filter: str | None,
    json_output: bool,
    update_schema: bool,
    verbose: bool,
) -> None:
    """Generate Python module for K8S resource."""
    # Configure logging based on verbose flag
    if verbose:
        # Set debug level for all class_generator modules
        for logger_name in [
            "class_generator.core.schema",
            "class_generator.core.generator",
            "class_generator.core.coverage",
            "class_generator.core.discovery",
            "class_generator.cli",
            "class_generator.utils",
            "ocp_resources",
        ]:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            # Prevent propagation to avoid duplicate messages
            logger.propagate = False
            # Also set all handlers to DEBUG to ensure debug logs surface
            for handler in logger.handlers:
                handler.setLevel(logging.DEBUG)

        # Set root logger to DEBUG to cover all configured handlers
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        for handler in root_logger.handlers:
            handler.setLevel(logging.DEBUG)

    # Validate input parameters
    validate_actions(
        kind=kind,
        update_schema=update_schema,
        discover_missing=discover_missing,
        coverage_report=coverage_report,
        generate_missing=generate_missing,
        regenerate_all=regenerate_all,
    )

    # Handle schema update
    if not handle_schema_update(update_schema=update_schema, generate_missing=generate_missing):
        return

    # Handle coverage analysis and reporting
    coverage_analysis = handle_coverage_analysis_and_reporting(
        coverage_report=coverage_report,
        discover_missing=discover_missing,
        generate_missing=generate_missing,
        json_output=json_output,
    )

    # Handle missing resources generation
    handle_missing_resources_generation(
        generate_missing=generate_missing,
        coverage_analysis=coverage_analysis,
        overwrite=overwrite,
        dry_run=dry_run,
    )

    # Handle regenerate-all operation
    if handle_regenerate_all(regenerate_all=regenerate_all, backup=backup, dry_run=dry_run, filter_pattern=filter):
        return

    # Exit if we only did discovery/report/generation
    if discover_missing or coverage_report or generate_missing:
        return

    # Handle normal generation with -k/--kind option
    if not kind:
        LOGGER.error("No kind specified for generation")
        return

    # Handle normal kind generation
    handle_normal_kind_generation(
        kind=kind,
        overwrite=overwrite,
        output_file=output_file,
        dry_run=dry_run,
        add_tests=add_tests,
        backup=backup,
    )

    # Handle test generation
    handle_test_generation(add_tests=add_tests)


if __name__ == "__main__":
    main()
