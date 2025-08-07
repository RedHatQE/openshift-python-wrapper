"""Unit tests for ValidationError exception."""

import pytest

from ocp_resources.exceptions import ValidationError


class TestValidationError:
    """Test cases for ValidationError exception."""

    def test_validation_error_basic(self):
        """Test basic ValidationError creation and string representation."""
        error = ValidationError(message="Field is required")
        assert str(error) == "Validation error: Field is required"
        assert error.message == "Field is required"
        assert error.path == ""
        assert error.schema_error is None

    def test_validation_error_with_path(self):
        """Test ValidationError with path information."""
        error = ValidationError(message="Invalid type", path="spec.containers[0].image")
        assert str(error) == "Validation error at 'spec.containers[0].image': Invalid type"
        assert error.message == "Invalid type"
        assert error.path == "spec.containers[0].image"

    def test_validation_error_with_schema_error(self):
        """Test ValidationError with original schema error attached."""
        original_error = ValueError("Original error")
        error = ValidationError(message="Custom message", schema_error=original_error)
        assert error.message == "Custom message"
        assert error.schema_error == original_error

    def test_validation_error_empty_path(self):
        """Test that empty path doesn't include path in string representation."""
        error = ValidationError(message="Missing required field", path="")
        assert str(error) == "Validation error: Missing required field"

    def test_validation_error_inheritance(self):
        """Test that ValidationError is properly inherited from Exception."""
        error = ValidationError(message="Test error")
        assert isinstance(error, Exception)

        # Test that it can be raised and caught
        with pytest.raises(ValidationError) as exc_info:
            raise error
        assert exc_info.value.message == "Test error"

    def test_validation_error_complex_path(self):
        """Test ValidationError with complex JSONPath."""
        path = "spec.template.spec.containers[0].env[2].valueFrom.secretKeyRef.name"
        error = ValidationError(message="Secret not found", path=path)
        expected = f"Validation error at '{path}': Secret not found"
        assert str(error) == expected
