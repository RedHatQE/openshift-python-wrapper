import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.node_network_configuration_policy_latest import NodeNetworkConfigurationPolicy


class TestNodeNetworkConfigurationPolicy:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def nodenetworkconfigurationpolicy(self, client):
        return NodeNetworkConfigurationPolicy(
            client=client,
            name="test-nodenetworkconfigurationpolicy",
        )

    def test_create_nodenetworkconfigurationpolicy(self, nodenetworkconfigurationpolicy):
        """Test creating NodeNetworkConfigurationPolicy"""
        deployed_resource = nodenetworkconfigurationpolicy.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-nodenetworkconfigurationpolicy"
        assert nodenetworkconfigurationpolicy.exists

    def test_get_nodenetworkconfigurationpolicy(self, nodenetworkconfigurationpolicy):
        """Test getting NodeNetworkConfigurationPolicy"""
        assert nodenetworkconfigurationpolicy.instance
        assert nodenetworkconfigurationpolicy.kind == "NodeNetworkConfigurationPolicy"

    def test_update_nodenetworkconfigurationpolicy(self, nodenetworkconfigurationpolicy):
        """Test updating NodeNetworkConfigurationPolicy"""
        resource_dict = nodenetworkconfigurationpolicy.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        nodenetworkconfigurationpolicy.update(resource_dict=resource_dict)
        assert nodenetworkconfigurationpolicy.labels["updated"] == "true"

    def test_delete_nodenetworkconfigurationpolicy(self, nodenetworkconfigurationpolicy):
        """Test deleting NodeNetworkConfigurationPolicy"""
        nodenetworkconfigurationpolicy.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not nodenetworkconfigurationpolicy.exists
