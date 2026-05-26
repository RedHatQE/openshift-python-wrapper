import pytest

from ocp_resources.direct_volume_migration_progress import DirectVolumeMigrationProgress


@pytest.mark.incremental
class TestDirectVolumeMigrationProgress:
    @pytest.fixture(scope="class")
    def directvolumemigrationprogress(self, fake_client):
        return DirectVolumeMigrationProgress(
            client=fake_client,
            name="test-directvolumemigrationprogress",
            namespace="default",
        )

    def test_01_create_directvolumemigrationprogress(self, directvolumemigrationprogress):
        """Test creating DirectVolumeMigrationProgress"""
        deployed_resource = directvolumemigrationprogress.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-directvolumemigrationprogress"
        assert directvolumemigrationprogress.exists

    def test_02_get_directvolumemigrationprogress(self, directvolumemigrationprogress):
        """Test getting DirectVolumeMigrationProgress"""
        assert directvolumemigrationprogress.instance
        assert directvolumemigrationprogress.kind == "DirectVolumeMigrationProgress"

    def test_03_update_directvolumemigrationprogress(self, directvolumemigrationprogress):
        """Test updating DirectVolumeMigrationProgress"""
        resource_dict = directvolumemigrationprogress.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        directvolumemigrationprogress.update(resource_dict=resource_dict)
        assert directvolumemigrationprogress.labels["updated"] == "true"

    def test_04_delete_directvolumemigrationprogress(self, directvolumemigrationprogress):
        """Test deleting DirectVolumeMigrationProgress"""
        directvolumemigrationprogress.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not directvolumemigrationprogress.exists
