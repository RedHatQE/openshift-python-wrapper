import pytest

from ocp_resources.cluster_resource_quota import ClusterResourceQuota


@pytest.mark.incremental
class TestClusterResourceQuota:
    @pytest.fixture(scope="class")
    def clusterresourcequota(self, fake_client):
        return ClusterResourceQuota(
            client=fake_client,
            name="test-clusterresourcequota",
            quota={"test-quota": "test-value"},
            selector={"matchLabels": {"app": "test"}},
        )

    def test_01_create_clusterresourcequota(self, clusterresourcequota):
        """Test creating ClusterResourceQuota"""
        deployed_resource = clusterresourcequota.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-clusterresourcequota"
        assert clusterresourcequota.exists

    def test_02_get_clusterresourcequota(self, clusterresourcequota):
        """Test getting ClusterResourceQuota"""
        assert clusterresourcequota.instance
        assert clusterresourcequota.kind == "ClusterResourceQuota"

    def test_03_update_clusterresourcequota(self, clusterresourcequota):
        """Test updating ClusterResourceQuota"""
        resource_dict = clusterresourcequota.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        clusterresourcequota.update(resource_dict=resource_dict)
        assert clusterresourcequota.labels["updated"] == "true"

    def test_04_delete_clusterresourcequota(self, clusterresourcequota):
        """Test deleting ClusterResourceQuota"""
        clusterresourcequota.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not clusterresourcequota.exists
