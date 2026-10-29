# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md#adding-tests

import traceback

from class_generator.constants import TESTS_MANIFESTS_DIR
from class_generator.core.generator import class_generator
from class_generator.core.schema import read_resources_mapping_file
from class_generator.utils import execute_parallel_tasks


def _test_single_resource(kind: str) -> tuple[str, str] | None:
    """
    Verify a single resource kind against its expected files and return failure info if test fails.

    Args:
        kind: The resource kind to test

    Returns:
        None if test passes, or (kind, error_message) tuple if test fails
    """
    try:
        if not read_resources_mapping_file().get(kind.lower()):
            return (kind, f"{kind} not found in resources mapping")

        drifted_files = class_generator(
            kind=kind,
            output_dir=str(TESTS_MANIFESTS_DIR / kind),
            verify=True,
            called_from_test=True,
        )

        if drifted_files:
            drifted_names = [drifted[0] if isinstance(drifted, tuple) else drifted for drifted in drifted_files]
            return (kind, f"Generated output differs from expected files: {', '.join(drifted_names)}")

        return None

    except Exception as e:
        error_details = f"Exception during verification: {str(e)}\n"
        error_details += f"Traceback:\n{traceback.format_exc()}"
        return (kind, error_details)


def test_parse_explain() -> None:
    """Test all resource kinds in parallel and collect all failures."""
    # List of all resource kinds to test
    resource_kinds = [
        "APIServer",
        "ClusterOperator",
        "ConfigMap",
        "DNS",
        "Deployment",
        "ImageContentSourcePolicy",
        "Ingress",
        "Machine",
        "NMState",
        "OAuth",
        "Pipeline",
        "Pod",
        "RouteAdvertisements",
        "Secret",
        "ServiceMeshMember",
        "ServingRuntime",
        "VirtualMachineFileRestore",
    ]

    failures: list[tuple[str, str]] = []

    # Process test results and collect failures
    def process_test_result(kind: str, result: tuple[str, str] | None) -> None:
        if result is not None:
            failures.append(result)

    def handle_test_error(kind: str, exc: Exception) -> None:
        failures.append((kind, f"Task execution failed: {str(exc)}"))

    def create_test_task(kind: str) -> tuple[str, str] | None:
        return _test_single_resource(kind)

    # Run tests in parallel
    execute_parallel_tasks(
        tasks=resource_kinds,
        task_func=create_test_task,
        max_workers=8,
        task_name="resource testing",
        result_processor=process_test_result,
        error_handler=handle_test_error,
    )

    # Display all failures if any occurred
    if failures:
        print("\n" + "=" * 70)
        print("RESOURCE GENERATION TEST FAILURES")
        print("=" * 70)

        for i, (kind, error) in enumerate(failures, 1):
            print(f"\n{i}. FAILED: {kind}")
            print(f"   Error: {error}")

        print("\n" + "=" * 70)
        print(f"SUMMARY: {len(failures)} failures out of {len(resource_kinds)} total resources")
        print("=" * 70)

        # Create a concise failure message for pytest
        failed_kinds = [kind for kind, _ in failures]
        failure_summary = f"{len(failures)} resource(s) failed: {','.join(failed_kinds)}"

        # Fail the test with summary - detailed output is already printed above
        raise AssertionError(failure_summary)

    # If we get here, all tests passed
    print(f"\nAll {len(resource_kinds)} resource generation tests passed successfully!")
