import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.node_config_openshift_io import Node


@pytest.mark.incremental
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

    def test_01_create_node(self, node):
        """Test creating Node"""
        deployed_resource = node.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-node"
        assert node.exists

    def test_02_get_node(self, node):
        """Test getting Node"""
        assert node.instance
        assert node.kind == "Node"

    def test_03_update_node(self, node):
        """Test updating Node"""
        resource_dict = node.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        node.update(resource_dict=resource_dict)
        assert node.labels["updated"] == "true"

    def test_04_delete_node(self, node):
        """Test deleting Node"""
        node.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not node.exists
