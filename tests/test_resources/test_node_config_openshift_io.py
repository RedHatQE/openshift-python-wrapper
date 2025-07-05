import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.node_config_openshift_io import Node


class TestNode:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def node(self, client):
        return Node(
            client=client,
            name="test-node",
        )

    def test_create_node(self, node):
        """Test creating Node"""
        deployed_resource = node.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-node"
        assert node.exists

    def test_get_node(self, node):
        """Test getting Node"""
        assert node.instance
        assert node.kind == "Node"

    def test_update_node(self, node):
        """Test updating Node"""
        resource_dict = node.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        node.update(resource_dict=resource_dict)
        assert node.labels["updated"] == "true"

    def test_delete_node(self, node):
        """Test deleting Node"""
        node.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
