"""Tests for resource validation functionality."""

import copy
import json
from unittest.mock import MagicMock, patch

import pytest

from ocp_resources.exceptions import ValidationError
from ocp_resources.pod import Pod
from ocp_resources.resource import Resource
from tests.fixtures.validation_schemas import (
    POD_INVALID_CONTAINER_NAME,
    POD_MISSING_REQUIRED,
    POD_SCHEMA,
    POD_VALID,
)


class TestResourceValidation:
    """Test resource validation functionality."""

    def test_validate_with_valid_resource(self):
        """Test validate() with a valid resource dict."""
        # Create a Pod instance with valid data
        pod = Pod(
            name="test-pod",
            namespace="default",
            containers=[{"name": "nginx", "image": "nginx:latest"}],
        )

        # Mock the schema loading
        with patch.object(pod, "_load_schema", return_value=POD_SCHEMA):
            # Should not raise any exception
            pod.validate()

    def test_validate_with_invalid_resource_missing_required(self):
        """Test validate() with missing required fields."""
        # Create a Pod instance
        pod = Pod(name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}])

        # Initialize the resource dict
        pod.res = {}

        # Mock the resource dict and skip to_dict
        with patch.object(pod, "res", POD_MISSING_REQUIRED):
            with patch.object(pod, "_load_schema", return_value=POD_SCHEMA):
                with pytest.raises(ValidationError) as exc_info:
                    pod.validate()

                assert "containers" in str(exc_info.value)
                assert "required property" in str(exc_info.value)

    def test_validate_with_invalid_resource_wrong_type(self):
        """Test validate() with wrong field types."""
        # Create a Pod instance
        pod = Pod(name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}])

        # Initialize the resource dict
        pod.res = {}

        # Mock the resource dict with invalid data
        invalid_data = copy.deepcopy(POD_VALID)
        invalid_data["spec"]["containers"] = "not-a-list"  # Should be a list

        with patch.object(pod, "res", invalid_data):
            with patch.object(pod, "_load_schema", return_value=POD_SCHEMA):
                with pytest.raises(ValidationError) as exc_info:
                    pod.validate()

                assert "containers" in str(exc_info.value)
                assert "type" in str(exc_info.value)

    def test_validate_with_no_schema_available(self):
        """Test validate() when no schema is available."""
        pod = Pod(name="test-pod", namespace="default")

        # Mock _load_schema to return None
        with patch.object(pod, "_load_schema", return_value=None):
            # Should not raise exception, just log warning
            pod.validate()

    def test_validate_dict_class_method(self):
        """Test validate_dict() class method."""
        # Test with valid dict
        with patch("ocp_resources.resource.Resource._load_schema", return_value=POD_SCHEMA):
            # Should not raise any exception
            Pod.validate_dict(resource_dict=POD_VALID)

        # Test with invalid dict
        with patch("ocp_resources.resource.Resource._load_schema", return_value=POD_SCHEMA):
            with pytest.raises(ValidationError):
                Pod.validate_dict(resource_dict=POD_MISSING_REQUIRED)

    def test_format_validation_error(self):
        """Test _format_validation_error() method."""
        pod = Pod(name="test-pod", namespace="default")

        # Create a mock validation error
        from jsonschema import ValidationError as JsonSchemaError

        error = JsonSchemaError(
            message="'containers' is a required property",
            path=["spec"],
            schema_path=["properties", "spec", "required"],
            instance={"metadata": {"name": "test-pod"}},
        )

        formatted = pod._format_validation_error(error=error)

        assert "Validation error at 'spec'" in formatted
        assert "'containers' is a required property" in formatted
        assert "Schema path:" in formatted

    def test_validate_with_nested_error(self):
        """Test validate() with nested validation errors."""
        pod = Pod(name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}])
        pod.res = {}

        # Mock the resource dict with nested error
        with patch.object(pod, "res", POD_INVALID_CONTAINER_NAME):
            with patch.object(pod, "_load_schema", return_value=POD_SCHEMA):
                with pytest.raises(ValidationError) as exc_info:
                    pod.validate()

                # Should show the nested path
                assert "spec.containers[0].name" in str(exc_info.value)

    def test_validate_with_multiple_errors(self):
        """Test validate() with multiple validation errors."""
        pod = Pod(name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}])
        pod.res = {}

        # Create data with multiple errors
        invalid_data = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": 123},  # Should be string
            "spec": {
                "containers": "not-a-list",  # Should be list
            },
        }

        with patch.object(pod, "res", invalid_data):
            with patch.object(pod, "_load_schema", return_value=POD_SCHEMA):
                with pytest.raises(ValidationError) as exc_info:
                    pod.validate()

                error_str = str(exc_info.value)
                # Should mention first error (implementation dependent)
                assert "metadata.name" in error_str or "containers" in error_str

    def test_validate_performance_with_cache(self):
        """Test that schema caching improves performance."""
        pod = Pod(name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}])
        pod.res = POD_VALID  # Set valid resource dict

        # Clear cache
        if hasattr(Resource, "_schema_cache"):
            Resource._schema_cache.clear()

        # Create a mock Path object that has read_text method
        mock_path = MagicMock()
        mock_path.read_text.return_value = json.dumps(POD_SCHEMA)

        with patch.object(pod, "_find_schema_file", return_value=mock_path) as mock_find:
            # First call should find and load schema
            pod.validate()
            assert mock_find.call_count == 1
            assert mock_path.read_text.call_count == 1

            # Second call should use cache (no file operations)
            pod.validate()
            assert mock_find.call_count == 1  # Should not increase
            assert mock_path.read_text.call_count == 1  # Should not increase

    def test_validate_with_additional_properties(self):
        """Test validate() with additional properties not in schema."""
        pod = Pod(name="test-pod", namespace="default", containers=[{"name": "test", "image": "test"}])
        pod.res = {}

        # Add extra field not in schema
        data_with_extra = copy.deepcopy(POD_VALID)
        data_with_extra["spec"]["extraField"] = "should-be-ignored"

        with patch.object(pod, "res", data_with_extra):
            with patch.object(pod, "_load_schema", return_value=POD_SCHEMA):
                # Should not raise exception for additional properties
                # (OpenAPI schemas typically allow them)
                pod.validate()
