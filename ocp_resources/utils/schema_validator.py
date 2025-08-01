"""Schema validation utilities for OpenShift Python Wrapper.

This module provides shared schema validation functionality that can be used by both
the Resource class and the fake Kubernetes client.
"""

import json
from importlib.resources import files
from pathlib import Path
from typing import Any

import jsonschema
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class SchemaValidator:
    """Shared schema validator for resource validation."""

    # Class-level caches shared across all instances
    _mappings_data: dict[str, Any] | None = None
    _definitions_data: dict[str, Any] | None = None
    _schema_cache: dict[str, dict[str, Any]] = {}

    @classmethod
    def load_mappings_data(cls) -> bool:
        """
        Load the resource mappings and definitions data.

        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if cls._mappings_data is not None and cls._definitions_data is not None:
            return True

        try:
            schema_dir = files("class_generator") / "schema"
            mappings_path = schema_dir / "__resources-mappings.json"
            definitions_path = schema_dir / "_definitions.json"

            # Read the files
            mappings_data = mappings_path.read_text()
            definitions_data = definitions_path.read_text()
        except (ImportError, ModuleNotFoundError):
            # Fallback to file system path for development
            schema_dir = Path(__file__).parent.parent.parent / "class_generator" / "schema"
            mappings_file = schema_dir / "__resources-mappings.json"
            definitions_file = schema_dir / "_definitions.json"

            if not mappings_file.exists() or not definitions_file.exists():
                LOGGER.warning(f"Schema files not found in {schema_dir}")
                return False

            try:
                with open(mappings_file, "r") as f:
                    mappings_data = f.read()
                with open(definitions_file, "r") as f:
                    definitions_data = f.read()
            except Exception as e:
                LOGGER.error(f"Failed to read schema files: {e}")
                return False

        # Parse the JSON data
        try:
            cls._mappings_data = json.loads(mappings_data)
            definitions_json = json.loads(definitions_data)
            # Extract the definitions from the top-level "definitions" key
            cls._definitions_data = definitions_json.get("definitions", {})
            return True
        except json.JSONDecodeError as e:
            LOGGER.error(f"Failed to parse schema JSON: {e}")
            return False

    @classmethod
    def get_mappings_data(cls) -> dict[str, Any] | None:
        """
        Get the resource mappings data.

        This method provides public access to the mappings data while maintaining
        encapsulation. It ensures the data is loaded before returning.

        Returns:
            dict[str, Any] | None: The mappings data or None if not loaded
        """
        # Ensure data is loaded
        if cls._mappings_data is None:
            cls.load_mappings_data()
        return cls._mappings_data

    @classmethod
    def get_definitions_data(cls) -> dict[str, Any] | None:
        """
        Get the resource definitions data.

        This method provides public access to the definitions data while maintaining
        encapsulation. It ensures the data is loaded before returning.

        Returns:
            dict[str, Any] | None: The definitions data or None if not loaded
        """
        # Ensure data is loaded
        if cls._definitions_data is None:
            cls.load_mappings_data()
        return cls._definitions_data

    @classmethod
    def load_schema(cls, kind: str, api_group: str | None = None) -> dict[str, Any] | None:
        """
        Load OpenAPI schema for a resource kind from the mappings file.

        Args:
            kind: The resource kind (e.g., "Pod", "Deployment")
            api_group: Optional API group to disambiguate resources with same kind

        Returns:
            Schema dict or None if not found
        """
        # Check cache first
        cache_key = f"{api_group}:{kind}" if api_group else kind
        if cache_key in cls._schema_cache:
            return cls._schema_cache[cache_key]

        # Load the mappings and definitions files if not already loaded
        if not cls.load_mappings_data():
            return None

        # Type guard - after load_mappings_data() succeeds, these cannot be None
        if cls._mappings_data is None or cls._definitions_data is None:
            return None

        # Look up schema by lowercase kind
        kind_lower = kind.lower()
        schemas = cls._mappings_data.get(kind_lower)

        if not schemas or not isinstance(schemas, list) or len(schemas) == 0:
            LOGGER.warning(f"No schema found for {kind} (looked up as '{kind_lower}')")
            return None

        # If there's only one schema or no api_group specified, use the first one
        if len(schemas) == 1 or not api_group:
            schema = schemas[0]
        else:
            # Multiple schemas exist, need to find the right one by API group
            schema = None
            for candidate in schemas:
                # Check x-kubernetes-group-version-kind
                gvk_list = candidate.get("x-kubernetes-group-version-kind", [])
                for gvk in gvk_list:
                    if gvk.get("group") == api_group:
                        schema = candidate
                        break
                if schema:
                    break

            if not schema:
                LOGGER.warning(
                    f"Could not find schema for {kind} with API group {api_group}. "
                    f"Available groups: {[gvk.get('group') for s in schemas for gvk in s.get('x-kubernetes-group-version-kind', [])]}"
                )
                # Fallback to first schema
                schema = schemas[0]

        # Create a resolver for $ref resolution
        try:
            resolver = jsonschema.RefResolver(
                base_uri="", referrer=schema, store={"": {"definitions": cls._definitions_data}}
            )

            # Resolve all $ref in the schema
            resolved_schema = cls._resolve_refs(schema, resolver)

            # Cache the resolved schema
            cls._schema_cache[cache_key] = resolved_schema
            return resolved_schema
        except Exception as e:
            LOGGER.warning(f"Failed to load schema for {kind}: {e}")
            return None

    @classmethod
    def _resolve_refs(cls, obj: Any, resolver: Any) -> Any:
        """
        Recursively resolve all $ref references in a schema object.

        Args:
            obj: The schema object to resolve
            resolver: jsonschema RefResolver instance

        Returns:
            The resolved schema object
        """
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref = obj["$ref"]
                # Handle internal references - both old and new formats
                if (
                    ref.startswith("#/definitions/")
                    or ref.startswith("#/components/schemas/")
                    or ref.startswith("/components/schemas/")
                ):
                    # Extract the definition name
                    if ref.startswith("#/definitions/"):
                        definition_name = ref[14:]  # Remove "#/definitions/"
                    elif ref.startswith("#/components/schemas/"):
                        definition_name = ref[21:]  # Remove "#/components/schemas/"
                    else:
                        definition_name = ref[20:]  # Remove "/components/schemas/"

                    # Type guard for mypy
                    if cls._definitions_data is not None and definition_name in cls._definitions_data:
                        # Return the resolved definition (and resolve any refs within it)
                        return cls._resolve_refs(cls._definitions_data[definition_name], resolver)
                    else:
                        LOGGER.warning(f"Definition not found: {definition_name}")
                        return obj
                else:
                    # Use the resolver for other types of references
                    try:
                        url, resolved = resolver.resolve(ref)
                        return cls._resolve_refs(resolved, resolver)
                    except Exception as e:
                        LOGGER.warning(f"Failed to resolve $ref '{ref}': {e}")
                        return obj
            else:
                # Recursively resolve refs in all values
                return {k: cls._resolve_refs(v, resolver) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [cls._resolve_refs(item, resolver) for item in obj]
        else:
            return obj

    @classmethod
    def validate(cls, resource_dict: dict[str, Any], kind: str, api_group: str | None = None) -> None:
        """
        Validate a resource dictionary against its OpenAPI schema.

        Args:
            resource_dict: The resource dictionary to validate
            kind: The resource kind (e.g., "Pod", "Deployment")
            api_group: Optional API group to disambiguate resources with same kind

        Raises:
            jsonschema.ValidationError: If validation fails
        """
        schema = cls.load_schema(kind=kind, api_group=api_group)
        if not schema:
            LOGGER.debug(f"No schema found for {kind}, skipping validation")
            return

        try:
            jsonschema.validate(instance=resource_dict, schema=schema)
        except jsonschema.ValidationError:
            # Re-raise as-is so caller can format the error
            raise

    @classmethod
    def format_validation_error(
        cls, error: jsonschema.ValidationError, kind: str, name: str, api_group: str | None = None
    ) -> str:
        """
        Format a validation error into a user-friendly message.

        Args:
            error: The jsonschema validation error
            kind: Resource kind
            name: Resource name
            api_group: Optional API group

        Returns:
            Formatted error message
        """
        # Build the resource identifier
        if api_group:
            resource_id = f"{api_group}/{kind}/{name}"
        else:
            resource_id = f"{kind}/{name}"

        # Build the field path from the error
        path_parts = []
        for i, part in enumerate(error.absolute_path):
            if isinstance(part, int):
                path_parts.append(f"[{part}]")
            else:
                if path_parts and not path_parts[-1].endswith("]"):
                    path_parts.append(".")
                elif path_parts and path_parts[-1].endswith("]") and i > 0:
                    path_parts.append(".")
                path_parts.append(str(part))

        field_path = "".join(path_parts) if path_parts else "root"

        # Build the error message
        message_parts = [f"Resource validation failed for {resource_id}"]
        message_parts.append(f"Field: {field_path}")
        message_parts.append(f"Error: {error.message}")

        # Add schema context if available
        if error.validator == "required":
            message_parts.append(f"Required fields: {error.validator_value}")
        elif error.validator == "enum":
            message_parts.append(f"Allowed values: {error.validator_value}")
        elif error.validator == "type":
            message_parts.append(f"Expected type: {error.validator_value}")

        return "\n  ".join(message_parts)

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the schema cache (useful for testing).

        This only clears the _schema_cache which contains resolved schemas.
        It does not clear _mappings_data or _definitions_data which are
        loaded from files.
        """
        cls._schema_cache.clear()
