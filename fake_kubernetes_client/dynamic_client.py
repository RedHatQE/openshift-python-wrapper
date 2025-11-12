"""FakeDynamicClient implementation for fake Kubernetes client"""

from typing import Any

from fake_kubernetes_client.exceptions import NotFoundError
from fake_kubernetes_client.kubernetes_client import FakeKubernetesClient
from fake_kubernetes_client.resource_field import FakeResourceField
from fake_kubernetes_client.resource_instance import FakeResourceInstance
from fake_kubernetes_client.resource_manager import FakeResourceManager
from fake_kubernetes_client.resource_registry import FakeResourceRegistry
from fake_kubernetes_client.resource_storage import FakeResourceStorage


class FakeDynamicClient:
    """Fake implementation of kubernetes.dynamic.DynamicClient"""

    def __init__(self, client: FakeKubernetesClient | None = None) -> None:
        # Distinguish between creating a new client vs using an existing one
        if client is None:
            # Create a new client with circular reference
            self.client = FakeKubernetesClient(dynamic_client=self)
        else:
            # Use the provided client without modifying its dynamic_client reference
            # This respects any intentional null or existing value
            self.client = client

        self.configuration = self.client.configuration
        self.storage = FakeResourceStorage()
        self.registry = FakeResourceRegistry()
        self._resources_manager = FakeResourceManager(client=self)

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

    def request(self, _method: str, _path: str, _body: Any = None, **_kwargs: Any) -> FakeResourceField:
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
        # Get the namespace resource definition
        ns_resource = self.resources.get(api_version="v1", kind="Namespace")

        # Check if namespace exists
        try:
            return ns_resource.get(name=namespace)
        except NotFoundError:
            # Create namespace if it doesn't exist
            body = {
                "metadata": {"name": namespace},
                "spec": {"finalizers": ["kubernetes"]},
            }
            return ns_resource.create(body=body)

    def api_client(self) -> FakeKubernetesClient:
        """Get the underlying API client"""
        return self.client

    def register_resources(self, resources: dict[str, Any] | list[dict[str, Any]]) -> None:
        """
        Register custom resources dynamically.

        This method allows you to add custom resource definitions to the fake client,
        which is useful for testing with Custom Resource Definitions (CRDs) or
        resources that are not included in the default schema.

        Args:
            resources: Either a single resource definition dict or a list of resource definitions.
                      Each resource definition should contain:
                      - kind: Resource kind (required)
                      - api_version: API version without group (required)
                      - group: API group (optional, empty string for core resources)
                      - namespaced: Whether resource is namespaced (optional, defaults to True)
                      - plural: Plural name (optional, will be generated if not provided)
                      - singular: Singular name (optional, defaults to lowercase kind)

        Example:
            # Register a single custom resource
            client.register_resources({
                "kind": "MyCustomResource",
                "api_version": "v1alpha1",
                "group": "example.com",
                "namespaced": True
            })

            # Register multiple resources
            client.register_resources([
                {
                    "kind": "MyApp",
                    "api_version": "v1",
                    "group": "apps.example.com",
                    "namespaced": True,
                    "plural": "myapps"
                },
                {
                    "kind": "MyConfig",
                    "api_version": "v1beta1",
                    "group": "config.example.com",
                    "namespaced": False  # cluster-scoped
                }
            ])

            # After registration, use the resources normally
            myapp_api = client.resources.get(
                api_version="apps.example.com/v1",
                kind="MyApp"
            )
            myapp_api.create(body={...}, namespace="default")
        """
        self.registry.register_resources(resources=resources)

    def get(self, resource: Any, *args: Any, **kwargs: Any) -> Any:
        """Get resources based on resource definition"""
        # Extract resource definition from FakeResourceField if needed
        if hasattr(resource, "data"):
            resource_def = resource.data
        else:
            resource_def = resource

        # Create a resource instance for this resource type
        resource_instance = FakeResourceInstance(resource_def=resource_def, storage=self.storage, client=self)

        # Call get on the resource instance to list resources
        return resource_instance.get(*args, **kwargs)
