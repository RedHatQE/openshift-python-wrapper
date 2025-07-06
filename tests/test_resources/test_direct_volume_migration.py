import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.direct_volume_migration import DirectVolumeMigration


@pytest.mark.incremental
class TestDirectVolumeMigration:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def directvolumemigration(self, client):
        return DirectVolumeMigration(
            client=client,
            name="test-directvolumemigration",
            namespace="default",
        )

    def test_01_create_directvolumemigration(self, directvolumemigration):
        """Test creating DirectVolumeMigration"""
        deployed_resource = directvolumemigration.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-directvolumemigration"
        assert directvolumemigration.exists

    def test_02_get_directvolumemigration(self, directvolumemigration):
        """Test getting DirectVolumeMigration"""
        assert directvolumemigration.instance
        assert directvolumemigration.kind == "DirectVolumeMigration"

    def test_03_update_directvolumemigration(self, directvolumemigration):
        """Test updating DirectVolumeMigration"""
        resource_dict = directvolumemigration.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        directvolumemigration.update(resource_dict=resource_dict)
        assert directvolumemigration.labels["updated"] == "true"

    def test_04_delete_directvolumemigration(self, directvolumemigration):
        """Test deleting DirectVolumeMigration"""
        directvolumemigration.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not directvolumemigration.exists
