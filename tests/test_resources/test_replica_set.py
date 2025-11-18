import pytest

from ocp_resources.replica_set import ReplicaSet


@pytest.mark.incremental
class TestReplicaSet:
    @pytest.fixture(scope="class")
    def replicaset(self, fake_client):
        return ReplicaSet(
            client=fake_client,
            name="test-replicaset",
            namespace="default",
            selector={"matchLabels": {"app": "test"}},
        )

    def test_01_create_replicaset(self, replicaset):
        """Test creating ReplicaSet"""
        deployed_resource = replicaset.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-replicaset"
        assert replicaset.exists

    def test_02_get_replicaset(self, replicaset):
        """Test getting ReplicaSet"""
        assert replicaset.instance
        assert replicaset.kind == "ReplicaSet"

    def test_03_update_replicaset(self, replicaset):
        """Test updating ReplicaSet"""
        resource_dict = replicaset.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        replicaset.update(resource_dict=resource_dict)
        assert replicaset.labels["updated"] == "true"

    def test_04_delete_replicaset(self, replicaset):
        """Test deleting ReplicaSet"""
        replicaset.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not replicaset.exists
