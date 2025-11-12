"""Coverage analysis for generated resources vs available cluster resources."""

import ast
import json
import os
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from simple_logger.logger import get_logger

from class_generator.constants import GENERATED_USING_MARKER
from class_generator.core.schema import read_resources_mapping_file

LOGGER = get_logger(name=__name__)


def analyze_coverage(
    resources_dir: str = "ocp_resources",
) -> dict[str, Any]:
    """Analyze resource coverage by comparing schema-mapped resources vs implemented resources."""
    # Get all resources from the schema mapping
    resources_mapping = read_resources_mapping_file()
    all_mapped_resources: set[str] = set()

    # Convert schema keys to proper case (they're lowercase in schema)
    for kind in resources_mapping:
        # Schema keys are lowercase, need to convert to PascalCase
        # e.g., "aaq" -> "AAQ", "pod" -> "Pod", "virtualservice" -> "VirtualService"
        if kind.isupper():
            # Already uppercase
            all_mapped_resources.add(kind)
        else:
            # Convert to PascalCase - handle special cases
            if "_" in kind:
                # Handle snake_case
                pascal_case = "".join(word.capitalize() for word in kind.split("_"))
            else:
                # Simple lowercase to PascalCase
                pascal_case = kind[0].upper() + kind[1:] if kind else ""
            all_mapped_resources.add(pascal_case)

    # Scan implemented resources
    generated_resources = []  # Auto-generated resources
    manual_resources = []  # Manually created resources

    files = []
    try:
        if os.path.exists(resources_dir):
            files = os.listdir(resources_dir)
    except Exception as e:
        LOGGER.error(f"Failed to scan resources directory: {e}")
        files = []

    # Parse each Python file to find implemented resources
    for filename in files:
        # Skip non-Python files and special files
        if not filename.endswith(".py") or filename == "__init__.py":
            continue

        # Skip utility/helper files
        if filename in ["utils.py", "constants.py", "exceptions.py", "resource.py"]:
            continue

        filepath = os.path.join(resources_dir, filename)
        if not os.path.isfile(filepath):
            continue

        try:
            with open(filepath) as f:
                content = f.read()

            # Check if file is auto-generated
            is_generated = GENERATED_USING_MARKER in content

            # Parse the file to find class definitions
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if this is a resource class (not a helper/base class)
                    # Look for classes that inherit from Resource, NamespacedResource, etc.
                    for base in node.bases:
                        base_name = ""
                        if isinstance(base, ast.Name):
                            base_name = base.id
                        elif isinstance(base, ast.Attribute):
                            # Handle cases like resources.Resource
                            base_name = base.attr

                        if base_name in ["Resource", "NamespacedResource"]:
                            # Found a resource class
                            if is_generated:
                                generated_resources.append(node.name)
                            else:
                                manual_resources.append(node.name)
                            break

        except Exception as e:
            LOGGER.debug(f"Failed to parse {filename}: {e}")

    # Calculate coverage based on schema mapping
    generated_set = set(generated_resources)
    manual_set = set(manual_resources)

    # Create lowercase mapping for comparison
    generated_lower = {r.lower(): r for r in generated_set}
    all_mapped_lower = {r.lower(): r for r in all_mapped_resources}

    # Find matches (case-insensitive)
    matched_generated = []
    not_generated = []

    for mapped_lower, mapped_original in all_mapped_lower.items():
        if mapped_lower in generated_lower:
            matched_generated.append(generated_lower[mapped_lower])
        else:
            not_generated.append(mapped_original)

    not_generated.sort()

    # Normalize missing_resources entries to dicts with "kind" key
    missing_resources = [{"kind": resource} if isinstance(resource, str) else resource for resource in not_generated]

    # Calculate coverage statistics
    total_in_mapping = len(all_mapped_resources)
    total_generated = len(matched_generated)
    coverage_percentage = (total_generated / total_in_mapping * 100) if total_in_mapping > 0 else 0

    return {
        "generated_resources": sorted(generated_set),
        "manual_resources": sorted(manual_set),
        "missing_resources": missing_resources,  # Resources in mapping but not generated
        "coverage_stats": {
            "total_in_mapping": total_in_mapping,
            "total_generated": total_generated,
            "total_manual": len(manual_set),
            "coverage_percentage": coverage_percentage,
            "missing_count": len(missing_resources),
        },
    }


def generate_report(coverage_data: dict[str, Any], output_format: str | None = None) -> str | None:
    """Generate a coverage report in the specified format."""
    stats = coverage_data["coverage_stats"]

    if output_format == "json":
        return json.dumps(coverage_data, indent=2)

    # Default behavior - console output
    console = Console()

    # Create summary table
    summary_table = Table(title="Resource Coverage Summary", show_header=False)
    summary_table.add_column(style="bold", header="Metric")
    summary_table.add_column(justify="right", header="Value")

    summary_table.add_row("Total Resources in Schema", str(stats["total_in_mapping"]))
    summary_table.add_row("Auto-Generated Resources", str(stats["total_generated"]))
    summary_table.add_row("Coverage", f"{stats['coverage_percentage']:.1f}%")
    summary_table.add_row("", "")  # Empty row for separation
    summary_table.add_row("Missing (Not Generated)", str(stats["missing_count"]))
    summary_table.add_row("Manual Implementations", str(stats["total_manual"]))

    console.print(Panel(summary_table, title="Coverage Analysis", border_style="green"))

    # Show missing resources if any
    if coverage_data["missing_resources"]:
        missing_table = Table(title="Resources Not Yet Generated")
        missing_table.add_column(header="Resource Kind", style="red")

        for resource in coverage_data["missing_resources"][:20]:  # Show first 20
            # Handle both string and dict formats
            if isinstance(resource, dict):
                kind = resource.get("kind", str(resource))
            else:
                kind = str(resource)
            missing_table.add_row(kind)

        if len(coverage_data["missing_resources"]) > 20:
            missing_table.add_row(f"... and {len(coverage_data['missing_resources']) - 20} more")

        console.print(missing_table)

    # Print ready-to-use commands
    if coverage_data["missing_resources"]:
        console.print("\n[bold]Generate missing resources with:[/bold]")
        for resource in coverage_data["missing_resources"][:5]:
            if isinstance(resource, dict):
                kind = resource.get("kind", resource)
            else:
                kind = resource
            console.print(f"  class-generator -k {kind}")
        if len(coverage_data["missing_resources"]) > 5:
            console.print(f"  ... and {len(coverage_data['missing_resources']) - 5} more")

    return None
