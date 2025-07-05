import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.volume_snapshot import VolumeSnapshot


class TestVolumeSnapshot:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def volumesnapshot(self, client):
        return VolumeSnapshot(
            client=client,
            name="test-volumesnapshot",
            namespace="default",
            source="test-source",
        )

    def test_create_volumesnapshot(self, volumesnapshot):
        """Test creating VolumeSnapshot"""
        deployed_resource = volumesnapshot.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-volumesnapshot"
        assert volumesnapshot.exists

    def test_get_volumesnapshot(self, volumesnapshot):
        """Test getting VolumeSnapshot"""
        assert volumesnapshot.instance
        assert volumesnapshot.kind == "VolumeSnapshot"

    def test_update_volumesnapshot(self, volumesnapshot):
        """Test updating VolumeSnapshot"""
        resource_dict = volumesnapshot.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        volumesnapshot.update(resource_dict=resource_dict)
        assert volumesnapshot.labels["updated"] == "true"

    def test_delete_volumesnapshot(self, volumesnapshot):
        """Test deleting VolumeSnapshot"""
        volumesnapshot.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
