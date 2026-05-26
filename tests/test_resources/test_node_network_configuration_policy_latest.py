import pytest

from ocp_resources.node_network_configuration_policy_latest import NodeNetworkConfigurationPolicy


@pytest.mark.incremental
class TestNodeNetworkConfigurationPolicy:
    @pytest.fixture(scope="class")
    def nodenetworkconfigurationpolicy(self, fake_client):
        return NodeNetworkConfigurationPolicy(
            client=fake_client,
            name="test-nodenetworkconfigurationpolicy",
        )

    def test_01_create_nodenetworkconfigurationpolicy(self, nodenetworkconfigurationpolicy):
        """Test creating NodeNetworkConfigurationPolicy"""
        deployed_resource = nodenetworkconfigurationpolicy.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-nodenetworkconfigurationpolicy"
        assert nodenetworkconfigurationpolicy.exists

    def test_02_get_nodenetworkconfigurationpolicy(self, nodenetworkconfigurationpolicy):
        """Test getting NodeNetworkConfigurationPolicy"""
        assert nodenetworkconfigurationpolicy.instance
        assert nodenetworkconfigurationpolicy.kind == "NodeNetworkConfigurationPolicy"

    def test_03_update_nodenetworkconfigurationpolicy(self, nodenetworkconfigurationpolicy):
        """Test updating NodeNetworkConfigurationPolicy"""
        resource_dict = nodenetworkconfigurationpolicy.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        nodenetworkconfigurationpolicy.update(resource_dict=resource_dict)
        assert nodenetworkconfigurationpolicy.labels["updated"] == "true"

    def test_04_delete_nodenetworkconfigurationpolicy(self, nodenetworkconfigurationpolicy):
        """Test deleting NodeNetworkConfigurationPolicy"""
        nodenetworkconfigurationpolicy.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not nodenetworkconfigurationpolicy.exists
