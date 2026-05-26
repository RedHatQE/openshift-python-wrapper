import pytest

from ocp_resources.network_config_openshift_io import Network


@pytest.mark.incremental
class TestNetwork:
    @pytest.fixture(scope="class")
    def network(self, fake_client):
        return Network(
            client=fake_client,
            name="test-network",
        )

    def test_01_create_network(self, network):
        """Test creating Network"""
        deployed_resource = network.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-network"
        assert network.exists

    def test_02_get_network(self, network):
        """Test getting Network"""
        assert network.instance
        assert network.kind == "Network"

    def test_03_update_network(self, network):
        """Test updating Network"""
        resource_dict = network.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        network.update(resource_dict=resource_dict)
        assert network.labels["updated"] == "true"

    def test_04_delete_network(self, network):
        """Test deleting Network"""
        network.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not network.exists
