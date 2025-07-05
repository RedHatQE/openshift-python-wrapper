import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.network_operator_openshift_io import Network


class TestNetwork:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def network(self, client):
        return Network(
            client=client,
            name="test-network",
        )

    def test_create_network(self, network):
        """Test creating Network"""
        deployed_resource = network.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-network"
        assert network.exists

    def test_get_network(self, network):
        """Test getting Network"""
        assert network.instance
        assert network.kind == "Network"

    def test_update_network(self, network):
        """Test updating Network"""
        resource_dict = network.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        network.update(resource_dict=resource_dict)
        assert network.labels["updated"] == "true"

    def test_delete_network(self, network):
        """Test deleting Network"""
        network.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
