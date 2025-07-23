"""Tests for schema loading functionality."""

import json
from unittest.mock import MagicMock, Mock, mock_open, patch


from ocp_resources.resource import Resource


class TestSchemaLoading:
    """Test cases for schema loading functionality."""

    def test_find_schema_file_simple_case(self):
        """Test finding schema file for simple resource kind."""

        # Create a mock resource class
        class MockPod(Resource):
            kind = "Pod"
            api_version = "v1"

        # Mock the client
        mock_client = MagicMock()
        resource = MockPod(name="test-pod", client=mock_client)

        # Test _find_schema_file method
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            schema_file = resource._find_schema_file()

            assert schema_file is not None
            assert str(schema_file).endswith("pod.json")

    def test_find_schema_file_camelcase_conversion(self):
        """Test schema file finding with CamelCase to snake_case conversion."""

        class MockDeployment(Resource):
            kind = "Deployment"
            api_version = "apps/v1"

        mock_client = MagicMock()
        resource = MockDeployment(name="test-deployment", client=mock_client)

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            schema_file = resource._find_schema_file()

            assert schema_file is not None
            assert str(schema_file).endswith("deployment.json")

    def test_find_schema_file_complex_name(self):
        """Test schema file finding for complex resource names."""

        class MockVirtualMachineInstance(Resource):
            kind = "VirtualMachineInstance"
            api_version = "kubevirt.io/v1"

        mock_client = MagicMock()
        resource = MockVirtualMachineInstance(name="test-vmi", client=mock_client)

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            schema_file = resource._find_schema_file()

            assert schema_file is not None
            assert str(schema_file).endswith("virtual_machine_instance.json")

    def test_find_schema_file_not_found(self):
        """Test behavior when schema file doesn't exist."""

        class MockCustomResource(Resource):
            kind = "CustomResource"
            api_version = "custom.io/v1"

        mock_client = MagicMock()
        resource = MockCustomResource(name="test-custom", client=mock_client)

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = False
            schema_file = resource._find_schema_file()

            assert schema_file is None

    def test_load_schema_success(self):
        """Test successful schema loading from file."""

        class MockPod(Resource):
            kind = "Pod"
            api_version = "v1"

        mock_client = MagicMock()
        resource = MockPod(name="test-pod", client=mock_client)
        test_schema = {"type": "object", "properties": {"test": {"type": "string"}}}

        with patch.object(resource, "_find_schema_file") as mock_find:
            mock_path = Mock()
            mock_path.exists.return_value = True
            mock_find.return_value = mock_path

            with patch("builtins.open", mock_open(read_data=json.dumps(test_schema))):
                schema = resource._load_schema()

                assert schema == test_schema
                # Verify it was cached
                assert resource._schema_cache["Pod"] == test_schema

    def test_load_schema_from_cache(self):
        """Test that schema is loaded from cache on second call."""

        class MockPod(Resource):
            kind = "Pod"
            api_version = "v1"
            _schema_cache = {}

        mock_client = MagicMock()
        resource = MockPod(name="test-pod", client=mock_client)
        test_schema = {"type": "object", "properties": {"test": {"type": "string"}}}

        # Pre-populate cache
        resource._schema_cache["Pod"] = test_schema

        with patch.object(resource, "_find_schema_file") as mock_find:
            schema = resource._load_schema()

            # Should not call _find_schema_file if in cache
            mock_find.assert_not_called()
            assert schema == test_schema

    def test_load_schema_file_not_found(self):
        """Test behavior when schema file is not found."""

        class MockCustomResource(Resource):
            kind = "CustomResource"
            api_version = "custom.io/v1"

        mock_client = MagicMock()
        resource = MockCustomResource(name="test-custom", client=mock_client)

        with patch.object(resource, "_find_schema_file") as mock_find:
            mock_find.return_value = None

            schema = resource._load_schema()

            assert schema is None

    def test_load_schema_invalid_json(self):
        """Test behavior when schema file contains invalid JSON."""

        class MockPod(Resource):
            kind = "Pod"
            api_version = "v1"

        mock_client = MagicMock()
        resource = MockPod(name="test-pod", client=mock_client)

        # Clear cache to ensure clean test
        resource._schema_cache.clear()

        with patch.object(resource, "_find_schema_file") as mock_find:
            mock_path = Mock()
            mock_path.exists.return_value = True
            mock_find.return_value = mock_path

            with patch("builtins.open", mock_open(read_data="invalid json")):
                schema = resource._load_schema()

                assert schema is None

    def test_load_schema_io_error(self):
        """Test behavior when IO error occurs during schema loading."""

        class MockPod(Resource):
            kind = "Pod"
            api_version = "v1"

        mock_client = MagicMock()
        resource = MockPod(name="test-pod", client=mock_client)

        # Clear cache to ensure clean test
        resource._schema_cache.clear()

        with patch.object(resource, "_find_schema_file") as mock_find:
            mock_path = Mock()
            mock_path.exists.return_value = True
            mock_find.return_value = mock_path

            with patch("builtins.open", side_effect=IOError("File read error")):
                schema = resource._load_schema()

                assert schema is None

    def test_camelcase_to_snake_case(self):
        """Test CamelCase to snake_case conversion."""
        # Use the function from utils
        from ocp_resources.utils.utils import convert_camel_case_to_snake_case

        test_cases = [
            ("Pod", "pod"),
            ("ConfigMap", "config_map"),
            ("VirtualMachineInstance", "virtual_machine_instance"),
            ("APIService", "api_service"),
            ("CSIDriver", "csi_driver"),
            ("DNS", "dns"),
            ("OAuth", "oauth"),
        ]

        for camel, expected_snake in test_cases:
            assert convert_camel_case_to_snake_case(name=camel) == expected_snake

    def test_schema_cache_isolation(self):
        """Test that schema cache is properly isolated between resource types."""

        class MockPod(Resource):
            kind = "Pod"
            api_version = "v1"
            _schema_cache = {}

        class MockService(Resource):
            kind = "Service"
            api_version = "v1"
            _schema_cache = {}

        mock_client = MagicMock()
        pod_resource = MockPod(name="test-pod", client=mock_client)
        service_resource = MockService(name="test-service", client=mock_client)

        pod_schema = {"type": "object", "kind": "Pod"}
        service_schema = {"type": "object", "kind": "Service"}

        # Load schemas into cache
        pod_resource._schema_cache["Pod"] = pod_schema
        service_resource._schema_cache["Service"] = service_schema

        # Verify isolation
        assert pod_resource._load_schema() == pod_schema
        assert service_resource._load_schema() == service_schema
        assert "Service" not in pod_resource._schema_cache
        assert "Pod" not in service_resource._schema_cache
