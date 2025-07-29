"""Command-line interface for the class generator."""

import sys
from concurrent.futures import Future, ThreadPoolExecutor, as_completed

import cloup
from cloup.constraints import If, IsSet, accept_none
from simple_logger.logger import get_logger

from class_generator.constants import TESTS_MANIFESTS_DIR
from class_generator.core.coverage import analyze_coverage, generate_report
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
@cloup.constraint(
    If(IsSet("update_schema") & ~IsSet("generate_missing"), then=accept_none),
    ["kind", "discover_missing", "coverage_report", "dry_run", "overwrite", "output_file", "add_tests"],
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
    json_output: bool,
    update_schema: bool,
) -> None:
    """Generate Python module for K8S resource."""
    # Check that at least one action is specified
    actions = [kind, update_schema, discover_missing, coverage_report, generate_missing]
    if not any(actions):
        LOGGER.error(
            "At least one action must be specified (--kind, --update-schema, --discover-missing, --coverage-report, or --generate-missing)"
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

    if len(kind_list) == 1:
        # Single kind - run directly
        class_generator(
            kind=kind,
            overwrite=overwrite,
            dry_run=dry_run,
            output_file=output_file,
            add_tests=add_tests,
        )
    else:
        # Multiple kinds - run in parallel
        futures: list[Future] = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for _kind in kind_list:
                futures.append(
                    executor.submit(
                        class_generator,
                        kind=_kind,
                        overwrite=overwrite,
                        dry_run=dry_run,
                        output_file=output_file,
                        add_tests=add_tests,
                    )
                )

            # Wait for all tasks to complete
            for _ in as_completed(futures):
                pass


if __name__ == "__main__":
    main()
