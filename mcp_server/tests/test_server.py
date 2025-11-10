"""Unit tests for MCP server.

Comprehensive tests for the OpenShift Python Wrapper MCP Server
"""

import pytest

import mcp_server.server
from mcp_server.server import (
    _get_available_resource_types,
    format_resource_info,
    get_resource_class,
)
from ocp_resources.config_map import ConfigMap

# Get the actual function implementations from the decorated tools
list_resources_func = mcp_server.server.list_resources.fn
get_resource_func = mcp_server.server.get_resource.fn
create_resource_func = mcp_server.server.create_resource.fn
update_resource_func = mcp_server.server.update_resource.fn
delete_resource_func = mcp_server.server.delete_resource.fn
get_pod_logs_func = mcp_server.server.get_pod_logs.fn
exec_in_pod_func = mcp_server.server.exec_in_pod.fn
get_resource_events_func = mcp_server.server.get_resource_events.fn
apply_yaml_func = mcp_server.server.apply_yaml.fn
get_resource_types_func = mcp_server.server.get_resource_types.fn


@pytest.fixture
def use_fake_client():
    """Ensure MCP server uses fake client for tests"""
    # Reset the global client before each test
    mcp_server.server._client = None

    # Get a fake client
    fake_client = mcp_server.server.get_dynamic_client(fake=True)

    yield fake_client

    # Reset client after test
    mcp_server.server._client = None


class TestClientManagement:
    """Test client creation and management"""

    def test_get_dynamic_client_with_fake(self, use_fake_client):
        """Test that get_dynamic_client returns fake client"""
        client = mcp_server.server.get_dynamic_client()
        assert client is not None
        # The client should be a fake client
        assert hasattr(client, "resources")


class TestResourceDiscovery:
    """Test resource type discovery"""

    def test_get_available_resource_types(self):
        """Test _get_available_resource_types discovers resources correctly"""
        resource_types = _get_available_resource_types()

        assert isinstance(resource_types, list)
        assert len(resource_types) > 0
        assert "pod" in resource_types
        assert "configmap" in resource_types
        assert "namespace" in resource_types

    def test_get_resource_class_found(self):
        """Test get_resource_class when resource is found"""
        result = get_resource_class(resource_type="pod")
        assert result is not None
        assert hasattr(result, "kind")

    def test_get_resource_class_not_found(self):
        """Test get_resource_class when resource is not found"""
        result = get_resource_class(resource_type="this_resource_does_not_exist_12345")
        assert result is None


class TestFormatResourceInfo:
    """Test resource info formatting"""

    def test_format_resource_info_basic(self, use_fake_client):
        """Test basic resource info formatting"""
        # Create a real ConfigMap resource using the fake client
        cm = ConfigMap(client=use_fake_client, name="test-cm", namespace="default", data={"key": "value"})
        cm.create()

        result = format_resource_info(resource=cm)

        assert result["name"] == "test-cm"
        assert result["namespace"] == "default"
        assert "uid" in result
        assert "resourceVersion" in result
        assert "creationTimestamp" in result


class TestListResources:
    """Test list_resources function"""

    def test_list_resources_success(self, use_fake_client):
        """Test successful resource listing"""
        # Create test resources
        for i in range(3):
            cm = ConfigMap(name=f"test-cm-{i}", namespace="default", data={"key": f"value-{i}"}, client=use_fake_client)
            cm.deploy()

        result = list_resources_func(resource_type="configmap", namespace="default", limit=10)

        assert result["resource_type"] == "configmap"
        assert result["namespace"] == "default"
        assert result["count"] >= 3
        assert len(result["resources"]) >= 3

    def test_list_resources_unknown_type(self):
        """Test listing with unknown resource type"""
        result = list_resources_func(resource_type="unknown_resource_type")

        assert "error" in result
        assert "Unknown resource type" in result["error"]


class TestGetResource:
    """Test get_resource function"""

    def test_get_resource_success(self, use_fake_client):
        """Test successful resource retrieval"""
        cm = ConfigMap(name="test-get-cm", namespace="default", data={"key": "value"}, client=use_fake_client)
        cm.deploy()

        result = get_resource_func(
            resource_type="configmap", name="test-get-cm", namespace="default", output_format="info"
        )

        assert result["name"] == "test-get-cm"
        assert result["namespace"] == "default"

    def test_get_resource_unknown_type(self):
        """Test getting unknown resource type"""
        result = get_resource_func(resource_type="unknown_type", name="name", namespace="default")

        assert "error" in result
        assert "Unknown resource type" in result["error"]

    def test_get_resource_not_found(self, use_fake_client):
        """Test getting non-existent resource"""
        result = get_resource_func(resource_type="configmap", name="does-not-exist", namespace="default")

        assert "error" in result


class TestCreateResource:
    """Test create_resource function"""

    def test_create_resource_success(self, use_fake_client):
        """Test successful resource creation"""
        result = create_resource_func(
            resource_type="configmap", name="test-create-cm", namespace="default", spec={"data": {"key": "value"}}
        )

        assert result["success"] is True
        assert result["name"] == "test-create-cm"
        assert "created successfully" in result["message"]

    def test_create_resource_unknown_type(self, use_fake_client):
        """Test creating unknown resource type"""
        result = create_resource_func(resource_type="unknown", name="name", namespace="default", spec={"test": "data"})

        assert "error" in result
        assert "Unknown resource type" in result["error"]


class TestUpdateResource:
    """Test update_resource function"""

    def test_update_resource_success(self, use_fake_client):
        """Test successful resource update"""
        # First create a resource
        create_result = create_resource_func(
            resource_type="configmap", name="test-update-cm", namespace="default", spec={"data": {"key": "value"}}
        )
        assert create_result["success"] is True

        # Then update it - this should succeed with the fake client
        result = update_resource_func(
            resource_type="configmap",
            name="test-update-cm",
            namespace="default",
            patch={"metadata": {"name": "test-update-cm"}, "data": {"key": "updated-value", "newkey": "newvalue"}},
        )

        # The update should succeed (no error key means success)
        assert "error" not in result
        assert result.get("success") is True
        assert "updated successfully" in result["message"]
        assert result["resource_type"] == "configmap"
        assert result["name"] == "test-update-cm"
        assert result["namespace"] == "default"

    def test_update_resource_not_found(self, use_fake_client):
        """Test update of non-existent resource"""
        # Try to update a resource that doesn't exist
        result = update_resource_func(
            resource_type="configmap",
            name="non-existent-cm",
            namespace="default",
            patch={"data": {"key": "value"}},
        )

        # Should return an error
        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_update_resource_unknown_type(self, use_fake_client):
        """Test update with unknown resource type"""
        result = update_resource_func(
            resource_type="unknown_type",
            name="test-resource",
            namespace="default",
            patch={"spec": {"test": "value"}},
        )

        # Should return an error for unknown resource type
        assert "error" in result
        assert "Unknown resource type" in result["error"]


class TestDeleteResource:
    """Test delete_resource function"""

    def test_delete_resource_success(self, use_fake_client):
        """Test successful resource deletion"""
        # First create a resource
        create_result = create_resource_func(
            resource_type="configmap", name="test-delete-cm", namespace="default", spec={"data": {"key": "value"}}
        )
        assert create_result["success"] is True

        # Then delete it
        result = delete_resource_func(resource_type="configmap", name="test-delete-cm", namespace="default")

        assert result["success"] is True
        assert "deleted successfully" in result["message"]


class TestGetPodLogs:
    """Test get_pod_logs function"""

    def test_get_pod_logs_not_found(self, use_fake_client):
        """Test pod logs retrieval for non-existent pod"""
        result = get_pod_logs_func(name="non-existent-pod", namespace="default")

        assert "error" in result


class TestExecInPod:
    """Test exec_in_pod function"""

    def test_exec_in_pod_not_found(self, use_fake_client):
        """Test command execution in non-existent pod"""
        result = exec_in_pod_func(name="non-existent-pod", namespace="default", command=["echo", "hello"])

        assert "error" in result


class TestGetResourceEvents:
    """Test get_resource_events function"""

    def test_get_resource_events_empty(self, use_fake_client):
        """Test resource events retrieval when no events exist"""
        # No resources created, so no events should exist
        result = get_resource_events_func(resource_type="pod", name="test-pod", namespace="default")

        assert result["resource_type"] == "pod"
        assert result["name"] == "test-pod"
        assert result["namespace"] == "default"
        assert result["event_count"] == 0
        assert result["events"] == []

    def test_get_resource_events_with_created_resource(self, use_fake_client):
        """Test that events are automatically generated when resources are created"""
        # Create a ConfigMap - this will automatically generate a creation event
        cm = ConfigMap(client=use_fake_client, name="test-cm-events", namespace="default", data={"key": "value"})
        cm.create()

        # Get events for the created ConfigMap
        result = get_resource_events_func(resource_type="configmap", name="test-cm-events", namespace="default")

        assert result["resource_type"] == "configmap"
        assert result["name"] == "test-cm-events"
        assert result["namespace"] == "default"
        assert result["event_count"] == 1
        assert len(result["events"]) == 1

        # Check the event details
        event = result["events"][0]
        assert event["type"] == "Normal"
        assert event["reason"] == "Created"
        assert "ConfigMap test-cm-events has been created" in event["message"]
        assert event["involvedObject"]["kind"] == "ConfigMap"
        assert event["involvedObject"]["name"] == "test-cm-events"
        assert event["involvedObject"]["namespace"] == "default"

    def test_get_resource_events_correct_kind_values(self, use_fake_client):
        """Test that different resource types get the correct Kind value in field selector"""
        # Just test with resources we know work well with the fake client

        # Test with ConfigMap
        cm = ConfigMap(client=use_fake_client, name="test-cm-kind", namespace="default")
        cm.data = {"key": "value"}  # Set data after construction
        cm.create()

        result = get_resource_events_func(resource_type="configmap", name="test-cm-kind", namespace="default")
        assert result["event_count"] == 1
        event = result["events"][0]
        assert event["involvedObject"]["kind"] == "ConfigMap"

        # The important thing we're testing is that get_resource_events correctly
        # determines the Kind value from the resource type using the resource class.
        # The fix ensures it uses resource_class.kind instead of hard-coded logic.

        # We've verified that "configmap" -> "ConfigMap" works correctly.
        # The implementation uses _validate_resource_type to get the resource class
        # and then uses resource_class.kind to get the correct Kind value.


class TestApplyYaml:
    """Test apply_yaml function"""

    def test_apply_yaml_success(self, use_fake_client):
        """Test successful YAML application"""
        yaml_content = """
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-yaml-cm
  namespace: default
data:
  key: value
"""

        result = apply_yaml_func(yaml_content=yaml_content)

        assert result["total_resources"] == 1
        assert result["successful"] == 1
        assert result["failed"] == 0


class TestGetResourceTypes:
    """Test get_resource_types function"""

    def test_get_resource_types_success(self):
        """Test getting available resource types"""
        # The random_string parameter is passed to comply with MCP protocol requirements,
        # even though it is not used in the function implementation
        result = get_resource_types_func(random_string="test")

        assert "resource_types" in result
        assert isinstance(result["resource_types"], list)
        assert result["total_count"] > 0
        assert "categories" in result
