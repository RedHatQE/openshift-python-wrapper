#!/usr/bin/env python
"""
OpenShift Python Wrapper - Validation Troubleshooting Guide

This script demonstrates common validation errors and how to fix them.
Run this script to see examples of validation errors and their solutions.
"""

from ocp_resources.deployment import Deployment
from ocp_resources.exceptions import ValidationError
from ocp_resources.pod import Pod
from ocp_resources.service import Service


def print_error_case(title, description):
    """Print an error case header"""
    print(f"\n{'─' * 60}")
    print(f"❌ {title}")
    print(f"   {description}")
    print(f"{'─' * 60}\n")


def print_solution(solution):
    """Print the solution"""
    print(f"\n✅ Solution: {solution}\n")


def case_1_missing_required_fields():
    """Case 1: Missing required fields"""
    print_error_case(
        title="Missing Required Fields", description="One of the most common errors - forgetting required fields"
    )

    # Problem: Missing image in container
    print("Problem code:")
    print("""
    pod = Pod(
        name="my-pod",
        namespace="default",
        containers=[{"name": "nginx"}]  # Missing 'image'
    )
    """)

    try:
        pod = Pod(name="my-pod", namespace="default", containers=[{"name": "nginx"}])
        pod.validate()
    except ValidationError as e:
        print(f"Error: {e}")

    print_solution(solution="Add all required fields according to the Kubernetes API spec")

    print("Fixed code:")
    print("""
    pod = Pod(
        name="my-pod",
        namespace="default",
        containers=[{
            "name": "nginx",
            "image": "nginx:latest"  # Added required field
        }]
    )
    """)


def case_2_wrong_types():
    """Case 2: Wrong data types"""
    print_error_case(
        title="Wrong Data Types", description="Using incorrect types for fields (string instead of int, etc.)"
    )

    # Problem: replicas should be integer
    print("Problem code:")
    print("""
    deployment_dict = {
        "spec": {
            "replicas": "3"  # Should be integer, not string
        }
    }
    """)

    deployment_dict = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": "my-deployment"},
        "spec": {
            "replicas": "3",  # Wrong type
            "selector": {"matchLabels": {"app": "nginx"}},
            "template": {
                "metadata": {"labels": {"app": "nginx"}},
                "spec": {"containers": [{"name": "nginx", "image": "nginx:latest"}]},
            },
        },
    }

    try:
        Deployment.validate_dict(resource_dict=deployment_dict)
    except ValidationError as e:
        print(f"Error: {e}")

    print_solution(solution="Use the correct data type (integer for replicas)")

    print("Fixed code:")
    print("""
    deployment_dict = {
        "spec": {
            "replicas": 3  # Correct integer type
        }
    }
    """)


def case_3_invalid_field_values():
    """Case 3: Invalid field values"""
    print_error_case(
        title="Invalid Field Values", description="Using values that don't match the allowed pattern or range"
    )

    # Problem: Invalid DNS name
    print("Problem code:")
    print("""
    pod = Pod(
        name="My-Pod-123",  # Capital letters not allowed
        namespace="default"
    )
    """)

    try:
        pod = Pod(
            name="My-Pod-123",  # Invalid DNS name
            namespace="default",
            containers=[{"name": "nginx", "image": "nginx:latest"}],
        )
        pod.validate()
    except ValidationError as e:
        print(f"Error: {e}")

    print_solution(solution="Follow Kubernetes naming conventions (lowercase, alphanumeric, hyphens)")

    print("Fixed code:")
    print("""
    pod = Pod(
        name="my-pod-123",  # Valid DNS name
        namespace="default"
    )
    """)


def case_4_invalid_structure():
    """Case 4: Invalid resource structure"""
    print_error_case(
        title="Invalid Resource Structure", description="Incorrect nesting or structure of resource fields"
    )

    # Problem: ports should be an array
    print("Problem code:")
    print("""
    service = Service(
        name="my-service",
        namespace="default",
        selector={"app": "nginx"},
        ports={"port": 80}  # Should be array, not dict
    )
    """)

    try:
        # This will fail during object creation, not validation
        service_dict = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "my-service", "namespace": "default"},
            "spec": {
                "selector": {"app": "nginx"},
                "ports": {"port": 80},  # Wrong structure
            },
        }
        Service.validate_dict(resource_dict=service_dict)
    except ValidationError as e:
        print(f"Error: {e}")

    print_solution(solution="Use correct structure (array for ports)")

    print("Fixed code:")
    print("""
    service = Service(
        name="my-service",
        namespace="default",
        selector={"app": "nginx"},
        ports=[{"port": 80, "targetPort": 80}]  # Correct array structure
    )
    """)


def case_5_debugging_complex_errors():
    """Case 5: Debugging complex validation errors"""
    print_error_case(
        title="Debugging Complex Errors", description="How to understand and fix multi-level validation errors"
    )

    print("When you get a complex error, look for:")
    print("1. The path to the error (e.g., 'spec.template.spec.containers[0]')")
    print("2. The specific validation rule that failed")
    print("3. The actual vs expected value/type")

    # Example of complex error
    print("\nExample complex error:")
    deployment_dict = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": "complex-deployment"},
        "spec": {
            "selector": {"matchLabels": {"app": "test"}},
            "template": {
                "metadata": {"labels": {"app": "test"}},
                "spec": {
                    "containers": [
                        {
                            "name": "app",
                            "image": "myapp:latest",
                            "resources": {
                                "limits": {
                                    "memory": 100  # Should be string with units
                                }
                            },
                        }
                    ]
                },
            },
        },
    }

    try:
        Deployment.validate_dict(resource_dict=deployment_dict)
    except ValidationError as e:
        print(f"Error: {e}")

    print_solution(solution="Follow the error path and fix the specific issue")
    print("In this case: memory should be a string with units (e.g., '100Mi')")


def case_6_validation_performance():
    """Case 6: Validation performance tips"""
    print_error_case(title="Performance Considerations", description="Tips for optimal validation performance")

    print("Performance tips:")
    print("1. First validation loads schema (~25ms), subsequent are cached (~2ms)")
    print("2. Pre-warm cache for critical resources at startup")
    print("3. Disable auto-validation for bulk operations")
    print("4. Use validate_dict() for pre-validation without creating objects")

    print("\nExample - Pre-warming cache:")
    print("""
    # At application startup
    def warmup_cache():
        for resource_cls in [Pod, Deployment, Service]:
            try:
                resource_cls.validate_dict({
                    "apiVersion": "v1",
                    "kind": resource_cls.kind,
                    "metadata": {"name": "dummy"}
                })
            except ValidationError:
                # Schema validation errors are expected during warmup
                pass  # Ignore validation errors, just loading schemas
            except (ValueError, TypeError, AttributeError) as e:
                # Handle potential errors from missing/malformed data
                print(f"Warning: Failed to warmup cache for {resource_cls.kind}: {e}")
    """)


def main():
    """Run all troubleshooting cases"""
    print("\n" + "=" * 60)
    print(" Validation Troubleshooting Guide")
    print("=" * 60)

    cases = [
        case_1_missing_required_fields,
        case_2_wrong_types,
        case_3_invalid_field_values,
        case_4_invalid_structure,
        case_5_debugging_complex_errors,
        case_6_validation_performance,
    ]

    for case in cases:
        try:
            case()
        except Exception as e:
            print(f"\nUnexpected error in case: {e}")

    print("\n" + "=" * 60)
    print(" Common Validation Error Patterns:")
    print("=" * 60)
    print("""
    1. 'None is not of type X' → Required field is missing
    2. 'X is not of type Y' → Wrong data type used
    3. 'Does not match pattern' → Invalid format (e.g., DNS names)
    4. 'X is not one of [Y, Z]' → Invalid enum value
    5. 'Additional properties not allowed' → Unknown field name
    6. 'X is less than Y' → Value outside allowed range
    """)

    print("\n✨ Remember: Validation errors are your friend!")
    print("   They catch issues before they reach the Kubernetes API,")
    print("   saving time and preventing failed deployments.")


if __name__ == "__main__":
    main()
