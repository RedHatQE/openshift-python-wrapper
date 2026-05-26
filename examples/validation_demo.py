#!/usr/bin/env python
"""
OpenShift Python Wrapper - Schema Validation Demo

This script demonstrates the schema validation capabilities of the wrapper,
including manual validation, auto-validation, error handling, and performance.
"""

import time

from ocp_resources.config_map import ConfigMap
from ocp_resources.deployment import Deployment
from ocp_resources.exceptions import ValidationError
from ocp_resources.pod import Pod
from ocp_resources.resource import get_client
from ocp_resources.service import Service


def print_section(title):
    """Print a section header"""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}\n")


def demo_basic_validation():
    """Demonstrate basic manual validation"""
    print_section(title="Basic Manual Validation")

    # Create a valid pod
    print("1. Creating a valid pod and validating...")
    pod = Pod(
        name="nginx-pod",
        namespace="default",
        containers=[{"name": "nginx", "image": "nginx:latest", "ports": [{"containerPort": 80}]}],
    )

    try:
        pod.validate()
        print("✓ Pod validation passed!")
    except ValidationError as e:
        print(f"✗ Pod validation failed: {e}")

    # Create an invalid pod (missing required fields)
    print("\n2. Creating an invalid pod (missing image)...")
    invalid_pod = Pod(
        name="invalid-pod",
        namespace="default",
        containers=[{"name": "nginx"}],  # Missing required 'image' field
    )

    try:
        invalid_pod.validate()
        print("✓ Pod validation passed (unexpected!)")
    except ValidationError as e:
        print(f"✗ Pod validation failed (expected): {e}")


def demo_auto_validation():
    """Demonstrate automatic validation during create"""
    print_section(title="Auto-validation During Create")

    # Get a fake client for demo
    client = get_client(fake=True)

    # Create pod with auto-validation enabled
    print("1. Creating pod with auto-validation enabled...")
    pod = Pod(
        client=client,
        name="auto-validated-pod",
        namespace="default",
        containers=[{"name": "nginx", "image": "nginx:latest"}],
        schema_validation_enabled=True,  # Enable auto-validation
    )

    try:
        pod.create()
        print("✓ Pod created successfully (validation passed)")
    except ValidationError as e:
        print(f"✗ Pod creation failed due to validation: {e}")

    # Try to create invalid pod with auto-validation
    print("\n2. Creating invalid pod with auto-validation...")
    invalid_pod = Pod(
        client=client,
        name="invalid-auto-pod",
        namespace="default",
        containers=[{"name": "nginx"}],  # Missing image
        schema_validation_enabled=True,
    )

    try:
        invalid_pod.create()
        print("✓ Pod created (unexpected!)")
    except ValidationError as e:
        print(f"✗ Pod creation blocked by validation (expected): {e}")


def demo_dict_validation():
    """Demonstrate validating resource dictionaries"""
    print_section(title="Dictionary Validation")

    # Valid deployment dictionary
    print("1. Validating a correct deployment configuration...")
    deployment_dict = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": "nginx-deployment", "namespace": "default"},
        "spec": {
            "replicas": 3,
            "selector": {"matchLabels": {"app": "nginx"}},
            "template": {
                "metadata": {"labels": {"app": "nginx"}},
                "spec": {"containers": [{"name": "nginx", "image": "nginx:1.21", "ports": [{"containerPort": 80}]}]},
            },
        },
    }

    try:
        Deployment.validate_dict(resource_dict=deployment_dict)
        print("✓ Deployment configuration is valid!")
    except ValidationError as e:
        print(f"✗ Deployment validation failed: {e}")

    # Invalid deployment (wrong type for replicas)
    print("\n2. Validating deployment with wrong type...")
    invalid_deployment = deployment_dict.copy()
    invalid_deployment["spec"]["replicas"] = "three"  # Should be integer

    try:
        Deployment.validate_dict(resource_dict=invalid_deployment)
        print("✓ Deployment configuration is valid (unexpected!)")
    except ValidationError as e:
        print(f"✗ Deployment validation failed (expected): {e}")


def demo_different_resources():
    """Demonstrate validation with different resource types"""
    print_section(title="Validation with Different Resources")

    # Service validation
    print("1. Validating a Service...")
    service = Service(
        name="nginx-service",
        namespace="default",
        selector={"app": "nginx"},
        ports=[{"port": 80, "targetPort": 80, "protocol": "TCP"}],
    )

    try:
        service.validate()
        print("✓ Service validation passed!")
    except ValidationError as e:
        print(f"✗ Service validation failed: {e}")

    # ConfigMap validation
    print("\n2. Validating a ConfigMap...")
    config_map = ConfigMap(
        name="app-config",
        namespace="default",
        data={"app.properties": "debug=true\nport=8080", "database.url": "postgresql://localhost:5432/mydb"},
    )

    try:
        config_map.validate()
        print("✓ ConfigMap validation passed!")
    except ValidationError as e:
        print(f"✗ ConfigMap validation failed: {e}")


def demo_performance():
    """Demonstrate validation performance with caching"""
    print_section(title="Validation Performance")

    # Create multiple pods for performance testing
    pods = []
    for i in range(5):
        pods.append(
            Pod(name=f"perf-test-pod-{i}", namespace="default", containers=[{"name": "nginx", "image": "nginx:latest"}])
        )

    # First validation (loads and caches schema)
    print("First validation (loads schema)...")
    start = time.time()
    pods[0].validate()
    first_time = time.time() - start
    print(f"  Time: {first_time * 1000:.2f}ms")

    # Subsequent validations (uses cached schema)
    print("\nSubsequent validations (uses cache)...")
    times = []
    for i, pod in enumerate(pods[1:], 1):
        start = time.time()
        pod.validate()
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"  Pod {i}: {elapsed * 1000:.2f}ms")

    avg_cached = sum(times) / len(times)
    print(f"\nAverage cached validation time: {avg_cached * 1000:.2f}ms")
    print(f"Speed improvement: {first_time / avg_cached:.1f}x faster")


def demo_error_details():
    """Demonstrate detailed error messages"""
    print_section(title="Detailed Error Messages")

    # Create pod with multiple errors
    print("Creating a pod with multiple validation errors...")
    pod = Pod(
        name="invalid-name-",  # Names must start and end with alphanumeric, can only contain lowercase alphanumeric or hyphens
        namespace="default",
        containers=[
            {
                "name": "container@1",  # Invalid character in name
                "image": "nginx",
            },
            {
                "name": "container2"
                # Missing required 'image' field
            },
        ],
    )

    try:
        pod.validate()
        print("✓ Pod validation passed (unexpected!)")
    except ValidationError as e:
        print(f"✗ Validation errors found:\n{e}")


def main():
    """Run all validation demos"""
    print("\n" + "=" * 60)
    print(" OpenShift Python Wrapper - Schema Validation Demo")
    print("=" * 60)

    demos = [
        demo_basic_validation,
        demo_auto_validation,
        demo_dict_validation,
        demo_different_resources,
        demo_performance,
        demo_error_details,
    ]

    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\nError in demo: {e}")

    print("\n" + "=" * 60)
    print(" Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
