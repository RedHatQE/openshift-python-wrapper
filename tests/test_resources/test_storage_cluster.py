import pytest

from ocp_resources.storage_cluster import StorageCluster


@pytest.mark.incremental
class TestStorageCluster:
    @pytest.fixture(scope="class")
    def storagecluster(self, fake_client):
        return StorageCluster(
            client=fake_client,
            name="test-storagecluster",
            namespace="default",
        )

    def test_01_create_storagecluster(self, storagecluster):
        """Test creating StorageCluster"""
        deployed_resource = storagecluster.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-storagecluster"
        assert storagecluster.exists

    def test_02_get_storagecluster(self, storagecluster):
        """Test getting StorageCluster"""
        assert storagecluster.instance
        assert storagecluster.kind == "StorageCluster"

    def test_03_update_storagecluster(self, storagecluster):
        """Test updating StorageCluster"""
        resource_dict = storagecluster.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        storagecluster.update(resource_dict=resource_dict)
        assert storagecluster.labels["updated"] == "true"

    def test_04_delete_storagecluster(self, storagecluster):
        """Test deleting StorageCluster"""
        storagecluster.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not storagecluster.exists
