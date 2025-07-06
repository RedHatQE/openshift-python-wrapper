import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.mig_migration import MigMigration


class TestMigMigration:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def migmigration(self, client):
        return MigMigration(
            client=client,
            name="test-migmigration",
            namespace="default",
            stage="test-stage",
        )

    def test_create_migmigration(self, migmigration):
        """Test creating MigMigration"""
        deployed_resource = migmigration.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-migmigration"
        assert migmigration.exists

    def test_get_migmigration(self, migmigration):
        """Test getting MigMigration"""
        assert migmigration.instance
        assert migmigration.kind == "MigMigration"

    def test_update_migmigration(self, migmigration):
        """Test updating MigMigration"""
        resource_dict = migmigration.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        migmigration.update(resource_dict=resource_dict)
        assert migmigration.labels["updated"] == "true"

    def test_delete_migmigration(self, migmigration):
        """Test deleting MigMigration"""
        migmigration.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not migmigration.exists
