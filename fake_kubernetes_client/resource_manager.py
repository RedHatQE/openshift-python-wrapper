"""FakeResourceManager implementation for fake Kubernetes client"""

from typing import TYPE_CHECKING, Any, Union

from fake_kubernetes_client.exceptions import ResourceNotFoundError
from fake_kubernetes_client.resource_field import FakeResourceField
from fake_kubernetes_client.resource_instance import FakeResourceInstance

if TYPE_CHECKING:
    from fake_kubernetes_client.dynamic_client import FakeDynamicClient


class FakeResourceManager:
    """Manager for resource discovery and access"""

    def __init__(self, client: "FakeDynamicClient") -> None:
        self.client = client
        self.registry = client.registry
        self.storage = client.storage

    def get(
        self,
        api_version: Union[str, None] = None,
        kind: Union[str, None] = None,
        name: Union[str, None] = None,
        singular_name: Union[str, None] = None,
        namespaced: Union[bool, None] = None,
        group: Union[str, None] = None,
        version: Union[str, None] = None,
        preferred: Union[bool, None] = None,
        prefix: Union[str, None] = None,
        **kwargs: Any,
    ) -> FakeResourceInstance:
        """Get resource instance for performing operations"""
        # Construct API version if group and version provided
        if group is not None and version is not None:
            # Explicitly check if group is not empty string
            if group != "":
                api_version = f"{group}/{version}"
            else:
                # If group is empty string, use version alone (core API group)
                api_version = version

        # Find resource definition
        resource_def = None

        if kind and api_version:
            resource_def = self.registry.get_resource_definition(kind=kind, api_version=api_version)
        elif name and api_version:  # 'name' is the plural
            resource_def = self.registry.get_resource_definition_by_plural(plural=name, api_version=api_version)
        elif kind:
            # Get all definitions for this kind
            definitions = self.registry.get_resource_definitions(kind=kind)
            if definitions:
                # If preferred is True, try to find preferred version
                if preferred:
                    # Simple logic: prefer stable versions (v1 > v1beta1 > v1alpha1)
                    for def_ in definitions:
                        if def_["version"] == "v1":
                            resource_def = def_
                            break
                    if not resource_def:
                        resource_def = definitions[0]
                else:
                    resource_def = definitions[0]

        if not resource_def:
            raise ResourceNotFoundError(f"Resource not found: api_version={api_version}, kind={kind}, name={name}")

        return FakeResourceInstance(resource_def=resource_def, storage=self.storage, client=self.client)

    def search(
        self, group: Union[str, None] = None, kind: Union[str, None] = None, **kwargs: Any
    ) -> list[FakeResourceField]:
        """Search for resource definitions"""
        # Delegate to registry's search method
        return self.registry.search(kind=kind, group=group, **kwargs)
