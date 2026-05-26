import pytest

from ocp_resources.cluster_user_defined_network import ClusterUserDefinedNetwork


@pytest.mark.incremental
class TestClusterUserDefinedNetwork:
    @pytest.fixture(scope="class")
    def clusteruserdefinednetwork(self, fake_client):
        return ClusterUserDefinedNetwork(
            client=fake_client,
            name="test-clusteruserdefinednetwork",
            namespace_selector={"test-namespace_selector": "test-value"},
            network={"test-network": "test-value"},
        )

    def test_01_create_clusteruserdefinednetwork(self, clusteruserdefinednetwork):
        """Test creating ClusterUserDefinedNetwork"""
        deployed_resource = clusteruserdefinednetwork.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-clusteruserdefinednetwork"
        assert clusteruserdefinednetwork.exists

    def test_02_get_clusteruserdefinednetwork(self, clusteruserdefinednetwork):
        """Test getting ClusterUserDefinedNetwork"""
        assert clusteruserdefinednetwork.instance
        assert clusteruserdefinednetwork.kind == "ClusterUserDefinedNetwork"

    def test_03_update_clusteruserdefinednetwork(self, clusteruserdefinednetwork):
        """Test updating ClusterUserDefinedNetwork"""
        resource_dict = clusteruserdefinednetwork.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        clusteruserdefinednetwork.update(resource_dict=resource_dict)
        assert clusteruserdefinednetwork.labels["updated"] == "true"

    def test_04_delete_clusteruserdefinednetwork(self, clusteruserdefinednetwork):
        """Test deleting ClusterUserDefinedNetwork"""
        clusteruserdefinednetwork.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not clusteruserdefinednetwork.exists
