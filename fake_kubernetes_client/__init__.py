"""Fake Kubernetes client for testing"""

from fake_kubernetes_client.configuration import FakeConfiguration
from fake_kubernetes_client.dynamic_client import FakeDynamicClient
from fake_kubernetes_client.exceptions import (
    ApiException,
    ConflictError,
    NotFoundError,
)
from fake_kubernetes_client.kubernetes_client import FakeKubernetesClient
from fake_kubernetes_client.resource_field import FakeResourceField
from fake_kubernetes_client.resource_instance import FakeResourceInstance
from fake_kubernetes_client.resource_manager import FakeResourceManager
from fake_kubernetes_client.resource_registry import FakeResourceRegistry
from fake_kubernetes_client.resource_storage import FakeResourceStorage

__all__ = [
    "FakeConfiguration",
    "FakeDynamicClient",
    "FakeKubernetesClient",
    "FakeResourceField",
    "FakeResourceInstance",
    "FakeResourceRegistry",
    "FakeResourceStorage",
    "FakeResourceManager",
    "ApiException",
    "NotFoundError",
    "ConflictError",
]
