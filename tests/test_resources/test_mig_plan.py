import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.mig_plan import MigPlan


@pytest.mark.incremental
class TestMigPlan:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def migplan(self, client):
        return MigPlan(
            client=client,
            name="test-migplan",
            namespace="default",
        )

    def test_01_create_migplan(self, migplan):
        """Test creating MigPlan"""
        deployed_resource = migplan.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-migplan"
        assert migplan.exists

    def test_02_get_migplan(self, migplan):
        """Test getting MigPlan"""
        assert migplan.instance
        assert migplan.kind == "MigPlan"

    def test_03_update_migplan(self, migplan):
        """Test updating MigPlan"""
        resource_dict = migplan.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        migplan.update(resource_dict=resource_dict)
        assert migplan.labels["updated"] == "true"

    def test_04_delete_migplan(self, migplan):
        """Test deleting MigPlan"""
        migplan.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not migplan.exists
