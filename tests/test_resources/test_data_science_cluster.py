import pytest

from ocp_resources.data_science_cluster import DataScienceCluster


@pytest.mark.incremental
class TestDataScienceCluster:
    @pytest.fixture(scope="class")
    def datasciencecluster(self, fake_client):
        return DataScienceCluster(
            client=fake_client,
            name="test-datasciencecluster",
        )

    def test_01_create_datasciencecluster(self, datasciencecluster):
        """Test creating DataScienceCluster"""
        deployed_resource = datasciencecluster.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-datasciencecluster"
        assert datasciencecluster.exists

    def test_02_get_datasciencecluster(self, datasciencecluster):
        """Test getting DataScienceCluster"""
        assert datasciencecluster.instance
        assert datasciencecluster.kind == "DataScienceCluster"

    def test_03_update_datasciencecluster(self, datasciencecluster):
        """Test updating DataScienceCluster"""
        resource_dict = datasciencecluster.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        datasciencecluster.update(resource_dict=resource_dict)
        assert datasciencecluster.labels["updated"] == "true"

    def test_04_delete_datasciencecluster(self, datasciencecluster):
        """Test deleting DataScienceCluster"""
        datasciencecluster.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not datasciencecluster.exists
