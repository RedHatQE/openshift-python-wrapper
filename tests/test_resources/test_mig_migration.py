import pytest

from ocp_resources.mig_migration import MigMigration


@pytest.mark.incremental
class TestMigMigration:
    @pytest.fixture(scope="class")
    def migmigration(self, fake_client):
        return MigMigration(
            client=fake_client,
            name="test-migmigration",
            namespace="default",
            stage=True,
        )

    def test_01_create_migmigration(self, migmigration):
        """Test creating MigMigration"""
        deployed_resource = migmigration.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-migmigration"
        assert migmigration.exists

    def test_02_get_migmigration(self, migmigration):
        """Test getting MigMigration"""
        assert migmigration.instance
        assert migmigration.kind == "MigMigration"

    def test_03_update_migmigration(self, migmigration):
        """Test updating MigMigration"""
        resource_dict = migmigration.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        migmigration.update(resource_dict=resource_dict)
        assert migmigration.labels["updated"] == "true"

    def test_04_delete_migmigration(self, migmigration):
        """Test deleting MigMigration"""
        migmigration.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not migmigration.exists
