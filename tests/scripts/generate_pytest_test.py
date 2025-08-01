#!/usr/bin/env python3
"""
Pytest Test Generator for OCP Resources

This script generates pytest tests for Kubernetes/OpenShift resources using the fake_kubernetes_client.
It can generate tests for specific kinds or analyze test coverage across all resources.

Usage:
    # Generate tests for specific kinds
    uv run python tests/scripts/generate_pytest_test.py --kind Pod
    uv run python tests/scripts/generate_pytest_test.py --kind Pod,Node,Service

    # Check which resources have tests vs missing tests
    uv run python tests/scripts/generate_pytest_test.py --check-coverage

    # Generate tests for all missing resources
    uv run python tests/scripts/generate_pytest_test.py --generate-missing

    # Dry run mode
    uv run python tests/scripts/generate_pytest_test.py --kind Pod --dry-run

Features:
- Scans ocp_resources/ directory to discover all resource classes
- Generates comprehensive CRUD tests (create, get, update, delete)
- Uses fake_kubernetes_client for isolated testing
- Analyzes test coverage and identifies missing tests
- Smart parameter generation based on resource requirements
- Proper fixture setup for namespaced vs cluster resources

Author: Generated by AI Assistant
License: Same as openshift-python-wrapper project
"""

import importlib
import shlex
import subprocess
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union, get_type_hints, get_origin, get_args

import cloup
from jinja2 import DictLoader, Environment
from pyhelper_utils.shell import run_command
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

# Import ResourceScanner and ResourceInfo from class_generator.utils
from class_generator.utils import ResourceScanner, ResourceInfo

console = Console()

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Static mapping of ephemeral resources to their actual resource types
EPHEMERAL_RESOURCES = {
    "ProjectRequest": "Project",  # ProjectRequest creates Project
    # Add more ephemeral resources here as discovered:
    # "SomeOtherEphemeralResource": "ActualResourceType",
}


@dataclass
class CoverageReport:
    """Test coverage analysis results"""

    resources_with_tests: dict[str, str]  # {resource_name: test_file_path}
    resources_without_tests: dict[str, str]  # {resource_name: resource_file_path}
    invalid_resources: dict[str, str]  # {resource_name: reason}
    total_resources: int
    tested_resources: int
    coverage_percentage: float


# Remove ResourceInfo and ResourceScanner classes - they're now imported from class_generator.utils


class TestCoverageAnalyzer:
    """Analyzes test coverage for resources"""

    def __init__(self, tests_path: str = "tests"):
        self.tests_path = Path(tests_path)

    def analyze_coverage(self, resources: list[ResourceInfo]) -> CoverageReport:
        """Analyze test coverage for discovered resources"""
        existing_tests = self._find_existing_tests()

        resources_with_tests: dict[str, str] = {}
        resources_without_tests: dict[str, str] = {}
        invalid_resources: dict[str, str] = {}

        for resource in resources:
            test_file = self._find_test_for_resource(resource.name, existing_tests)
            if test_file:
                resources_with_tests[resource.name] = test_file
            else:
                resources_without_tests[resource.name] = resource.file_path

        total_resources = len(resources)
        tested_resources = len(resources_with_tests)
        coverage_percentage = (tested_resources / total_resources * 100) if total_resources > 0 else 0

        return CoverageReport(
            resources_with_tests=resources_with_tests,
            resources_without_tests=resources_without_tests,
            invalid_resources=invalid_resources,
            total_resources=total_resources,
            tested_resources=tested_resources,
            coverage_percentage=coverage_percentage,
        )

    def _find_existing_tests(self) -> dict[str, str]:
        """Find all existing test files"""
        tests = {}

        for test_file in self.tests_path.glob("test_*.py"):
            # Extract potential resource name from test file
            test_name = test_file.stem.replace("test_", "")
            tests[test_name] = str(test_file)

        return tests

    def _find_test_for_resource(self, resource_name: str, existing_tests: dict[str, str]) -> Union[str, None]:
        """Find test file for a specific resource"""
        # Convert resource name to potential test file names
        potential_names = [resource_name.lower(), resource_name]

        for name in potential_names:
            if name in existing_tests:
                return existing_tests[name]

        return None


class PytestTestGenerator:
    """Generates pytest tests for resources"""

    def __init__(self):
        template_env = Environment(loader=DictLoader(self._get_templates()))
        # Add custom filter for Python repr
        template_env.filters["python_repr"] = self._python_repr_filter
        self.template_env = template_env

    def _python_repr_filter(self, value):
        """Custom Jinja2 filter to get Python representation of values"""
        return repr(value)

    def generate_test_for_resource(self, resource: ResourceInfo) -> str:
        """Generate test code for a specific resource"""
        # Choose template based on whether resource is ephemeral
        template_name = "ephemeral_template.j2" if resource.is_ephemeral else "test_template.j2"
        template = self.template_env.get_template(name=template_name)

        # Generate test data
        test_data = self._generate_test_data(resource)

        # Extract module name from file path
        module_name = Path(resource.file_path).stem

        return template.render(
            resource=resource,
            test_data=test_data,
            fixture_name=resource.name.lower(),
            class_name=f"Test{resource.name}",
            module_name=module_name,
        )

    def _detect_template_type_from_docstring(self, resource: ResourceInfo, param_name: str) -> str:
        """Detect template type from resource docstring - follows oc explain output"""
        try:
            # Import the resource class to get docstring
            module_name = Path(resource.file_path).stem
            module = importlib.import_module(f"ocp_resources.{module_name}")
            resource_class = getattr(module, resource.name)

            # Get the __init__ docstring
            docstring = resource_class.__init__.__doc__ or ""

            # Extract the template parameter description
            template_description = self._extract_param_description(docstring, param_name)

            if template_description:
                desc_lower = template_description.lower()

                # Pattern matching based on docstring keywords (following oc explain)
                if "dvs to be created" in desc_lower or "datavolume" in desc_lower:
                    return "datavolume"
                elif "podtemplatespec" in desc_lower or "pod template" in desc_lower or "pod should have" in desc_lower:
                    return "pod"
                elif "pods that will be created" in desc_lower:
                    return "pod"  # Follow docstring even if seems wrong for VM resources
                elif "revision to be stamped" in desc_lower or "revision specification" in desc_lower:
                    return "knative_revision"
                elif "common templates" in desc_lower and "operand" in desc_lower:
                    return "vm_template"
                elif "template validator" in desc_lower:
                    return "validator_config"

            return "unknown"

        except Exception:
            return "unknown"

    def _extract_param_description(self, docstring: str, param_name: str) -> str:
        """Extract parameter description from docstring"""
        if not docstring or not param_name:
            return ""

        lines = docstring.split("\n")
        for i, line in enumerate(lines):
            # Look for parameter definition: "param_name (type): description"
            if f"{param_name} (" in line and "):" in line:
                # Extract description part after "):"
                desc_start = line.find("):") + 2
                description = line[desc_start:].strip()

                # Check if description continues on next lines (indented)
                j = i + 1
                while j < len(lines) and lines[j].strip() and lines[j].startswith("              "):
                    description += " " + lines[j].strip()
                    j += 1

                return description

        return ""

    def _generate_template_by_type(self, template_type: str) -> dict:
        """Generate template based on detected type from docstring"""
        if template_type == "datavolume":
            # DataVolume template (DVTemplateSpec)
            return {
                "metadata": {"labels": {"app": "test"}},
                "spec": {
                    "source": {"http": {"url": "http://example.com/disk.qcow2"}},
                    "pvc": {"accessModes": ["ReadWriteOnce"], "resources": {"requests": {"storage": "1Gi"}}},
                },
            }
        elif template_type == "pod":
            # Pod template (PodTemplateSpec) - follows docstring even if seems wrong
            return {
                "metadata": {"labels": {"app": "test"}},
                "spec": {"containers": [{"name": "test-container", "image": "nginx:latest"}]},
            }
        elif template_type == "knative_revision":
            # Knative Revision template
            return {"spec": {"containers": [{"image": "nginx:latest", "name": "nginx"}]}}
        elif template_type == "vm_template":
            # VM template configuration
            return {"test-vm-template": "test-value"}
        elif template_type == "validator_config":
            # Template validator configuration
            return {"test-validator": "test-value"}
        else:
            # Unknown type - fallback to pod template
            return {
                "metadata": {"labels": {"app": "test"}},
                "spec": {"containers": [{"name": "test-container", "image": "nginx:latest"}]},
            }

    def _get_type_aware_value(self, resource: ResourceInfo, param_name: str) -> Any:
        """Generate a test value based on the parameter's actual type hint"""
        try:
            # Import the resource class to get type hints
            module_name = Path(resource.file_path).stem
            module = importlib.import_module(f"ocp_resources.{module_name}")
            resource_class = getattr(module, resource.name)

            # Get type hints from the constructor
            type_hints = get_type_hints(resource_class.__init__)
            param_type = type_hints.get(param_name)

            if param_type is None:
                return f"test-{param_name}"

            # Handle Union types (e.g., bool | None, str | None)
            if type(param_type) is types.UnionType or get_origin(param_type) is Union:
                # Get the non-None type from Union
                args = get_args(param_type)
                non_none_types = [arg for arg in args if arg is not type(None)]
                if non_none_types:
                    param_type = non_none_types[0]

            # Generate value based on type
            if param_type is bool:
                return True
            elif param_type is int:
                return 1
            elif param_type is str:
                return f"test-{param_name}"
            elif param_type is list or (hasattr(param_type, "__origin__") and param_type.__origin__ is list):
                return [f"test-{param_name}"]
            elif param_type is dict or (hasattr(param_type, "__origin__") and param_type.__origin__ is dict):
                return {f"test-{param_name}": "test-value"}
            else:
                return f"test-{param_name}"

        except Exception:
            # Fallback to string if type analysis fails
            return f"test-{param_name}"

    def _generate_test_data(self, resource: ResourceInfo) -> dict[str, Any]:
        """Generate realistic test data for a resource"""
        data: dict[str, Any] = {
            "name": f"test-{resource.name.lower()}",
        }

        # Add namespace for namespaced resources
        if resource.base_class == "NamespacedResource":
            data["namespace"] = "default"

        # Add resource-specific required parameters
        if resource.name == "VolumeSnapshotClass":
            data["deletion_policy"] = "Delete"
            data["driver"] = "example.com/csi-driver"
        elif resource.name == "ConfigMap":
            data["data"] = {"key1": "value1"}
        elif resource.name == "Secret":
            data["string_data"] = {"password": "secret123"}  # pragma: allowlist secret
        elif resource.name == "PersistentVolumeClaim":
            data["access_modes"] = ["ReadWriteOnce"]
            data["size"] = "1Gi"
        elif resource.name == "Deployment":
            # Deployment needs selector and template, not containers directly
            data["selector"] = {"matchLabels": {"app": "test"}}
            data["template"] = {
                "metadata": {"labels": {"app": "test"}},
                "spec": {"containers": [{"name": "test-container", "image": "nginx:latest"}]},
            }
            data["replicas"] = 1
        elif resource.name == "Pod":
            # Pod takes containers directly
            data["containers"] = [{"name": "test-container", "image": "nginx:latest"}]
        elif resource.name == "Service":
            # Distinguish between core v1 Service and serving.knative.dev Service
            module_name = Path(resource.file_path).stem
            if module_name == "service_serving_knative_dev" or "serving.knative.dev" in (resource.api_group or ""):
                # Knative serving Service needs template and traffic
                data["template"] = {"spec": {"containers": [{"image": "nginx:latest", "name": "nginx"}]}}
                data["traffic"] = [{"percent": 100, "latestRevision": True}]
            else:
                # Core v1 Service needs ports and selector
                data["ports"] = [{"port": 80, "target_port": 8080}]
                data["selector"] = {"app": "test"}
        elif resource.name == "UserDefinedNetwork":
            # This requires topology parameter
            data["topology"] = "Layer2"
        elif resource.name == "VirtualMachineInstanceReplicaSet":
            # VirtualMachineInstanceReplicaSet needs selector (template will be auto-detected)
            data["selector"] = {"matchLabels": {"app": "test"}}
        elif resource.name == "DataImportCron":
            # DataImportCron specific parameters (template will be auto-detected)
            data["managed_data_source"] = "test-managed-data-source"
            data["schedule"] = "0 2 * * *"  # Daily at 2 AM (cron format)

        # Add any additional required parameters from analysis
        for param in resource.required_params:
            if param not in data and param not in ["name", "namespace", "client"]:
                # Provide sensible defaults for common parameter names
                if param in ["deletion_policy"]:
                    data[param] = "Delete"
                elif param in ["driver"]:
                    data[param] = "example.com/driver"
                elif param in ["access_modes"]:
                    data[param] = ["ReadWriteOnce"]
                elif param in ["size"]:
                    data[param] = "1Gi"
                elif param in ["selector"]:
                    data[param] = {"matchLabels": {"app": "test"}}
                elif param in ["template"]:
                    # Auto-detect template type from resource docstring
                    template_type = self._detect_template_type_from_docstring(resource, param)
                    data[param] = self._generate_template_by_type(template_type)
                elif param in ["topology"]:
                    data[param] = "Layer2"
                elif param.endswith("_policy"):
                    data[param] = "Delete"
                elif "port" in param.lower():
                    data[param] = [{"port": 80, "target_port": 8080}]
                elif "data" in param.lower():
                    data[param] = {"key1": "value1"}
                else:
                    # Use type-aware value generation
                    data[param] = self._get_type_aware_value(resource, param)

        return data

    def _get_templates(self) -> dict[str, str]:
        """Get Jinja2 templates for test generation"""
        return {
            "test_template.j2": '''import pytest
from ocp_resources.{{ module_name }} import {{ resource.name }}

@pytest.mark.incremental
class {{ class_name }}:
    @pytest.fixture(scope="class")
    def {{ fixture_name }}(self, fake_client):
        return {{ resource.name }}(
            client=fake_client,
{%- for key, value in test_data.items() %}
{%- if key == "name" %}
            name="{{ value }}",
{%- elif key == "namespace" %}
            namespace="{{ value }}",
{%- elif value is string %}
            {{ key }}="{{ value }}",
{%- else %}
            {{ key }}={{ value | python_repr }},
{%- endif %}
{%- endfor %}
        )

    def test_01_create_{{ fixture_name }}(self, {{ fixture_name }}):
        """Test creating {{ resource.name }}"""
        deployed_resource = {{ fixture_name }}.deploy()
        assert deployed_resource
        assert deployed_resource.name == "{{ test_data.name }}"
        assert {{ fixture_name }}.exists

    def test_02_get_{{ fixture_name }}(self, {{ fixture_name }}):
        """Test getting {{ resource.name }}"""
        assert {{ fixture_name }}.instance
        assert {{ fixture_name }}.kind == "{{ resource.name }}"

    def test_03_update_{{ fixture_name }}(self, {{ fixture_name }}):
        """Test updating {{ resource.name }}"""
        resource_dict = {{ fixture_name }}.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        {{ fixture_name }}.update(resource_dict=resource_dict)
        assert {{ fixture_name }}.labels["updated"] == "true"

    def test_04_delete_{{ fixture_name }}(self, {{ fixture_name }}):
        """Test deleting {{ resource.name }}"""
        {{ fixture_name }}.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not {{ fixture_name }}.exists
''',
            "ephemeral_template.j2": '''import pytest
from ocp_resources.{{ module_name }} import {{ resource.name }}
{%- if resource.actual_resource_type == "Project" %}
from ocp_resources.project_project_openshift_io import Project
{%- endif %}

@pytest.mark.incremental
class {{ class_name }}:
    @pytest.fixture(scope="class")
    def {{ fixture_name }}(self, fake_client):
        return {{ resource.name }}(
            client=fake_client,
{%- for key, value in test_data.items() %}
{%- if key == "name" %}
            name="{{ value }}",
{%- elif key == "namespace" %}
            namespace="{{ value }}",
{%- elif value is string %}
            {{ key }}="{{ value }}",
{%- else %}
            {{ key }}={{ value | python_repr }},
{%- endif %}
{%- endfor %}
        )

    def test_01_create_{{ fixture_name }}(self, {{ fixture_name }}):
        """Test creating ephemeral {{ resource.name }} (creates {{ resource.actual_resource_type }})"""
        # Create the ephemeral resource - this returns raw ResourceInstance
        actual_resource_instance = {{ fixture_name }}.create()

        # Wrap in proper Resource object to use ocp-resources methods
        actual_resource = {{ resource.actual_resource_type }}(
            client={{ fixture_name }}.client,
            name=actual_resource_instance.metadata.name
        )

        # Verify the actual resource was created and has correct properties
        assert actual_resource.name == "{{ test_data.name }}"
        assert actual_resource.exists
        assert actual_resource.kind == "{{ resource.actual_resource_type }}"
        # The ephemeral resource itself should not exist after creation
        assert not {{ fixture_name }}.exists

    def test_02_get_{{ fixture_name }}(self, {{ fixture_name }}):
        """Test getting {{ resource.name }} properties"""
        # We can still access the ephemeral resource's properties before deployment
        assert {{ fixture_name }}.kind == "{{ resource.name }}"
        assert {{ fixture_name }}.name == "{{ test_data.name }}"

    def test_03_delete_{{ fixture_name }}(self, {{ fixture_name }}):
        """Test deleting {{ resource.name }} (deletes {{ resource.actual_resource_type }})"""
        # First create to get the actual resource
        actual_resource_instance = {{ fixture_name }}.create()

        # Wrap in proper Resource object
        actual_resource = {{ resource.actual_resource_type }}(
            client={{ fixture_name }}.client,
            name=actual_resource_instance.metadata.name
        )
        assert actual_resource.exists

        # Clean up should delete the actual resource, not the ephemeral one
        {{ fixture_name }}.clean_up(wait=False)

        # Verify the actual resource no longer exists using Resource methods
        assert not actual_resource.exists
''',
        }


def run_ruff_on_files(filepaths: list[str]) -> bool:
    """Run ruff format and check on files"""
    try:
        file_count = len(filepaths)
        file_desc = "file" if file_count == 1 else f"{file_count} files"
        console.print(f"[bold blue]Running ruff format and check on {file_desc}...[/bold blue]")

        # Run ruff format and check on all files
        for op in ("format", "check"):
            cmd_str = f"uvx ruff {op} {' '.join(filepaths)}"
            rc, _, _ = run_command(
                command=shlex.split(cmd_str),
                verify_stderr=False,
                check=False,
            )
            if rc != 0:
                console.print(f"[yellow]Ruff {op} returned exit code {rc}[/yellow]")

        return True

    except Exception as e:
        console.print(f"[red]Error running ruff: {e}[/red]")
        return False


def run_pytest_on_files(test_filepaths: list[str]) -> bool:
    """Run pytest on test files and return True if all tests pass"""
    try:
        file_count = len(test_filepaths)
        file_desc = "file" if file_count == 1 else f"{file_count} files"
        console.print(f"\n[bold blue]Running pytest on {file_desc}...[/bold blue]")

        # Run pytest with uv and let it show output directly (live output, no coverage)
        cmd = ["uv", "run", "--group", "tests", "pytest"] + test_filepaths + ["-s", "--no-cov"]
        result = subprocess.run(cmd, cwd=Path.cwd())

        return result.returncode == 0

    except Exception as e:
        console.print(f"[red]Error running pytest: {e}[/red]")
        return False


def print_coverage_report(coverage: CoverageReport):
    """Print a formatted coverage report"""
    console.print("\n[bold blue]Test Coverage Analysis[/bold blue]")
    console.print(f"Total Resources: {coverage.total_resources}")
    console.print(f"Tested Resources: {coverage.tested_resources}")
    console.print(f"Coverage: {coverage.coverage_percentage:.1f}%")

    if coverage.resources_with_tests:
        console.print(f"\n[bold green]Resources with Tests ({len(coverage.resources_with_tests)}):[/bold green]")
        table = Table(show_header=True, header_style="bold green")
        table.add_column(header="Resource")
        table.add_column(header="Test File")

        for resource, test_file in sorted(coverage.resources_with_tests.items()):
            table.add_row(resource, test_file)
        console.print(table)

    if coverage.resources_without_tests:
        console.print(f"\n[bold red]Resources without Tests ({len(coverage.resources_without_tests)}):[/bold red]")
        table = Table(show_header=True, header_style="bold red")
        table.add_column(header="Resource")
        table.add_column(header="Resource File")

        for resource, resource_file in sorted(coverage.resources_without_tests.items()):
            table.add_row(resource, resource_file)
        console.print(table)


@cloup.command()
@cloup.option("--kind", help="Comma-separated list of resource kinds to generate tests for")
@cloup.option("--check-coverage", is_flag=True, help="Check test coverage without generating tests")
@cloup.option("--generate-missing", is_flag=True, help="Generate tests for all resources without tests")
@cloup.option("--dry-run", is_flag=True, help="Show what would be generated without creating files")
def main(kind, check_coverage, generate_missing, dry_run):
    """
    Generate pytest tests for OCP resources using fake_kubernetes_client.

    This tool scans the ocp_resources/ directory to discover resource classes
    and generates comprehensive CRUD tests for them.

    Note: Tests are only generated for classes that were generated by class-generator.
    """
    console.print("[bold blue]OCP Resources Pytest Test Generator[/bold blue]")

    # Initialize components
    scanner = ResourceScanner()
    analyzer = TestCoverageAnalyzer()
    generator = PytestTestGenerator()

    # Scan for resources
    console.print("Scanning ocp_resources directory...")
    resources = scanner.scan_resources()
    console.print(f"Found {len(resources)} resource classes")

    # Analyze coverage
    coverage = analyzer.analyze_coverage(resources=resources)

    if check_coverage:
        print_coverage_report(coverage=coverage)
        return

    # Determine which resources to generate tests for
    target_resources = []

    if kind:
        # Generate tests for specific kinds
        kind_list = [k.strip() for k in kind.split(",")]
        target_resources = [r for r in resources if r.name in kind_list]

        # Check for invalid kinds
        found_kinds = {r.name for r in target_resources}
        invalid_kinds = set(kind_list) - found_kinds
        if invalid_kinds:
            console.print(f"[red]Error: Invalid kinds: {', '.join(invalid_kinds)}[/red]")
            console.print(f"Available kinds: {', '.join(sorted(r.name for r in resources))}")
            return

    elif generate_missing:
        # Generate tests for all resources without tests
        target_resources = [r for r in resources if r.name in coverage.resources_without_tests]
        console.print(f"Generating tests for {len(target_resources)} resources without tests")

    else:
        console.print("[yellow]Please specify --kind, --generate-missing, or --check-coverage[/yellow]")
        print_coverage_report(coverage=coverage)
        return

    # Generate tests
    generated_files = []

    for resource in target_resources:
        console.print(f"Generating test for {resource.name}...")

        try:
            # Create output directory
            resource_file_name = Path(resource.file_path).stem  # Extract filename without extension
            output_path = Path("tests") / "test_resources"
            output_path.mkdir(parents=True, exist_ok=True)

            test_code = generator.generate_test_for_resource(resource=resource)
            test_filename = f"test_{resource_file_name}.py"
            test_filepath = output_path / test_filename

            if dry_run:
                if test_filepath.exists():
                    console.print(f"[yellow]Would overwrite: {test_filepath}[/yellow]")
                else:
                    console.print(f"[yellow]Would create: {test_filepath}[/yellow]")
                # Show the complete generated code
                syntax = Syntax(code=test_code, lexer="python", theme="monokai", line_numbers=True)
                console.print(syntax)
            else:
                # Always overwrite existing files
                file_action = "Overwritten" if test_filepath.exists() else "Created"
                with open(test_filepath, "w", encoding="utf-8") as f:
                    f.write(test_code)
                generated_files.append(str(test_filepath))
                console.print(f"{file_action}: {test_filepath}")

        except Exception as e:
            console.print(f"[red]Failed to generate test for {resource.name}: {e}[/red]")

    # Summary and test execution
    if not dry_run and generated_files:
        console.print(f"\n[bold green]Successfully generated {len(generated_files)} test files:[/bold green]")
        for filepath in generated_files:
            console.print(f"  - {filepath}")

        # Run ruff on all generated files
        run_ruff_on_files(filepaths=generated_files)

        # Run pytest on all generated files
        console.print("\n[bold blue]Running tests on generated files...[/bold blue]")
        success = run_pytest_on_files(test_filepaths=generated_files)

        if success:
            console.print("[bold green]All tests passed![/bold green]")
        else:
            console.print("[bold yellow]Some tests failed. Check the output above for details.[/bold yellow]")

    elif dry_run:
        console.print(
            f"\n[bold yellow]Dry run completed. Would generate {len(target_resources)} test files.[/bold yellow]"
        )


if __name__ == "__main__":
    main.main()
