import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.mig_analytic import MigAnalytic


class TestMigAnalytic:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def miganalytic(self, client):
        return MigAnalytic(
            client=client,
            name="test-miganalytic",
            namespace="default",
            analyze_image_count="test-analyze_image_count",
            analyze_k8s_resources="test-analyze_k8s_resources",
            analyze_pv_capacity="test-analyze_pv_capacity",
            mig_plan_ref="test-mig_plan_ref",
        )

    def test_create_miganalytic(self, miganalytic):
        """Test creating MigAnalytic"""
        deployed_resource = miganalytic.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-miganalytic"
        assert miganalytic.exists

    def test_get_miganalytic(self, miganalytic):
        """Test getting MigAnalytic"""
        assert miganalytic.instance
        assert miganalytic.kind == "MigAnalytic"

    def test_update_miganalytic(self, miganalytic):
        """Test updating MigAnalytic"""
        resource_dict = miganalytic.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        miganalytic.update(resource_dict=resource_dict)
        assert miganalytic.labels["updated"] == "true"

    def test_delete_miganalytic(self, miganalytic):
        """Test deleting MigAnalytic"""
        miganalytic.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
