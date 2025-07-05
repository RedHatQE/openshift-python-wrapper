"""
Fake Kubernetes DynamicClient for Testing

This package provides a comprehensive fake implementation of the Kubernetes DynamicClient
that can be used as a drop-in replacement for unit testing.

Features:
- Complete CRUD operations (Create, Read, Update, Delete, Patch, Replace)
- Resource discovery and auto-generation for any resource kind
- Label and field selectors
- Watch functionality
- Automatic event generation
- Realistic status simulation
- Universal resource support (works with any Kubernetes/OpenShift resource)

Usage:
    from fake_kubernetes_client import FakeDynamicClient

    client = FakeDynamicClient()

    # Use exactly like real DynamicClient
    pod_api = client.resources.get(kind="Pod", api_version="v1")
    pod = pod_api.create(body=pod_manifest, namespace="default")
"""

from .fake_dynamic_client import (
    FakeDynamicClient,
    create_fake_client_with_resources,
    create_fake_client_with_custom_resources,
    FakeResourceField,
    FakeResourceInstance,
    FakeResourceRegistry,
    FakeResourceStorage,
)

__all__ = [
    "FakeDynamicClient",
    "create_fake_client_with_resources",
    "create_fake_client_with_custom_resources",
    "FakeResourceField",
    "FakeResourceInstance",
    "FakeResourceRegistry",
    "FakeResourceStorage",
]

# Main export for easy importing
__version__ = "1.0.0"
