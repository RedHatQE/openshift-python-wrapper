import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.cluster_user_defined_network import ClusterUserDefinedNetwork


class TestClusterUserDefinedNetwork:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def clusteruserdefinednetwork(self, client):
        return ClusterUserDefinedNetwork(
            client=client,
            name="test-clusteruserdefinednetwork",
            namespace_selector="test-namespace_selector",
            network="test-network",
        )

    def test_create_clusteruserdefinednetwork(self, clusteruserdefinednetwork):
        """Test creating ClusterUserDefinedNetwork"""
        deployed_resource = clusteruserdefinednetwork.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-clusteruserdefinednetwork"
        assert clusteruserdefinednetwork.exists

    def test_get_clusteruserdefinednetwork(self, clusteruserdefinednetwork):
        """Test getting ClusterUserDefinedNetwork"""
        assert clusteruserdefinednetwork.instance
        assert clusteruserdefinednetwork.kind == "ClusterUserDefinedNetwork"

    def test_update_clusteruserdefinednetwork(self, clusteruserdefinednetwork):
        """Test updating ClusterUserDefinedNetwork"""
        resource_dict = clusteruserdefinednetwork.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        clusteruserdefinednetwork.update(resource_dict=resource_dict)
        assert clusteruserdefinednetwork.labels["updated"] == "true"

    def test_delete_clusteruserdefinednetwork(self, clusteruserdefinednetwork):
        """Test deleting ClusterUserDefinedNetwork"""
        clusteruserdefinednetwork.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
