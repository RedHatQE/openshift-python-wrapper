import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.data_science_cluster import DataScienceCluster


class TestDataScienceCluster:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def datasciencecluster(self, client):
        return DataScienceCluster(
            client=client,
            name="test-datasciencecluster",
        )

    def test_create_datasciencecluster(self, datasciencecluster):
        """Test creating DataScienceCluster"""
        deployed_resource = datasciencecluster.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-datasciencecluster"
        assert datasciencecluster.exists

    def test_get_datasciencecluster(self, datasciencecluster):
        """Test getting DataScienceCluster"""
        assert datasciencecluster.instance
        assert datasciencecluster.kind == "DataScienceCluster"

    def test_update_datasciencecluster(self, datasciencecluster):
        """Test updating DataScienceCluster"""
        resource_dict = datasciencecluster.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        datasciencecluster.update(resource_dict=resource_dict)
        assert datasciencecluster.labels["updated"] == "true"

    def test_delete_datasciencecluster(self, datasciencecluster):
        """Test deleting DataScienceCluster"""
        datasciencecluster.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
