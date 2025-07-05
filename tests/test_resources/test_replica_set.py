import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.replica_set import ReplicaSet


class TestReplicaSet:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def replicaset(self, client):
        return ReplicaSet(
            client=client,
            name="test-replicaset",
            namespace="default",
            selector={"matchLabels": {"app": "test"}},
        )

    def test_create_replicaset(self, replicaset):
        """Test creating ReplicaSet"""
        deployed_resource = replicaset.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-replicaset"
        assert replicaset.exists

    def test_get_replicaset(self, replicaset):
        """Test getting ReplicaSet"""
        assert replicaset.instance
        assert replicaset.kind == "ReplicaSet"

    def test_update_replicaset(self, replicaset):
        """Test updating ReplicaSet"""
        resource_dict = replicaset.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        replicaset.update(resource_dict=resource_dict)
        assert replicaset.labels["updated"] == "true"

    def test_delete_replicaset(self, replicaset):
        """Test deleting ReplicaSet"""
        replicaset.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
