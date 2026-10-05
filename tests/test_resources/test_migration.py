import pytest

from fake_kubernetes_client.dynamic_client import FakeDynamicClient
from ocp_resources.migration import Migration
from ocp_resources.utils.constants import TIMEOUT_4MINUTES


@pytest.mark.incremental
class TestMigration:
    @pytest.fixture(scope="class")
    def migration(self, fake_client: FakeDynamicClient) -> Migration:
        return Migration(
            client=fake_client,
            name="test-migration",
            namespace="default",
            plan_name="test-plan",
            plan_namespace="default",
        )

    def test_01_create_migration(self, migration: Migration) -> None:
        """Test creating Migration"""
        deployed_resource = migration.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-migration"
        assert migration.exists

    def test_02_get_migration(self, migration: Migration) -> None:
        """Test getting Migration"""
        assert migration.instance
        assert migration.kind == "Migration"

    def test_03_migration_spec(self, migration: Migration) -> None:
        """Test that Migration spec contains plan details"""
        resource_dict = migration.instance.to_dict()
        assert resource_dict["spec"]["plan"]["name"] == "test-plan"
        assert resource_dict["spec"]["plan"]["namespace"] == "default"

    def test_04_update_migration(self, migration: Migration) -> None:
        """Test updating Migration"""
        resource_dict = migration.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        migration.update(resource_dict=resource_dict)
        assert migration.labels["updated"] == "true"

    def test_05_delete_migration(self, migration: Migration) -> None:
        """Test deleting Migration"""
        migration.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not migration.exists

    def test_06_migration_with_resume_conversion(self, fake_client: FakeDynamicClient) -> None:
        """Test Migration with resume_conversion parameter"""
        migration = Migration(
            client=fake_client,
            name="test-migration-resume",
            namespace="default",
            plan_name="test-plan",
            plan_namespace="default",
            resume_conversion=True,
        )
        deployed_resource = migration.deploy()
        assert deployed_resource
        resource_dict = deployed_resource.instance.to_dict()
        assert resource_dict["spec"]["resumeConversion"] is True
        deployed_resource.clean_up(wait=False)

    def test_07_migration_with_positional_client(self, fake_client: FakeDynamicClient) -> None:
        """Preserve the existing positional constructor arguments.

        Args:
            fake_client (FakeDynamicClient): Fake Kubernetes client supplied by the fixture.
        """
        migration = Migration(
            "test-migration-positional",
            "default",
            "test-plan",
            "default",
            None,
            fake_client,
            True,
            None,
            TIMEOUT_4MINUTES,
        )
        assert migration.client is fake_client
        deployed_resource = migration.deploy()
        assert "resumeConversion" not in deployed_resource.instance.to_dict()["spec"]
        deployed_resource.clean_up(wait=False)
