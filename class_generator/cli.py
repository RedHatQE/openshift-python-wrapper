"""Command-line interface for the class generator."""

import fnmatch
import shutil
import sys
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
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
from class_generator.core.schema import update_kind_schema
from class_generator.tests.test_generation import generate_class_generator_tests

LOGGER = get_logger(name=__name__)


@cloup.command("Resource class generator", show_constraints=True)
@cloup.option(
    "-k",
    "--kind",
    type=cloup.STRING,
    help="""
    \b
    The Kind to generate the class for, Needs working cluster with admin privileges.
    multiple kinds can be sent separated by comma (without psaces)
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
) -> None:
    """Generate Python module for K8S resource."""
    # Check that at least one action is specified
    actions = [kind, update_schema, discover_missing, coverage_report, generate_missing, regenerate_all]
    if not any(actions):
        LOGGER.error(
            "At least one action must be specified (--kind, --update-schema, --discover-missing, --coverage-report, --generate-missing, or --regenerate-all)"
        )
        sys.exit(1)

    # Handle schema update - either standalone or with --generate-missing
    if update_schema:
        LOGGER.info("Updating resource schema...")
        update_kind_schema()

        # If only updating schema (not generating), exit
        if not generate_missing:
            return

        LOGGER.info("Schema updated. Proceeding with resource generation...")

    # Analyze coverage (now based on schema mapping, not cluster discovery)
    coverage_analysis = analyze_coverage()

    # Generate report if requested
    if coverage_report or discover_missing or generate_missing:
        output_format = "json" if json_output else None
        report = generate_report(coverage_data=coverage_analysis, output_format=output_format)
        if report is not None:  # Only print if report is not None (json format)
            print(report)

    # Generate missing resources if requested
    if generate_missing and coverage_analysis["missing_resources"]:
        LOGGER.info(f"Generating {len(coverage_analysis['missing_resources'])} missing resources...")
        for resource_kind in coverage_analysis["missing_resources"]:
            if isinstance(resource_kind, dict):
                kind_to_generate = resource_kind.get("kind", resource_kind)
            else:
                kind_to_generate = resource_kind

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
                LOGGER.error(f"Failed to generate {kind_to_generate}: {e}")

    # Handle --regenerate-all option
    if regenerate_all:
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
        if filter:
            filtered = []
            for resource in discovered:
                if fnmatch.fnmatch(resource["kind"], filter):
                    filtered.append(resource)
            discovered = filtered
            LOGGER.info(f"Filtered to {len(discovered)} resources matching '{filter}'")

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
                if backup_dir:
                    # Preserve directory structure in backup
                    resource_path = Path(resource_file)
                    if resource_path.is_absolute():
                        try:
                            relative_path = resource_path.relative_to(Path.cwd())
                        except ValueError:
                            # File is outside current directory, use just the filename
                            relative_path = Path(resource_path.name)
                    else:
                        # Path is already relative, use as-is
                        relative_path = resource_path
                    backup_path = backup_dir / relative_path
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(resource_file, backup_path)
                    LOGGER.info(f"Backed up {resource_file}")

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
                LOGGER.error(f"Failed to regenerate {resource_kind}: {e}")
                return resource_kind, False, str(e)

        # Process resources in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all tasks
            regeneration_futures = {
                executor.submit(regenerate_single_resource, resource): resource for resource in discovered
            }

            # Process results as they complete
            for future in as_completed(regeneration_futures):
                resource_kind, success, error = future.result()
                if success:
                    success_count += 1
                else:
                    error_count += 1

        # Print summary
        if not dry_run:
            LOGGER.info(f"\nRegeneration complete: {success_count} succeeded, {error_count} failed")
            if backup_dir:
                LOGGER.info(f"Backup files stored in: {backup_dir}")
        else:
            LOGGER.info(f"\nDry run complete: would regenerate {len(discovered)} resources")

        return

    # Exit if we only did discovery/report/generation
    if discover_missing or coverage_report or generate_missing:
        return

    # Handle normal generation with -k/--kind option
    if not kind:
        LOGGER.error("No kind specified for generation")
        return

    # Handle add_tests option with kind
    if add_tests:
        generate_class_generator_tests()
        return

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
                from ocp_resources.utils.utils import convert_camel_case_to_snake_case

                formatted_kind = convert_camel_case_to_snake_case(name=kind)
                target_file = Path("ocp_resources") / f"{formatted_kind}.py"

            # Create backup if file exists
            if target_file.exists():
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

        class_generator(
            kind=kind,
            overwrite=overwrite,
            dry_run=dry_run,
            output_file=output_file,
            add_tests=add_tests,
        )

        if backup_dir and not dry_run:
            LOGGER.info(f"Backup files stored in: {backup_dir}")
    else:
        # Multiple kinds - run in parallel
        def generate_with_backup(kind_to_generate: str) -> list[str]:
            """Generate a single kind with optional backup."""
            if overwrite and backup_dir:
                # Determine the output file path for this kind
                from ocp_resources.utils.utils import convert_camel_case_to_snake_case

                formatted_kind = convert_camel_case_to_snake_case(name=kind_to_generate)
                target_file = Path("ocp_resources") / f"{formatted_kind}.py"

                # Create backup if file exists
                if target_file.exists():
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

            return class_generator(
                kind=kind_to_generate,
                overwrite=overwrite,
                dry_run=dry_run,
                output_file=output_file,
                add_tests=add_tests,
            )

        futures: list[Future] = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for _kind in kind_list:
                futures.append(executor.submit(generate_with_backup, _kind))

            # Wait for all tasks to complete
            for _ in as_completed(futures):
                pass

        if backup_dir and not dry_run:
            LOGGER.info(f"Backup files stored in: {backup_dir}")


if __name__ == "__main__":
    main()
