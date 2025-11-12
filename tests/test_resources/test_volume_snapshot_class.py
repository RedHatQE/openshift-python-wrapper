import pytest

from ocp_resources.volume_snapshot_class import VolumeSnapshotClass


@pytest.mark.incremental
class TestVolumeSnapshotClass:
    @pytest.fixture(scope="class")
    def volumesnapshotclass(self, fake_client):
        return VolumeSnapshotClass(
            client=fake_client,
            name="test-volumesnapshotclass",
            deletion_policy="Delete",
            driver="example.com/csi-driver",
        )

    def test_01_create_volumesnapshotclass(self, volumesnapshotclass):
        """Test creating VolumeSnapshotClass"""
        deployed_resource = volumesnapshotclass.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-volumesnapshotclass"
        assert volumesnapshotclass.exists

    def test_02_get_volumesnapshotclass(self, volumesnapshotclass):
        """Test getting VolumeSnapshotClass"""
        assert volumesnapshotclass.instance
        assert volumesnapshotclass.kind == "VolumeSnapshotClass"

    def test_03_update_volumesnapshotclass(self, volumesnapshotclass):
        """Test updating VolumeSnapshotClass"""
        resource_dict = volumesnapshotclass.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        volumesnapshotclass.update(resource_dict=resource_dict)
        assert volumesnapshotclass.labels["updated"] == "true"

    def test_04_delete_volumesnapshotclass(self, volumesnapshotclass):
        """Test deleting VolumeSnapshotClass"""
        volumesnapshotclass.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not volumesnapshotclass.exists
