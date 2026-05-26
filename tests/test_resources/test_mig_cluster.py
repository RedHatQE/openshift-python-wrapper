import pytest

from ocp_resources.mig_cluster import MigCluster


@pytest.mark.incremental
class TestMigCluster:
    @pytest.fixture(scope="class")
    def migcluster(self, fake_client):
        return MigCluster(
            client=fake_client,
            name="test-migcluster",
            namespace="default",
            is_host_cluster=True,
        )

    def test_01_create_migcluster(self, migcluster):
        """Test creating MigCluster"""
        deployed_resource = migcluster.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-migcluster"
        assert migcluster.exists

    def test_02_get_migcluster(self, migcluster):
        """Test getting MigCluster"""
        assert migcluster.instance
        assert migcluster.kind == "MigCluster"

    def test_03_update_migcluster(self, migcluster):
        """Test updating MigCluster"""
        resource_dict = migcluster.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        migcluster.update(resource_dict=resource_dict)
        assert migcluster.labels["updated"] == "true"

    def test_04_delete_migcluster(self, migcluster):
        """Test deleting MigCluster"""
        migcluster.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not migcluster.exists
