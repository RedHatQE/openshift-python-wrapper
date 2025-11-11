import pytest

from ocp_resources.snapshot import Snapshot


@pytest.mark.incremental
class TestSnapshot:
    @pytest.fixture(scope="class")
    def snapshot(self, fake_client):
        return Snapshot(
            client=fake_client,
            name="test-snapshot",
            namespace="default",
            application="test-application",
        )

    def test_01_create_snapshot(self, snapshot):
        """Test creating Snapshot"""
        deployed_resource = snapshot.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-snapshot"
        assert snapshot.exists

    def test_02_get_snapshot(self, snapshot):
        """Test getting Snapshot"""
        assert snapshot.instance
        assert snapshot.kind == "Snapshot"

    def test_03_update_snapshot(self, snapshot):
        """Test updating Snapshot"""
        resource_dict = snapshot.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        snapshot.update(resource_dict=resource_dict)
        assert snapshot.labels["updated"] == "true"

    def test_04_delete_snapshot(self, snapshot):
        """Test deleting Snapshot"""
        snapshot.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not snapshot.exists
