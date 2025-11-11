"""Tests for resource validation functionality."""

import copy
from unittest.mock import patch

import pytest
from jsonschema import ValidationError as JsonSchemaError

from ocp_resources.exceptions import ValidationError
from ocp_resources.pod import Pod
from ocp_resources.resource import Resource
from ocp_resources.utils.schema_validator import SchemaValidator
from tests.fixtures.validation_schemas import (
    POD_SCHEMA,
    POD_VALID,
)


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


@pytest.fixture
def enable_validation_by_default(monkeypatch):
    """Fixture to enable schema validation by default for all Resource instances during tests."""
    original_init = Resource.__init__

    def patched_init(self, *args, **kwargs):
        # If schema_validation_enabled is not explicitly set, default to True
        if "schema_validation_enabled" not in kwargs:
            kwargs["schema_validation_enabled"] = True
        # Call original_init with self as keyword argument to satisfy FCN001
        return original_init(*args, self=self, **kwargs)

    monkeypatch.setattr(Resource, "__init__", patched_init)
    yield
    # Cleanup happens automatically when fixture goes out of scope


class TestResourceValidation:
    """Test resource validation functionality."""

    def test_validate_with_valid_resource(self, fake_client, enable_validation_by_default):
        """Test validation passes with valid resource."""
        pod = Pod(
            name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}], client=fake_client
        )
        pod.res = POD_VALID  # Set valid resource dict

        # Mock the schema loading
        with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
            # Should not raise any exception
            pod.validate()

            # Also test validate_dict class method
            with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
                Pod.validate_dict(resource_dict=POD_VALID)

    def test_validate_with_invalid_resource_missing_required(self, fake_client, enable_validation_by_default):
        """Test validation fails when required fields are missing."""
        pod = Pod(
            name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}], client=fake_client
        )

        # Create invalid resource missing required metadata
        invalid_resource = copy.deepcopy(POD_VALID)
        del invalid_resource["metadata"]
        pod.res = invalid_resource

        # Mock the schema loading
        with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
            with pytest.raises(ValidationError) as exc_info:
                pod.validate()

            assert "'metadata' is a required property" in str(exc_info.value)

    def test_validate_with_invalid_resource_wrong_type(self, fake_client, enable_validation_by_default):
        """Test validation fails when field has wrong type."""
        pod = Pod(name="test-pod", namespace="default", client=fake_client)

        # Create invalid resource with wrong type for spec
        invalid_resource = copy.deepcopy(POD_VALID)
        invalid_resource["spec"] = "this should be an object not a string"
        pod.res = invalid_resource

        # Mock the schema loading
        with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
            with pytest.raises(ValidationError) as exc_info:
                pod.validate()

            # Should indicate that spec should be object, not string
            assert "spec" in str(exc_info.value)
            assert "must be of type" in str(exc_info.value) or "is not of type" in str(exc_info.value)

    def test_validate_with_no_schema_available(self, fake_client, enable_validation_by_default):
        """Test validation is skipped when no schema is available."""
        pod = Pod(name="test-pod", namespace="default", client=fake_client)
        pod.res = POD_VALID

        # Mock schema loading to return None (no schema found)
        with patch.object(SchemaValidator, "load_schema", return_value=None):
            # Should not raise any exception, just skip validation
            pod.validate()

    def test_validate_dict_class_method(self, fake_client):
        """Test the validate_dict class method."""
        # Test with valid resource
        with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
            Pod.validate_dict(resource_dict=POD_VALID)

        # Test with invalid resource
        invalid_resource = copy.deepcopy(POD_VALID)
        del invalid_resource["metadata"]

        with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
            with pytest.raises(ValidationError):
                Pod.validate_dict(resource_dict=invalid_resource)

    def test_format_validation_error(self, fake_client):
        """Test validation error formatting."""
        # Create a mock validation error
        mock_error = JsonSchemaError(
            message="'name' is a required property",
            path=["metadata"],
            schema_path=["properties", "metadata", "required"],
        )

        formatted = SchemaValidator.format_validation_error(error=mock_error, kind="Pod", name="test-pod")
        assert "Resource validation failed for Pod/test-pod" in formatted
        assert "Field: metadata" in formatted
        assert "'name' is a required property" in formatted

    def test_validate_with_nested_error(self, fake_client, enable_validation_by_default):
        """Test validation with deeply nested error."""
        pod = Pod(
            name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}], client=fake_client
        )

        # Create invalid resource with wrong type in nested field
        invalid_resource = copy.deepcopy(POD_VALID)
        invalid_resource["spec"]["containers"][0]["image"] = 123  # Should be string
        pod.res = invalid_resource

        # Mock the schema loading
        with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
            with pytest.raises(ValidationError) as exc_info:
                pod.validate()

            # Error should mention the path to the invalid field
            error_str = str(exc_info.value)
            assert "spec.containers[0].image" in error_str or "spec.containers.0.image" in error_str

    def test_validate_with_multiple_errors(self, fake_client, enable_validation_by_default):
        """Test validation reports multiple errors."""
        pod = Pod(
            name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}], client=fake_client
        )

        # Create resource with multiple errors
        invalid_resource = {
            "apiVersion": "v1",
            "kind": 123,  # Should be string
            # Missing metadata and spec
        }
        pod.res = invalid_resource

        # Mock the schema loading
        with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
            with pytest.raises(ValidationError) as exc_info:
                pod.validate()

            error_str = str(exc_info.value)
            # Should mention at least one of the issues
            assert any(term in error_str for term in ["kind", "metadata", "spec", "required", "type"])

    def test_validate_performance_with_cache(self, fake_client, enable_validation_by_default, monkeypatch):
        """Test that schema caching improves performance."""
        pod = Pod(
            name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}], client=fake_client
        )
        pod.res = POD_VALID  # Set valid resource dict

        # Clear cache
        SchemaValidator.clear_cache()

        # Mock the mappings data to return our test schema
        mock_mappings = {"pod": [POD_SCHEMA]}
        mock_definitions = {}  # Empty definitions for this test

        # Set up the class attributes using monkeypatch
        monkeypatch.setattr(SchemaValidator, "_mappings_data", mock_mappings)
        monkeypatch.setattr(SchemaValidator, "_definitions_data", mock_definitions)

        try:
            # Mock load_mappings_data to return True (already loaded)
            with patch.object(SchemaValidator, "load_mappings_data", return_value=True):
                # First call should process and cache the schema
                pod.validate()

                # Check that schema was cached
                assert "Pod" in SchemaValidator._schema_cache

                # Clear the mock to ensure second call uses cache
                with patch.object(SchemaValidator, "_resolve_refs") as mock_resolve:
                    # Second call should use cache (no ref resolution needed)
                    pod.validate()
                    mock_resolve.assert_not_called()
        finally:
            # Clean up
            SchemaValidator.clear_cache()

    def test_validate_with_additional_properties(self, fake_client, enable_validation_by_default):
        """Test validation passes even with additional properties not in schema."""
        pod = Pod(
            name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}], client=fake_client
        )

        # Add extra properties to the resource
        resource_with_extras = copy.deepcopy(POD_VALID)
        resource_with_extras["extraField"] = "extra value"
        resource_with_extras["metadata"]["customAnnotation"] = "custom"
        pod.res = resource_with_extras

        # Mock the schema loading
        with patch.object(SchemaValidator, "load_schema", return_value=POD_SCHEMA):
            # Should not raise any exception - additional properties are allowed
            pod.validate()

    def test_validate_with_api_group_disambiguation(self, fake_client, enable_validation_by_default):
        """Test that resources with same kind but different API groups use correct schema."""

        # Mock DNS classes to avoid initialization issues
        class MockDNSConfig:
            kind = "DNS"
            api_group = "config.openshift.io"
            name = "cluster"
            res = {"apiVersion": "config.openshift.io/v1", "kind": "DNS", "metadata": {"name": "cluster"}, "spec": {}}
            schema_validation_enabled = True

            def validate(self):
                Resource.validate(self)

        class MockDNSOperator:
            kind = "DNS"
            api_group = "operator.openshift.io"
            name = "default"
            res = {"apiVersion": "operator.openshift.io/v1", "kind": "DNS", "metadata": {"name": "default"}, "spec": {}}
            schema_validation_enabled = True

            def validate(self):
                Resource.validate(self)

        # Create mock instances
        dns_config = MockDNSConfig()
        dns_operator = MockDNSOperator()

        # Verify they have different API groups
        assert dns_config.api_group == "config.openshift.io"
        assert dns_operator.api_group == "operator.openshift.io"

        # Mock the schema loading to return different schemas
        config_schema = {"type": "object", "description": "DNS config schema"}
        operator_schema = {"type": "object", "description": "DNS operator schema"}

        def mock_load_schema(kind, api_group=None):
            if kind == "DNS" and api_group == "config.openshift.io":
                return config_schema
            elif kind == "DNS" and api_group == "operator.openshift.io":
                return operator_schema
            return None

        with patch.object(SchemaValidator, "load_schema", side_effect=mock_load_schema) as mock:
            # Validate both - they should use different schemas
            dns_config.validate()
            dns_operator.validate()

            # Verify the correct schemas were requested
            calls = mock.call_args_list
            assert len(calls) == 2

            # Check that each was called with the correct API group
            assert any(call[1].get("api_group") == "config.openshift.io" for call in calls)
            assert any(call[1].get("api_group") == "operator.openshift.io" for call in calls)


class TestAutoValidation:
    """Test auto-validation functionality for resources."""

    def test_auto_validation_disabled_by_default(self, fake_client):
        """Test that auto-validation is disabled by default."""
        pod = Pod(name="test-pod", namespace="default", client=fake_client)

        # Should be disabled by default
        assert pod.schema_validation_enabled is False

    def test_enable_schema_validation_instance(self, fake_client):
        """Test enabling schema validation at instance level."""
        # Create pod with validation disabled (default)
        pod1 = Pod(name="test-pod1", namespace="default", client=fake_client)
        assert pod1.schema_validation_enabled is False

        # Create pod with validation enabled
        pod2 = Pod(name="test-pod2", namespace="default", client=fake_client, schema_validation_enabled=True)
        assert pod2.schema_validation_enabled is True

    def test_auto_validation_on_create(self, monkeypatch, fake_client, enable_validation_by_default):
        """Test that validation runs automatically on create when enabled."""
        # Track if validate was called
        validate_calls = []

        def mock_validate():
            validate_calls.append(1)

        # Create pod with auto-validation disabled (default)
        pod = Pod(
            name="test-pod", namespace="default", client=fake_client, containers=[{"name": "test", "image": "nginx"}]
        )
        pod.schema_validation_enabled = False

        # Mock validate method
        monkeypatch.setattr(pod, "validate", mock_validate)

        # Deploy should not trigger validation
        validate_calls.clear()
        deployed = pod.deploy()
        assert deployed
        assert len(validate_calls) == 0

        # Clean up for next test
        pod.clean_up(wait=False)

        # Create new pod with validation enabled
        pod2 = Pod(
            name="test-pod2",
            namespace="default",
            client=fake_client,
            containers=[{"name": "test", "image": "nginx"}],
            schema_validation_enabled=True,
        )
        monkeypatch.setattr(pod2, "validate", mock_validate)

        # Deploy should trigger validation
        validate_calls.clear()
        deployed2 = pod2.deploy()
        assert deployed2
        assert len(validate_calls) == 1

    def test_auto_validation_on_update_replace(self, monkeypatch, fake_client, enable_validation_by_default):
        """Test that validation runs automatically on update_replace when enabled."""
        # Track if validate_dict was called
        validate_calls = []

        def mock_validate_dict(resource_dict):
            validate_calls.append(resource_dict)

        # Create and deploy pod first
        pod = Pod(
            name="test-pod", namespace="default", client=fake_client, containers=[{"name": "test", "image": "nginx"}]
        )
        pod.deploy()

        # Mock validate_dict
        monkeypatch.setattr(Pod, "validate_dict", mock_validate_dict)

        # Replace should not trigger validation when disabled
        pod.schema_validation_enabled = False
        validate_calls.clear()
        replacement_dict = pod.instance.to_dict()
        replacement_dict["metadata"]["labels"] = {"test": "label"}
        pod.update_replace(resource_dict=replacement_dict)
        assert len(validate_calls) == 0

        # Enable validation and try again
        pod.schema_validation_enabled = True
        validate_calls.clear()
        replacement_dict["metadata"]["labels"]["test2"] = "label2"
        pod.update_replace(resource_dict=replacement_dict)
        assert len(validate_calls) == 1
        assert validate_calls[0] == replacement_dict

    def test_auto_validation_with_validation_error(self, monkeypatch, fake_client, enable_validation_by_default):
        """Test that validation errors prevent create/update when auto-validation is enabled."""
        # Create pod with validation enabled
        pod = Pod(
            name="test-pod",
            namespace="default",
            client=fake_client,
            containers=[{"name": "test", "image": "nginx"}],
            schema_validation_enabled=True,
        )

        # Mock validate to raise ValidationError
        def mock_validate_error():
            raise ValidationError("Invalid resource")

        monkeypatch.setattr(pod, "validate", mock_validate_error)

        # Deploy should raise ValidationError
        with pytest.raises(ValidationError, match="Invalid resource"):
            pod.deploy()

    def test_auto_validation_instance_explicit(self, fake_client):
        """Test that instance-level validation setting works correctly."""
        # Create instance with validation explicitly disabled (default)
        pod1 = Pod(name="test-pod1", namespace="default", client=fake_client, schema_validation_enabled=False)
        assert pod1.schema_validation_enabled is False

        # Create instance with validation explicitly enabled
        pod2 = Pod(name="test-pod2", namespace="default", client=fake_client, schema_validation_enabled=True)
        assert pod2.schema_validation_enabled is True
