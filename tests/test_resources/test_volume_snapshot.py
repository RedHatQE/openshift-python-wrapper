import pytest

from ocp_resources.volume_snapshot import VolumeSnapshot


@pytest.mark.incremental
class TestVolumeSnapshot:
    @pytest.fixture(scope="class")
    def volumesnapshot(self, fake_client):
        return VolumeSnapshot(
            client=fake_client,
            name="test-volumesnapshot",
            namespace="default",
            source={"test-source": "test-value"},
        )

    def test_01_create_volumesnapshot(self, volumesnapshot):
        """Test creating VolumeSnapshot"""
        deployed_resource = volumesnapshot.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-volumesnapshot"
        assert volumesnapshot.exists

    def test_02_get_volumesnapshot(self, volumesnapshot):
        """Test getting VolumeSnapshot"""
        assert volumesnapshot.instance
        assert volumesnapshot.kind == "VolumeSnapshot"

    def test_03_update_volumesnapshot(self, volumesnapshot):
        """Test updating VolumeSnapshot"""
        resource_dict = volumesnapshot.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        volumesnapshot.update(resource_dict=resource_dict)
        assert volumesnapshot.labels["updated"] == "true"

    def test_04_delete_volumesnapshot(self, volumesnapshot):
        """Test deleting VolumeSnapshot"""
        volumesnapshot.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not volumesnapshot.exists
