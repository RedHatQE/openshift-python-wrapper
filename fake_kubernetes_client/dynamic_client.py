"""FakeDynamicClient implementation for fake Kubernetes client"""

from typing import Any, Union

from fake_kubernetes_client.kubernetes_client import FakeKubernetesClient
from fake_kubernetes_client.resource_field import FakeResourceField
from fake_kubernetes_client.resource_instance import FakeResourceInstance
from fake_kubernetes_client.resource_manager import FakeResourceManager
from fake_kubernetes_client.resource_registry import FakeResourceRegistry
from fake_kubernetes_client.resource_storage import FakeResourceStorage


class FakeDynamicClient:
    """Fake implementation of kubernetes.dynamic.DynamicClient"""

    def __init__(self, client: Union[FakeKubernetesClient, None] = None) -> None:
        self.client = client or FakeKubernetesClient(dynamic_client=self)
        self.configuration = self.client.configuration
        self.storage = FakeResourceStorage()
        self.registry = FakeResourceRegistry()
        self._resources_manager = FakeResourceManager(client=self)

        # Set dynamic client reference in client if not already set
        if not self.client.dynamic_client:
            self.client.dynamic_client = self

    @property
    def resources(self) -> FakeResourceManager:
        """Get the resource manager"""
        return self._resources_manager

    def get_openapi_spec(self) -> dict[str, Any]:
        """Get OpenAPI spec (minimal fake implementation)"""
        return {
            "openapi": "3.0.0",
            "info": {"title": "Kubernetes", "version": "v1.29.0"},
            "paths": {},
        }

    def request(self, method: str, path: str, body: Any = None, **kwargs: Any) -> FakeResourceField:
        """Make a raw request (fake implementation)"""
        # Minimal implementation - just return empty response
        return FakeResourceField(data={})

    def version(self) -> dict[str, Any]:
        """Get server version"""
        return {
            "major": "1",
            "minor": "29",
            "gitVersion": "v1.29.0",
            "gitCommit": "fake",
            "gitTreeState": "clean",
            "buildDate": "2024-01-01T00:00:00Z",
            "goVersion": "go1.21.0",
            "compiler": "gc",
            "platform": "linux/amd64",
        }

    def ensure_namespace(self, namespace: str) -> FakeResourceField:
        """Ensure namespace exists (fake implementation)"""
        # Check if namespace exists
        try:
            ns_resource = self.resources.get(api_version="v1", kind="Namespace")
            return ns_resource.get(name=namespace)
        except Exception:
            # Create namespace
            body = {
                "metadata": {"name": namespace},
                "spec": {"finalizers": ["kubernetes"]},
            }
            return ns_resource.create(body=body)

    def api_client(self) -> FakeKubernetesClient:
        """Get the underlying API client"""
        return self.client


def create_fake_client_with_resources(resources: list[dict[str, Any]]) -> FakeDynamicClient:
    """Create a fake client with pre-populated resources"""
    client = FakeDynamicClient()

    for resource in resources:
        # Extract resource info
        api_version = resource.get("apiVersion", "v1")
        kind = resource.get("kind", "")
        metadata = resource.get("metadata", {})
        name = metadata.get("name", "")
        namespace = metadata.get("namespace")

        if not kind or not name:
            continue

        # Get resource definition
        resource_def = client.registry.get_resource_definition(kind=kind, api_version=api_version)
        if not resource_def:
            # Skip unknown resources
            continue

        # Create resource instance and store
        resource_instance = FakeResourceInstance(resource_def=resource_def, storage=client.storage, client=client)
        try:
            resource_instance.create(body=resource, namespace=namespace)
        except Exception:
            # Skip if creation fails (e.g., duplicate)
            pass

    return client
