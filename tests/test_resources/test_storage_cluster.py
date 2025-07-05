import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.storage_cluster import StorageCluster


class TestStorageCluster:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def storagecluster(self, client):
        return StorageCluster(
            client=client,
            name="test-storagecluster",
            namespace="default",
        )

    def test_create_storagecluster(self, storagecluster):
        """Test creating StorageCluster"""
        deployed_resource = storagecluster.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-storagecluster"
        assert storagecluster.exists

    def test_get_storagecluster(self, storagecluster):
        """Test getting StorageCluster"""
        assert storagecluster.instance
        assert storagecluster.kind == "StorageCluster"

    def test_update_storagecluster(self, storagecluster):
        """Test updating StorageCluster"""
        resource_dict = storagecluster.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        storagecluster.update(resource_dict=resource_dict)
        assert storagecluster.labels["updated"] == "true"

    def test_delete_storagecluster(self, storagecluster):
        """Test deleting StorageCluster"""
        storagecluster.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
