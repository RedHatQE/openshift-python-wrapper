"""Command-line interface for the class generator."""

import fnmatch
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast

import cloup
from cloup.constraints import If, IsSet, accept_none, mutually_exclusive, require_one
from pyhelper_utils.shell import run_command
from simple_logger.logger import get_logger

from class_generator.constants import TESTS_MANIFESTS_DIR, VERIFY_TEMP_FILE_PREFIX
from class_generator.core.coverage import analyze_coverage, generate_report
from class_generator.core.discovery import discover_generated_resources
from class_generator.core.generator import class_generator, generated_file_name
from class_generator.core.schema import (
    ClusterVersionError,
    read_resources_mapping_file,
    update_kind_schema,
    update_single_resource_schema,
)
from class_generator.exceptions import ResourceNotFoundError
from class_generator.formatters.file_writer import DRIFT_CATEGORIES, DRIFT_CATEGORY_DESCRIPTIONS
from class_generator.tests.test_generation import generate_class_generator_tests
from class_generator.utils import execute_parallel_tasks

LOGGER = get_logger(name=__name__)

# Resources verified in parallel: each worker renders and formats one resource
DEFAULT_VERIFY_JOBS = 10


def validate_actions(
    kind: str | None,
    update_schema: bool,
    update_schema_for: str | None,
    discover_missing: bool,
    coverage_report: bool,
    generate_missing: bool,
    regenerate_all: bool,
    verify: bool,
    verify_all: bool,
    verify_changed: bool,
) -> None:
    """Validate that at least one action is specified."""
    actions = [
        kind,
        update_schema,
        update_schema_for,
        discover_missing,
        coverage_report,
        generate_missing,
        regenerate_all,
        verify,
        verify_all,
        verify_changed,
    ]
    if not any(actions):
        LOGGER.error(
            "At least one action must be specified (--kind, --update-schema, --update-schema-for, --discover-missing, --coverage-report, --generate-missing, --regenerate-all, --verify, --verify-all, or --verify-changed)"
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


def handle_single_schema_update(update_schema_for: str | None) -> bool:
    """
    Handle single resource schema update operations.

    Args:
        update_schema_for: The kind name to update schema for, or None

    Returns:
        True if processing should continue, False if it should exit
    """
    if update_schema_for:
        LOGGER.info(f"Updating schema for single resource: {update_schema_for}")
        try:
            update_single_resource_schema(kind=update_schema_for)
        except ResourceNotFoundError as e:
            LOGGER.error(f"Resource not found: {e}")
            sys.exit(1)
        except (OSError, RuntimeError) as e:
            LOGGER.exception(f"Failed to update schema for {update_schema_for}: {e}")
            sys.exit(1)

        LOGGER.info(f"Schema updated for {update_schema_for}.")
        return False

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


def _filter_deprecated(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Filter out deprecated resource files (hand-maintained deprecation shims).

    Files carrying a deprecation warning below the generated-code marker are
    intentionally diverged from generator output and cannot be verified.

    Args:
        resources: Discovered resources

    Returns:
        Resources that are not deprecated
    """
    deprecated = [resource for resource in resources if resource.get("deprecated")]
    if deprecated:
        names = ", ".join(sorted(Path(resource["path"]).name for resource in deprecated))
        LOGGER.info(f"Skipping {len(deprecated)} deprecated resource file(s): {names}")
    return [resource for resource in resources if not resource.get("deprecated")]


def _changed_generated_resources(base: str) -> list[tuple[str, str]]:
    """
    Get generated resources changed relative to a git base ref.

    Args:
        base: Git ref to compare against (e.g. origin/main)

    Returns:
        List of (kind, path) tuples for changed generated resource files
    """
    success, stdout, stderr = run_command(
        command=["git", "diff", "--name-only", base],
        verify_stderr=False,
        check=False,
        log_errors=False,
    )
    if not success:
        LOGGER.error(
            f"Failed to get changed files against {base}: {stderr}. "
            f"Make sure the ref exists locally (git fetch origin main) or pass --base <ref>."
        )
        sys.exit(1)

    changed_paths = {line.strip() for line in stdout.splitlines() if line.strip()}
    discovered = _filter_deprecated(discover_generated_resources())
    changed_resources = [resource for resource in discovered if resource["path"] in changed_paths]

    if changed_paths and not changed_resources:
        LOGGER.info("No generated resource files were changed")

    return [(resource["kind"], resource["path"]) for resource in changed_resources]


def handle_verify(
    verify: bool,
    verify_all: bool,
    verify_changed: bool,
    kind: str | None,
    filter_pattern: str | None,
    base: str,
    classification: str | None,
    exclude: str | None,
    match_within: bool,
    jobs: int = DEFAULT_VERIFY_JOBS,
) -> bool:
    """
    Handle verification of generated resource files without modifying them.

    Args:
        verify: Whether to verify specific kinds passed via --kind
        verify_all: Whether to verify all generated resources
        verify_changed: Whether to verify only resources changed relative to the base git ref
        kind: Comma-separated list of kinds to verify
        filter_pattern: Optional filter pattern for resource names
        base: Git ref to compare against when verify_changed is set
        classification: Optional comma-separated drift classifications; when set, only
            drifted files matching them are reported and fail the run
        exclude: Optional comma-separated drift classifications; files whose drift
            contains any of them are dropped from the report, leaving only drift that
            is safe to regenerate
        match_within: When True, require the file's drift categories to be within the
            given classifications (files with additional categories are excluded);
            False means at least one of them
        jobs: Number of resources verified in parallel

    Returns:
        True if verification was performed and main should exit, False to continue
    """
    if not verify and not verify_all and not verify_changed:
        return False

    # Verify runs hundreds of prek invocations; quiet the per-command shell logs so
    # the final summary stays readable
    logging.getLogger("pyhelper_utils.shell").setLevel(logging.WARNING)

    try:
        classification_filter: set[str] = set()
        if classification:
            classification_filter = {entry.strip() for entry in classification.split(",") if entry.strip()}
            unknown = classification_filter - set(DRIFT_CATEGORIES)
            if unknown:
                LOGGER.error(
                    f"Unknown classification(s): {', '.join(sorted(unknown))}. "
                    f"Valid classifications: {', '.join(DRIFT_CATEGORIES)}"
                )
                sys.exit(1)
        elif match_within:
            LOGGER.error("--match can only be used together with --classification")
            sys.exit(1)

        exclude_filter: set[str] = set()
        if exclude:
            exclude_filter = {entry.strip() for entry in exclude.split(",") if entry.strip()}
            unknown_excluded = exclude_filter - set(DRIFT_CATEGORIES)
            if unknown_excluded:
                LOGGER.error(
                    f"Unknown classification(s) in --exclude: {', '.join(sorted(unknown_excluded))}. "
                    f"Valid classifications: {', '.join(DRIFT_CATEGORIES)}"
                )
                sys.exit(1)

        if verify_all:
            discovered = _filter_deprecated(discover_generated_resources())
            if filter_pattern:
                discovered = [resource for resource in discovered if fnmatch.fnmatch(resource["kind"], filter_pattern)]
                LOGGER.info(f"Filtered to {len(discovered)} resources matching '{filter_pattern}'")

            targets = [(resource["kind"], resource["path"]) for resource in discovered]
            LOGGER.info(f"Verifying {len(targets)} generated resources...")

        elif verify_changed:
            targets = _changed_generated_resources(base=base)
            LOGGER.info(f"Verifying {len(targets)} changed generated resource(s) against {base}...")

        else:
            # Only generated files can be verified: a hand-maintained resource has no
            # generated header, so there is nothing to compare against
            generated_by_kind: dict[str, list[str]] = {}
            for resource in discover_generated_resources():
                generated_by_kind.setdefault(resource["kind"].lower(), []).append(resource["path"])

            targets = []
            skipped_kinds = []
            for requested_kind in (kind or "").split(","):
                if not requested_kind:
                    continue
                paths = generated_by_kind.get(requested_kind.lower())
                if not paths:
                    skipped_kinds.append(requested_kind)
                    continue
                targets.extend((requested_kind, path) for path in paths)

            if skipped_kinds:
                LOGGER.info(
                    f"Skipping {len(skipped_kinds)} kind(s) that are not generated resources: {', '.join(skipped_kinds)}"
                )
            LOGGER.info(f"Verifying {len(targets)} kind(s)...")

        drift_results: list[tuple[str, list[tuple[str, list[str]]]]] = []
        failed_kinds: list[str] = []
        resources_mapping = read_resources_mapping_file()

        def verify_single_resource(
            target: tuple[str, str | None],
        ) -> tuple[str, list[tuple[str, list[str]]], str | None]:
            """
            Verify a single resource.

            Returns:
                Tuple of (kind, drifted_files_with_categories, error_message)
            """
            resource_kind, resource_file = target
            if not resources_mapping.get(resource_kind.lower()):
                # A kind absent from the resources mapping can neither be rendered nor
                # regenerated; report it as a classified drift entry instead of raising
                if resource_file:
                    return resource_kind, [(resource_file, ["not in schema"])], None

            try:
                return (
                    resource_kind,
                    cast(
                        "list[tuple[str, list[str]]]",
                        class_generator(
                            kind=resource_kind,
                            verify=True,
                            output_file=resource_file or "",
                            called_from_cli=False,
                        ),
                    ),
                    None,
                )
            except Exception as e:
                LOGGER.exception(f"Failed to verify {resource_kind}: {e}")
                return resource_kind, [], str(e)

        def process_verification_result(
            _target: tuple[str, str | None], result: tuple[str, list[tuple[str, list[str]]], str | None]
        ) -> None:
            nonlocal drift_results, failed_kinds
            _resource_kind, drifted, error = result
            if drifted:
                drift_results.append((_resource_kind, drifted))
            if error:
                failed_kinds.append(_resource_kind)

        def handle_verification_error(target: tuple[str, str | None], exc: Exception) -> None:
            nonlocal failed_kinds
            resource_kind = target[0]
            LOGGER.exception(f"Executor-level failure for {resource_kind}: {exc}")
            failed_kinds.append(resource_kind)

        execute_parallel_tasks(
            tasks=targets,
            task_func=verify_single_resource,
            max_workers=jobs,
            task_name="verification",
            result_processor=process_verification_result,
            error_handler=handle_verification_error,
        )

        # Apply the classification filter: only drifted files matching the requested
        # classifications (per match_mode) are reported and fail the run
        def classification_matches(categories: list[str]) -> bool:
            if match_within:
                # --match: the file's categories must be a subset of the requested ones —
                # files with additional classifications are excluded
                return set(categories) <= classification_filter
            return bool(classification_filter & set(categories))

        drifted_files: list[tuple[str, list[str]]] = []
        drifted_entries: list[tuple[str, str, list[str]]] = []
        drifted_kinds: set[str] = set()
        filtered_out_count = 0
        excluded_out_count = 0
        for resource_kind, drifted in drift_results:
            if classification_filter:
                matching = [(path, categories) for path, categories in drifted if classification_matches(categories)]
                filtered_out_count += len(drifted) - len(matching)
                drifted = matching
            if exclude_filter:
                kept = [(path, categories) for path, categories in drifted if not exclude_filter & set(categories)]
                excluded_out_count += len(drifted) - len(kept)
                drifted = kept
            if drifted:
                drifted_kinds.add(resource_kind)
                drifted_files.extend(drifted)
                drifted_entries.extend((resource_kind, path, categories) for path, categories in drifted)

        # Kinds absent from the schema mapping cannot be regenerated; they get their
        # own message instead of regenerate commands
        not_in_schema_kinds = {
            resource_kind
            for resource_kind, drifted in drift_results
            if resource_kind in drifted_kinds and all(categories == ["not in schema"] for _path, categories in drifted)
        }

        if drifted_files or failed_kinds:
            if drifted_files:
                print(f"\nVerification failed: {len(drifted_files)} file(s) do not match class-generator output:")
                for drifted_file, categories in drifted_files:
                    print(f"  - {drifted_file} ({', '.join(categories)})")
            # Every reported file is produced by class-generator (filenames the generator
            # cannot emit are excluded at collection), so the plain per-kind command
            # regenerates it
            regenerable_kinds = sorted(drifted_kinds - not_in_schema_kinds)
            if regenerable_kinds:
                print(
                    "These files do not match the current class-generator output. Regenerate them instead of editing manually:"
                )
                for drifted_kind in regenerable_kinds:
                    print(f"  class-generator --kind {drifted_kind} --overwrite")
                print("Or regenerate all drifted kinds at once:")
                print(f"  class-generator --kind {','.join(regenerable_kinds)} --overwrite")
            if failed_kinds:
                print(f"\nVerification failed for {len(failed_kinds)} kind(s): {', '.join(failed_kinds)}")
            if not_in_schema_kinds:
                print(
                    f"\nKinds not found in the schema mapping (cannot be verified or regenerated): "
                    f"{', '.join(sorted(not_in_schema_kinds))}. Run --update-schema from a cluster "
                    "that serves these kinds."
                )
            if filtered_out_count:
                print(
                    f"{filtered_out_count} drifted file(s) did not match --classification "
                    f"'{classification}'{' --match' if match_within else ''} and are not shown"
                )
            if excluded_out_count:
                print(f"{excluded_out_count} drifted file(s) excluded by --exclude '{exclude}' and are not shown")
            sys.exit(1)

        if filtered_out_count:
            print(
                f"{filtered_out_count} drifted file(s) did not match --classification "
                f"'{classification}'{' --match' if match_within else ''} and are not shown"
            )
        if excluded_out_count:
            print(f"{excluded_out_count} drifted file(s) excluded by --exclude '{exclude}' and are not shown")
        print(f"\nVerification passed: all {len(targets)} generated resource(s) match class-generator output")
        return True
    finally:
        # Temp files created while rendering must never survive the run
        for leftover in Path("ocp_resources").glob(f"{VERIFY_TEMP_FILE_PREFIX}*"):
            leftover.unlink(missing_ok=True)


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
                target_file = Path("ocp_resources") / generated_file_name(kind=kind)

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
                target_file = Path("ocp_resources") / generated_file_name(kind=kind_to_generate)

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
        exit_code = os.system(f"uv run --group tests pytest {test_file}")

        # os.system returns the exit status shifted left by 8 bits
        if exit_code != 0:
            LOGGER.error(f"Tests failed with exit code {exit_code >> 8}")


def _build_epilog() -> str:
    """Build the --help epilog: verification notes, drift classifications and examples."""
    width = max(len(category) for category in DRIFT_CATEGORIES)
    classifications = "\n".join(
        f"  {category:<{width}}  {DRIFT_CATEGORY_DESCRIPTIONS[category]}" for category in DRIFT_CATEGORIES
    )
    return f"""
\b
Verification:
  --verify / --verify-all / --verify-changed never modify files. On drift they
  exit 1, list each drifted file with its classifications, and print the exact
  regenerate command. Drift means the file no longer matches current generator
  output - either it was hand-edited inside the generated markers, or the
  generator/template/schema changed since it was generated.

\b
Drift classifications (--classification):
{classifications}

\b
  Without --match a file is reported when its drift contains at least one of the
  given classifications. With --match the drift must be within them: a file that
  also has other classifications is excluded. --exclude is the opposite: files
  whose drift contains any of the given classifications are dropped, leaving only
  drift that is safe to regenerate.

\b
Examples:

\b
  class-generator --kind Deployment,Pod --add-tests
      generate classes, adding tests and test manifests

\b
  class-generator --verify-changed --base origin/main
      verify files changed in this branch were produced by class-generator

\b
  class-generator --verify-all --classification "blank lines,code add" --match
      list only files whose drift is blank lines and/or code add, nothing else

\b
  class-generator --verify-all --classification "breaking change"
      find regenerations that would break callers

\b
  class-generator --verify-all --exclude "breaking change,schema incomplete"
      list only drift that is safe to regenerate
"""


@cloup.command("Resource class generator", show_constraints=False, epilog=_build_epilog())
@cloup.option_group(
    "Generation",
    cloup.option(
        "-k",
        "--kind",
        type=cloup.STRING,
        help="The Kind to generate the class for. Needs a working cluster with admin privileges. "
        "Multiple kinds can be sent separated by comma (without spaces). "
        "Example: -k Deployment,Pod,ConfigMap",
    ),
    cloup.option(
        "-o",
        "--output-file",
        help="The full filename path to generate a python resource file. If not sent, resource kind will be used",
        type=cloup.Path(),
    ),
    cloup.option(
        "--overwrite",
        is_flag=True,
        help="Output file overwrite existing file if passed",
    ),
    cloup.option("--dry-run", is_flag=True, help="Run the script without writing to file"),
    cloup.option(
        "--add-tests",
        help=f"Add a test to `test_class_generator.py` and test files to `{TESTS_MANIFESTS_DIR}` dir",
        is_flag=True,
        show_default=True,
    ),
)
@cloup.option_group(
    "Schema",
    cloup.option(
        "--update-schema",
        help="Update kind schema files",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--update-schema-for",
        type=cloup.STRING,
        help="Update schema for a single resource kind only, without affecting other resources. "
        "Useful when connected to an older cluster but needing to update a specific CRD. "
        "Example: --update-schema-for LlamaStackDistribution. "
        "Cannot be used together with --update-schema.",
    ),
)
@cloup.option_group(
    "Discovery",
    cloup.option(
        "--discover-missing",
        help="Discover resources in the cluster that don't have wrapper classes",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--coverage-report",
        help="Generate a coverage report of implemented vs discovered resources",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--generate-missing",
        help="Generate classes for all missing resources after discovery",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--json",
        "json_output",
        help="Output reports in JSON format",
        is_flag=True,
        default=False,
        show_default=True,
    ),
)
@cloup.option_group(
    "Regeneration",
    cloup.option(
        "--regenerate-all",
        help="Regenerate all existing generated resource classes with latest schemas",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--backup",
        help="Create timestamped backup before regeneration or overwriting files",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--filter",
        help="Filter resources to regenerate using glob pattern (e.g., 'Pod*', '*Service')",
        type=cloup.STRING,
        default=None,
    ),
)
@cloup.option_group(
    "Verification",
    cloup.option(
        "--verify",
        help="Verify the files for the kinds passed via --kind; no files are modified",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--verify-all",
        help="Verify all generated resources; combine with --filter to narrow the scope",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--verify-changed",
        help="Verify only resources changed vs --base; untouched files are not checked",
        is_flag=True,
        show_default=True,
    ),
    cloup.option(
        "--base",
        type=cloup.STRING,
        default="origin/main",
        show_default=True,
        help="Git ref to compare against when using --verify-changed",
    ),
    cloup.option(
        "--classification",
        type=cloup.STRING,
        default=None,
        help="Only report drift matching these classifications (comma-separated); see below",
    ),
    cloup.option(
        "--exclude",
        type=cloup.STRING,
        default=None,
        help="Drop files whose drift contains any of these classifications (comma-separated); see below",
    ),
    cloup.option(
        "--match",
        is_flag=True,
        default=False,
        help="Require drift to be within --classification, not merely overlap it",
    ),
    cloup.option(
        "--jobs",
        type=cloup.IntRange(min=1),
        default=DEFAULT_VERIFY_JOBS,
        show_default=True,
        help="Number of resources verified in parallel",
    ),
)
@cloup.option_group(
    "Logging",
    cloup.option(
        "-v",
        "--verbose",
        help="Enable verbose output with debug logs",
        is_flag=True,
        show_default=True,
    ),
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
    mutually_exclusive,
    ["update_schema", "update_schema_for"],
)
@cloup.constraint(
    If(IsSet("update_schema_for"), then=accept_none),
    [
        "kind",
        "discover_missing",
        "coverage_report",
        "generate_missing",
        "regenerate_all",
    ],
)
@cloup.constraint(
    If(IsSet("backup"), then=require_one),
    ["regenerate_all", "overwrite"],
)
@cloup.constraint(
    If(IsSet("filter"), then=require_one),
    ["regenerate_all", "verify_all", "verify_changed"],
)
@cloup.constraint(
    mutually_exclusive,
    ["verify", "verify_all", "verify_changed"],
)
@cloup.constraint(
    mutually_exclusive,
    ["verify", "verify_all", "verify_changed", "regenerate_all"],
)
@cloup.constraint(
    mutually_exclusive,
    ["verify", "verify_all", "verify_changed", "backup"],
)
@cloup.constraint(
    mutually_exclusive,
    ["verify", "verify_all", "verify_changed", "overwrite"],
)
@cloup.constraint(
    mutually_exclusive,
    ["verify", "verify_all", "verify_changed", "add_tests"],
)
@cloup.constraint(
    mutually_exclusive,
    ["verify", "verify_all", "verify_changed", "dry_run"],
)
@cloup.constraint(
    If(IsSet("verify"), then=require_one),
    ["kind"],
)
@cloup.constraint(
    If(IsSet("classification") | IsSet("exclude"), then=require_one),
    ["verify", "verify_all", "verify_changed"],
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
    update_schema_for: str | None,
    verbose: bool,
    verify: bool,
    verify_all: bool,
    verify_changed: bool,
    base: str,
    classification: str | None,
    exclude: str | None,
    match: bool,
    jobs: int,
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
        update_schema_for=update_schema_for,
        discover_missing=discover_missing,
        coverage_report=coverage_report,
        generate_missing=generate_missing,
        regenerate_all=regenerate_all,
        verify=verify,
        verify_all=verify_all,
        verify_changed=verify_changed,
    )

    # Handle single resource schema update (if specified)
    if not handle_single_schema_update(update_schema_for=update_schema_for):
        return

    # Handle full schema update
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

    # Handle verification of generated files (no file is modified)
    if handle_verify(
        verify=verify,
        verify_all=verify_all,
        verify_changed=verify_changed,
        kind=kind,
        filter_pattern=filter,
        base=base,
        classification=classification,
        exclude=exclude,
        match_within=match,
        jobs=jobs,
    ):
        return

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
