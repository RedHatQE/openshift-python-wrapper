"""FakeResourceField implementation for fake Kubernetes client"""

import copy
from collections.abc import Iterator
from typing import Any


class FakeResourceField:
    """Fake implementation of kubernetes.dynamic.resource.ResourceField"""

    def __init__(self, data: dict[str, Any] | None) -> None:
        self._data = data if data is not None else {}

    def __getattribute__(self, name: str) -> Any:
        # ONLY handle essential internal attributes and methods here
        # Let __getattr__ handle all dynamic attribute access
        if name.startswith("_") or name in {"to_dict", "keys", "values", "get"}:
            return object.__getattribute__(self, name)

        # Special case: handle 'items' in __getattribute__ to override method lookup
        if name == "items":
            try:
                data = object.__getattribute__(self, "_data")
                if "items" in data:
                    value = data["items"]
                    if isinstance(value, list):
                        return [FakeResourceField(item) if isinstance(item, dict) else item for item in value]
                    return value
            except AttributeError:
                pass
            # Fall back to the method if no items data
            return object.__getattribute__(self, name)

        # For all other attributes, let __getattr__ handle it
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getattr__(self, name: str) -> Any:
        # This is called ONLY when __getattribute__ raises AttributeError
        # Handle all dynamic attribute access here

        # Direct access to _data without using hasattr (avoids recursion)
        try:
            data = object.__getattribute__(self, "_data")
        except AttributeError:
            data = {}

        # For resource definition access, return simple values for common attributes
        # This ensures compatibility with ocp_resources code that expects strings
        if name in ["api_version", "group_version", "kind", "plural", "singular", "group", "version"]:
            return data.get(name, "")

        # Handle general data access
        value = data.get(name)
        if value is None:
            return FakeResourceField(data={})
        elif isinstance(value, dict):
            return FakeResourceField(data=value)
        elif isinstance(value, list):
            return [FakeResourceField(data=item) if isinstance(item, dict) else item for item in value]
        else:
            return value

    def __getitem__(self, key: str) -> Any:
        value = self._data.get(key)
        if value is None:
            return FakeResourceField(data={})
        elif isinstance(value, dict):
            return FakeResourceField(data=value)
        elif isinstance(value, list):
            return [FakeResourceField(data=item) if isinstance(item, dict) else item for item in value]
        else:
            return value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __bool__(self) -> bool:
        return bool(self._data)

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return f"FakeResourceField({self._data})"

    def get(self, key: str, default: Any = None) -> Any:
        value = self._data.get(key, default)
        if isinstance(value, dict) and value != default:
            return FakeResourceField(data=value)
        return value

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return copy.deepcopy(self._data)

    def keys(self) -> Any:
        """Get dictionary keys"""
        return self._data.keys()

    def values(self) -> Any:
        """Get dictionary values"""
        return self._data.values()

    def items(self) -> Any:
        """Get dictionary items - but handle special case where 'items' is data"""
        # If 'items' key exists in data, return that instead of dict.items()
        if "items" in self._data:
            value = self._data["items"]
            if isinstance(value, list):
                return [FakeResourceField(data=item) if isinstance(item, dict) else item for item in value]
            return value
        # Otherwise return dict.items()
        return self._data.items()

    def __iter__(self) -> Iterator[str]:
        """Make it iterable like a dictionary"""
        return iter(self._data)

    def __len__(self) -> int:
        """Get length like a dictionary"""
        return len(self._data)
