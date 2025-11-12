"""FakeResourceStorage implementation for fake Kubernetes client"""

import copy
from collections import defaultdict
from typing import Any


class FakeResourceStorage:
    """In-memory storage for Kubernetes resources"""

    def __init__(self) -> None:
        # Storage structure: {api_version: {kind: {namespace: {name: resource}}}}
        self.resources: defaultdict[str, defaultdict[str, defaultdict[str | None, dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(dict))
        )

    def store_resource(
        self, kind: str, api_version: str, name: str, namespace: str | None, resource: dict[str, Any]
    ) -> None:
        """Store a resource"""
        self.resources[api_version][kind][namespace][name] = copy.deepcopy(resource)

    def get_resource(self, kind: str, api_version: str, name: str, namespace: str | None) -> dict[str, Any] | None:
        """Get a specific resource"""
        api_resources = self.resources.get(api_version)
        if not api_resources:
            return None
        kind_resources = api_resources.get(kind)
        if not kind_resources:
            return None
        namespace_resources = kind_resources.get(namespace)
        if not namespace_resources:
            return None
        resource = namespace_resources.get(name)
        return copy.deepcopy(resource) if resource else None

    def list_resources(
        self,
        kind: str,
        api_version: str,
        namespace: str | None = None,
        label_selector: str | None = None,
        field_selector: str | None = None,
    ) -> list[dict[str, Any]]:
        """List resources with optional filtering"""
        resources: list[dict[str, Any]] = []

        api_resources = self.resources.get(api_version)
        if not api_resources:
            return resources

        kind_resources = api_resources.get(kind)
        if not kind_resources:
            return resources

        if namespace is not None:
            # List resources in specific namespace
            namespace_resources = kind_resources.get(namespace, {})
            resources = list(namespace_resources.values())
        else:
            # List resources across all namespaces
            for ns_resources in kind_resources.values():
                resources.extend(ns_resources.values())

        # Apply label selector filter
        if label_selector:
            resources = self._filter_by_labels(resources, label_selector)

        # Apply field selector filter
        if field_selector:
            resources = self._filter_by_fields(resources, field_selector)

        return [copy.deepcopy(r) for r in resources]

    def delete_resource(self, kind: str, api_version: str, name: str, namespace: str | None) -> dict[str, Any] | None:
        """Delete a resource"""
        resource = self.get_resource(kind, api_version, name, namespace)
        if resource:
            del self.resources[api_version][kind][namespace][name]
            # Clean up empty structures
            if not self.resources[api_version][kind][namespace]:
                del self.resources[api_version][kind][namespace]
            if not self.resources[api_version][kind]:
                del self.resources[api_version][kind]
            if not self.resources[api_version]:
                del self.resources[api_version]
        return resource

    def _filter_by_labels(self, resources: list[dict[str, Any]], label_selector: str) -> list[dict[str, Any]]:
        """Filter resources by label selector"""
        filtered = []
        for resource in resources:
            labels = resource.get("metadata", {}).get("labels", {})
            if self._matches_label_selector(labels, label_selector):
                filtered.append(resource)
        return filtered

    def _matches_label_selector(self, labels: dict[str, str], selector: str) -> bool:
        """Check if labels match selector (simplified implementation)"""
        # Handle simple equality selectors (key=value)
        parts = selector.split(",")
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                if labels.get(key.strip()) != value.strip():
                    return False
            elif "!=" in part:
                key, value = part.split("!=", 1)
                if labels.get(key.strip()) == value.strip():
                    return False
            else:
                # Just key presence check
                if part.strip() not in labels:
                    return False
        return True

    def _filter_by_fields(self, resources: list[dict[str, Any]], field_selector: str) -> list[dict[str, Any]]:
        """Filter resources by field selector"""
        filtered = []
        for resource in resources:
            if self._matches_field_selector(resource, field_selector):
                filtered.append(resource)
        return filtered

    def _matches_field_selector(self, resource: dict[str, Any], selector: str) -> bool:
        """Check if resource matches field selector"""
        # Handle simple field selectors (field.path=value or field.path==value)
        parts = selector.split(",")
        for part in parts:
            if "==" in part:
                # Handle double equals
                field_path, selector_value = part.split("==", 1)
                field_value = self._get_field_value(resource, field_path.strip())
                if not self._compare_field_values(field_value, selector_value.strip()):
                    return False
            elif "=" in part:
                # Handle single equals
                field_path, selector_value = part.split("=", 1)
                field_value = self._get_field_value(resource, field_path.strip())
                if not self._compare_field_values(field_value, selector_value.strip()):
                    return False
        return True

    def _compare_field_values(self, field_value: Any, selector_value: str) -> bool:
        """
        Compare field value with selector value using type-aware comparison.

        Attempts to parse the selector value to match the field value's type.
        """
        # Handle missing fields - they don't match any selector
        if field_value is NotImplemented:
            return False

        # Handle None/null values
        if field_value is None:
            return selector_value.lower() in ("none", "null", "")

        # Handle boolean values
        if isinstance(field_value, bool):
            if selector_value.lower() == "true":
                return field_value is True
            elif selector_value.lower() == "false":
                return field_value is False
            else:
                return False

        # Handle numeric values
        if isinstance(field_value, (int, float)):
            try:
                # Try to parse as number
                if "." in selector_value:
                    return field_value == float(selector_value)
                else:
                    return field_value == int(selector_value)
            except ValueError:
                # If parsing fails, fall back to string comparison
                return str(field_value) == selector_value

        # Handle string values (default case)
        return str(field_value) == selector_value

    def _get_field_value(self, obj: dict[str, Any], path: str) -> Any:
        """Get value from nested dictionary using dot notation"""
        current = obj
        parts = path.split(".")

        for _i, part in enumerate(parts):
            if isinstance(current, dict):
                if part not in current:
                    # Return a sentinel value to indicate the field doesn't exist
                    return NotImplemented
                current = current[part]
            else:
                return NotImplemented

        return current
