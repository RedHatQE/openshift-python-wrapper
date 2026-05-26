import pytest

from ocp_resources.mig_analytic import MigAnalytic


@pytest.mark.incremental
class TestMigAnalytic:
    @pytest.fixture(scope="class")
    def miganalytic(self, fake_client):
        return MigAnalytic(
            client=fake_client,
            name="test-miganalytic",
            namespace="default",
            analyze_image_count=True,
            analyze_k8s_resources=True,
            analyze_pv_capacity=True,
            mig_plan_ref={"test-mig_plan_ref": "test-value"},
        )

    def test_01_create_miganalytic(self, miganalytic):
        """Test creating MigAnalytic"""
        deployed_resource = miganalytic.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-miganalytic"
        assert miganalytic.exists

    def test_02_get_miganalytic(self, miganalytic):
        """Test getting MigAnalytic"""
        assert miganalytic.instance
        assert miganalytic.kind == "MigAnalytic"

    def test_03_update_miganalytic(self, miganalytic):
        """Test updating MigAnalytic"""
        resource_dict = miganalytic.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        miganalytic.update(resource_dict=resource_dict)
        assert miganalytic.labels["updated"] == "true"

    def test_04_delete_miganalytic(self, miganalytic):
        """Test deleting MigAnalytic"""
        miganalytic.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not miganalytic.exists
