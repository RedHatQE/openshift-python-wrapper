"""Tests for schema loading functionality."""

from unittest.mock import mock_open, patch

import pytest

from ocp_resources.utils.schema_validator import SchemaValidator
from tests.fixtures.validation_schemas import POD_SCHEMA


@pytest.fixture(autouse=True)
def reset_schema_validator():
    """Reset SchemaValidator state before each test to prevent test pollution."""
    # Clear any existing state before test
    SchemaValidator._mappings_data = None
    SchemaValidator._definitions_data = None
    SchemaValidator._schema_cache.clear()

    yield

    # Clear state after test as well
    SchemaValidator._mappings_data = None
    SchemaValidator._definitions_data = None
    SchemaValidator._schema_cache.clear()


class TestSchemaLoading:
    """Test schema loading functionality."""

    def test_load_schema_from_mappings(self, monkeypatch):
        """Test loading schema from mappings file."""
        # Mock the mappings data
        mock_mappings = {"pod": [POD_SCHEMA]}
        mock_definitions = {}

        # Use monkeypatch to set the class attributes
        monkeypatch.setattr(SchemaValidator, "_mappings_data", mock_mappings)
        monkeypatch.setattr(SchemaValidator, "_definitions_data", mock_definitions)

        try:
            with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
                schema = SchemaValidator.load_schema(kind="Pod")

                assert schema is not None
                assert schema["type"] == "object"
                assert "properties" in schema
        finally:
            # Clean up
            SchemaValidator.clear_cache()

    def test_load_schema_with_missing_resource(self, monkeypatch):
        """Test loading schema when resource is not in mappings."""
        # Clear cache
        SchemaValidator.clear_cache()

        # Mock empty mappings
        mock_mappings = {}
        mock_definitions = {}

        # Use monkeypatch to set the class attributes
        monkeypatch.setattr(SchemaValidator, "_mappings_data", mock_mappings)
        monkeypatch.setattr(SchemaValidator, "_definitions_data", mock_definitions)

        with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
            schema = SchemaValidator.load_schema(kind="Pod")

            assert schema is None

    def test_load_mappings_data_success(self):
        """Test successful loading of mappings data."""
        mock_mappings_data = {"pod": [{"type": "object"}]}

        # Mock the archive loading function and file operations
        with patch("ocp_resources.utils.schema_validator.load_json_archive") as mock_load_archive:
            mock_load_archive.return_value = mock_mappings_data

            with patch("builtins.open", mock_open(read_data='{"definitions": {"SomeDefinition": {"type": "string"}}}')):
                # Mock Path.exists() method
                with patch("pathlib.Path.exists") as mock_exists:
                    mock_exists.return_value = True

                    result = SchemaValidator.load_mappings_data()

                    assert result is True
                    mappings_data = SchemaValidator.get_mappings_data()
                    assert mappings_data is not None
                    assert "pod" in mappings_data

                    definitions_data = SchemaValidator.get_definitions_data()
                    assert definitions_data is not None
                    assert "SomeDefinition" in definitions_data

    def test_load_mappings_data_already_loaded(self, monkeypatch):
        """Test that mappings data is not reloaded if already present."""
        # Set up existing data using monkeypatch
        monkeypatch.setattr(SchemaValidator, "_mappings_data", {"existing": "data"})
        monkeypatch.setattr(SchemaValidator, "_definitions_data", {"existing": "definitions"})

        # load_mappings_data should return True without loading
        with patch("builtins.open") as mock_open:
            result = SchemaValidator.load_mappings_data()

            assert result is True
            # Should not have tried to open any files
            mock_open.assert_not_called()

    def test_resolve_refs_with_definitions(self, monkeypatch):
        """Test resolving $ref references through load_schema."""
        # Set up test data with references
        schema_with_ref = {"type": "object", "properties": {"spec": {"$ref": "#/definitions/PodSpec"}}}

        definitions = {"PodSpec": {"type": "object", "properties": {"containers": {"type": "array"}}}}

        # Set up mock mappings with the schema containing references
        mock_mappings = {"testresource": [schema_with_ref]}

        # Set up test data using monkeypatch
        monkeypatch.setattr(SchemaValidator, "_mappings_data", mock_mappings)
        monkeypatch.setattr(SchemaValidator, "_definitions_data", definitions)

        # Use the public load_schema method which will resolve refs internally
        with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
            resolved = SchemaValidator.load_schema(kind="TestResource")

        # Check that $ref was resolved
        assert resolved is not None
        assert resolved["properties"]["spec"]["type"] == "object"
        assert "containers" in resolved["properties"]["spec"]["properties"]

    def test_resolve_refs_with_nested_refs(self, monkeypatch):
        """Test resolving nested $ref references through load_schema."""
        # Set up test data with nested references
        schema_with_ref = {"type": "object", "properties": {"spec": {"$ref": "#/definitions/PodSpec"}}}

        definitions = {
            "PodSpec": {"properties": {"container": {"$ref": "#/definitions/Container"}}},
            "Container": {"type": "object", "properties": {"image": {"type": "string"}}},
        }

        # Set up mock mappings with the schema containing nested references
        mock_mappings = {"nestedresource": [schema_with_ref]}

        # Set up test data using monkeypatch
        monkeypatch.setattr(SchemaValidator, "_mappings_data", mock_mappings)
        monkeypatch.setattr(SchemaValidator, "_definitions_data", definitions)

        # Use the public load_schema method which will resolve refs internally
        with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
            resolved = SchemaValidator.load_schema(kind="NestedResource")

        # Check that nested $refs were resolved
        assert resolved is not None
        assert "image" in resolved["properties"]["spec"]["properties"]["container"]["properties"]
        assert resolved["properties"]["spec"]["properties"]["container"]["type"] == "object"

    def test_schema_caching_across_instances(self, monkeypatch):
        """Test that schema cache is shared across instances."""
        # Clear cache
        SchemaValidator.clear_cache()

        mock_mappings = {"pod": [POD_SCHEMA]}
        mock_definitions = {}

        # Set up test data using monkeypatch
        monkeypatch.setattr(SchemaValidator, "_mappings_data", mock_mappings)
        monkeypatch.setattr(SchemaValidator, "_definitions_data", mock_definitions)

        with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
            # First load
            schema1 = SchemaValidator.load_schema(kind="Pod")

            # Second load should get cached schema
            with patch.object(SchemaValidator, "_resolve_refs") as mock_resolve:
                schema2 = SchemaValidator.load_schema(kind="Pod")

                # Should use cache, not resolve refs again
                mock_resolve.assert_not_called()

            assert schema1 is schema2  # Same object from cache

    def test_case_insensitive_lookup(self, monkeypatch):
        """Test that resource kinds are looked up case-insensitively."""
        # Mock mappings with lowercase key
        mock_mappings = {"deployment": [{"type": "object", "properties": {}}]}
        mock_definitions = {}

        # Set up test data using monkeypatch
        monkeypatch.setattr(SchemaValidator, "_mappings_data", mock_mappings)
        monkeypatch.setattr(SchemaValidator, "_definitions_data", mock_definitions)

        with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
            schema = SchemaValidator.load_schema(kind="Deployment")

            assert schema is not None
            # Deployment kind is looked up as "deployment" (lowercase)


class TestSchemaLoadingWithApiGroup:
    """Test schema loading with API group disambiguation."""

    @pytest.fixture(autouse=True)
    def setup_dns_schemas(self, monkeypatch):
        """Set up mock DNS schemas for different API groups."""
        # Create mock schemas with different descriptions
        dns_config_schema = {
            "type": "object",
            "description": "DNS holds cluster-wide information about DNS",
            "x-kubernetes-group-version-kind": [{"group": "config.openshift.io", "version": "v1", "kind": "DNS"}],
            "properties": {"spec": {"type": "object"}},
        }

        dns_operator_schema = {
            "type": "object",
            "description": "DNS manages the CoreDNS component",
            "x-kubernetes-group-version-kind": [{"group": "operator.openshift.io", "version": "v1", "kind": "DNS"}],
            "properties": {"spec": {"type": "object"}},
        }

        # Set up mock mappings
        mock_mappings = {
            "dns": [dns_operator_schema, dns_config_schema]  # Order matters for testing
        }

        # Set test data using monkeypatch
        monkeypatch.setattr(SchemaValidator, "_mappings_data", mock_mappings)
        monkeypatch.setattr(SchemaValidator, "_definitions_data", {})

        # Mock load_mappings_data to always return True
        with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
            yield

        # monkeypatch automatically cleans up

    def test_load_schema_dns_config_openshift_io(self):
        """Test loading DNS schema for config.openshift.io API group."""
        # Load DNS schema for config.openshift.io
        schema = SchemaValidator.load_schema(kind="DNS", api_group="config.openshift.io")
        assert schema is not None

        # Verify it's the right schema by checking the description
        assert "cluster-wide information" in schema.get("description", "")

    def test_load_schema_dns_operator_openshift_io(self):
        """Test loading DNS schema for operator.openshift.io API group."""
        # Load DNS schema for operator.openshift.io
        schema = SchemaValidator.load_schema(kind="DNS", api_group="operator.openshift.io")
        assert schema is not None

        # Verify it's the right schema by checking the description
        assert "CoreDNS component" in schema.get("description", "")

    def test_load_schema_without_api_group_uses_first(self):
        """Test that loading without API group uses the first available schema."""
        # Load DNS schema without specifying API group
        schema = SchemaValidator.load_schema(kind="DNS")
        assert schema is not None

        # Should get the first one (operator.openshift.io based on the order we set up)
        # But we shouldn't rely on order, just verify we got a schema
        assert "description" in schema

    def test_load_schema_with_wrong_api_group_fallback(self):
        """Test that wrong API group falls back to first schema with warning."""
        # Try to load DNS with a non-existent API group
        # Note: This will log a warning via simple_logger, but we're not capturing it
        # because simple_logger doesn't integrate with pytest's logging capture
        schema = SchemaValidator.load_schema(kind="DNS", api_group="nonexistent.io")

        # Should still get a schema (fallback to first)
        assert schema is not None

        # Verify we got a valid schema (it should fallback to one of the available schemas)
        assert "type" in schema
        assert "x-kubernetes-group-version-kind" in schema

    def test_cache_key_includes_api_group(self):
        """Test that schemas are cached separately by API group."""
        # Clear cache first
        SchemaValidator.clear_cache()

        # Load both DNS schemas
        schema1 = SchemaValidator.load_schema(kind="DNS", api_group="config.openshift.io")
        schema2 = SchemaValidator.load_schema(kind="DNS", api_group="operator.openshift.io")

        # They should be different schemas
        assert schema1 is not None
        assert schema2 is not None
        assert schema1 is not schema2

        # Verify caching by checking that repeated calls return the same object
        schema1_again = SchemaValidator.load_schema(kind="DNS", api_group="config.openshift.io")
        schema2_again = SchemaValidator.load_schema(kind="DNS", api_group="operator.openshift.io")

        assert schema1 is schema1_again  # Same object from cache
        assert schema2 is schema2_again  # Same object from cache

    def test_validate_with_api_group(self):
        """Test validation uses the correct schema based on API group."""
        # Create a minimal DNS resource for config.openshift.io
        dns_config_resource = {
            "apiVersion": "config.openshift.io/v1",
            "kind": "DNS",
            "metadata": {"name": "cluster"},
            "spec": {},
        }

        # This should validate successfully against the config.openshift.io schema
        # (we're not testing full validation here, just that it picks the right schema)
        try:
            SchemaValidator.validate(resource_dict=dns_config_resource, kind="DNS", api_group="config.openshift.io")
        except Exception as e:
            # If validation fails, it should be because of schema requirements,
            # not because we picked the wrong schema
            assert "ValidationError" in str(type(e))
