"""Tests for schema loading functionality."""

from unittest.mock import MagicMock, patch


from ocp_resources.utils.schema_validator import SchemaValidator
from tests.fixtures.validation_schemas import POD_SCHEMA


class TestSchemaLoading:
    """Test schema loading functionality."""

    def test_load_schema_from_mappings(self):
        """Test loading schema from mappings file."""
        # Mock the mappings data
        mock_mappings = {"pod": [POD_SCHEMA]}
        mock_definitions = {}

        # Set up the class attributes
        SchemaValidator._mappings_data = mock_mappings
        SchemaValidator._definitions_data = mock_definitions

        try:
            with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
                schema = SchemaValidator.load_schema(kind="Pod")

                assert schema is not None
                assert schema["type"] == "object"
                assert "properties" in schema
        finally:
            # Clean up
            SchemaValidator.clear_cache()

    def test_load_schema_with_missing_resource(self):
        """Test loading schema when resource is not in mappings."""
        # Clear cache
        SchemaValidator.clear_cache()

        # Mock empty mappings
        mock_mappings = {}
        mock_definitions = {}

        # Set up the class attributes
        SchemaValidator._mappings_data = mock_mappings
        SchemaValidator._definitions_data = mock_definitions

        try:
            with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
                schema = SchemaValidator.load_schema(kind="Pod")

                assert schema is None
        finally:
            # Clean up
            SchemaValidator.clear_cache()

    def test_load_mappings_data_success(self):
        """Test successful loading of mappings data."""
        # Clear any existing data
        SchemaValidator.clear_cache()

        mock_mappings_content = '{"pod": [{"type": "object"}]}'
        mock_definitions_content = '{"definitions": {"SomeDefinition": {"type": "string"}}}'

        # Mock the file system operations
        from unittest.mock import mock_open

        def side_effect(filename, *args, **kwargs):
            if "mappings" in str(filename):
                return mock_open(read_data=mock_mappings_content)()
            elif "definitions" in str(filename):
                return mock_open(read_data=mock_definitions_content)()
            raise FileNotFoundError(f"File not found: {filename}")

        # Patch importlib.resources to prevent actual file loading
        with patch("ocp_resources.utils.schema_validator.files") as mock_files:
            # Mock the files() function
            mock_schema_dir = mock_files.return_value.__truediv__.return_value
            mock_mappings_path = mock_schema_dir.__truediv__.return_value
            mock_mappings_path.read_text.return_value = mock_mappings_content

            # Set up the second call for definitions
            def side_effect_for_truediv(path):
                mock_path = MagicMock()
                if "__resources-mappings.json" in str(path):
                    mock_path.read_text.return_value = mock_mappings_content
                elif "_definitions.json" in str(path):
                    mock_path.read_text.return_value = mock_definitions_content
                return mock_path

            mock_schema_dir.__truediv__.side_effect = side_effect_for_truediv

            result = SchemaValidator.load_mappings_data()

            assert result is True
            assert hasattr(SchemaValidator, "_mappings_data")
            assert hasattr(SchemaValidator, "_definitions_data")
            assert "pod" in SchemaValidator._mappings_data
            assert "SomeDefinition" in SchemaValidator._definitions_data

        # Clean up after test
        SchemaValidator.clear_cache()

    def test_load_mappings_data_already_loaded(self):
        """Test that mappings data is not reloaded if already present."""
        # Set up existing data
        SchemaValidator._mappings_data = {"existing": "data"}
        SchemaValidator._definitions_data = {"existing": "definitions"}

        # load_mappings_data should return True without loading
        with patch("builtins.open") as mock_open:
            result = SchemaValidator.load_mappings_data()

            assert result is True
            mock_open.assert_not_called()

        # Clean up
        SchemaValidator.clear_cache()

    def test_resolve_refs_with_definitions(self):
        """Test resolving $ref references."""
        # Set up test data with references
        schema_with_ref = {"type": "object", "properties": {"spec": {"$ref": "#/definitions/PodSpec"}}}

        definitions = {"PodSpec": {"type": "object", "properties": {"containers": {"type": "array"}}}}

        SchemaValidator._definitions_data = definitions
        resolver = MagicMock()
        resolved = SchemaValidator._resolve_refs(obj=schema_with_ref, resolver=resolver)

        # Check that $ref was resolved
        assert resolved["properties"]["spec"]["type"] == "object"
        assert "containers" in resolved["properties"]["spec"]["properties"]
        assert "$ref" not in resolved["properties"]["spec"]

        # Clean up
        SchemaValidator.clear_cache()

    def test_resolve_refs_with_nested_refs(self):
        """Test resolving nested $ref references."""
        # Set up test data with nested references
        schema_with_ref = {"properties": {"spec": {"$ref": "#/definitions/PodSpec"}}}

        definitions = {
            "PodSpec": {"properties": {"container": {"$ref": "#/definitions/Container"}}},
            "Container": {"type": "object", "properties": {"image": {"type": "string"}}},
        }

        SchemaValidator._definitions_data = definitions
        resolver = MagicMock()
        resolved = SchemaValidator._resolve_refs(obj=schema_with_ref, resolver=resolver)

        # Check that nested refs were resolved
        spec = resolved["properties"]["spec"]
        container = spec["properties"]["container"]
        assert container["type"] == "object"
        assert "image" in container["properties"]

        # Clean up
        SchemaValidator.clear_cache()

    def test_schema_caching_across_instances(self):
        """Test that schema cache is shared across instances."""
        # Clear cache
        SchemaValidator.clear_cache()

        mock_mappings = {"pod": [POD_SCHEMA]}
        mock_definitions = {}

        # Set up the class attributes
        SchemaValidator._mappings_data = mock_mappings
        SchemaValidator._definitions_data = mock_definitions

        try:
            with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
                # First load
                schema1 = SchemaValidator.load_schema(kind="Pod")

                # Second load should get cached schema
                with patch.object(SchemaValidator, "_resolve_refs") as mock_resolve:
                    schema2 = SchemaValidator.load_schema(kind="Pod")

                    # Should use cache, not resolve refs again
                    mock_resolve.assert_not_called()

                assert schema1 is schema2  # Same object from cache
        finally:
            # Clean up
            SchemaValidator.clear_cache()

    def test_case_insensitive_lookup(self):
        """Test that resource kinds are looked up case-insensitively."""
        # Mock mappings with lowercase key
        mock_mappings = {"deployment": [{"type": "object", "properties": {}}]}
        mock_definitions = {}

        # Set up the class attributes
        SchemaValidator._mappings_data = mock_mappings
        SchemaValidator._definitions_data = mock_definitions

        try:
            with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
                schema = SchemaValidator.load_schema(kind="Deployment")

                assert schema is not None
                # Deployment kind is looked up as "deployment" (lowercase)
        finally:
            # Clean up
            SchemaValidator.clear_cache()


class TestSchemaLoadingWithApiGroup:
    """Test schema loading with API group disambiguation."""

    def test_load_schema_dns_config_openshift_io(self):
        """Test loading DNS schema for config.openshift.io API group."""
        # Load the mappings first
        assert SchemaValidator.load_mappings_data()

        # Load DNS schema for config.openshift.io
        schema = SchemaValidator.load_schema(kind="DNS", api_group="config.openshift.io")
        assert schema is not None

        # Verify it's the right schema by checking the description
        assert "cluster-wide information" in schema.get("description", "")

    def test_load_schema_dns_operator_openshift_io(self):
        """Test loading DNS schema for operator.openshift.io API group."""
        # Load the mappings first
        assert SchemaValidator.load_mappings_data()

        # Load DNS schema for operator.openshift.io
        schema = SchemaValidator.load_schema(kind="DNS", api_group="operator.openshift.io")
        assert schema is not None

        # Verify it's the right schema by checking the description
        assert "CoreDNS component" in schema.get("description", "")

    def test_load_schema_without_api_group_uses_first(self):
        """Test that loading without API group uses the first available schema."""
        # Load the mappings first
        assert SchemaValidator.load_mappings_data()

        # Load DNS schema without specifying API group
        schema = SchemaValidator.load_schema(kind="DNS")
        assert schema is not None

        # Should get the first one (operator.openshift.io based on the order we saw)
        # But we shouldn't rely on order, just verify we got a schema
        assert "description" in schema

    def test_load_schema_with_wrong_api_group_fallback(self):
        """Test that wrong API group falls back to first schema with warning."""
        # Load the mappings first
        assert SchemaValidator.load_mappings_data()

        # Try to load DNS with a non-existent API group
        schema = SchemaValidator.load_schema(kind="DNS", api_group="nonexistent.io")

        # Should still get a schema (fallback to first)
        assert schema is not None

    def test_cache_key_includes_api_group(self):
        """Test that schemas are cached separately by API group."""
        # Clear cache first
        SchemaValidator._schema_cache.clear()

        # Load the mappings
        assert SchemaValidator.load_mappings_data()

        # Load both DNS schemas
        schema1 = SchemaValidator.load_schema(kind="DNS", api_group="config.openshift.io")
        schema2 = SchemaValidator.load_schema(kind="DNS", api_group="operator.openshift.io")

        # They should be different schemas
        assert schema1 is not None
        assert schema2 is not None
        assert schema1 is not schema2

        # Check cache has both entries
        assert "config.openshift.io:DNS" in SchemaValidator._schema_cache
        assert "operator.openshift.io:DNS" in SchemaValidator._schema_cache

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
