import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.dsc_initialization import DSCInitialization


class TestDSCInitialization:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def dscinitialization(self, client):
        return DSCInitialization(
            client=client,
            name="test-dscinitialization",
            applications_namespace="test-applications_namespace",
        )

    def test_create_dscinitialization(self, dscinitialization):
        """Test creating DSCInitialization"""
        deployed_resource = dscinitialization.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-dscinitialization"
        assert dscinitialization.exists

    def test_get_dscinitialization(self, dscinitialization):
        """Test getting DSCInitialization"""
        assert dscinitialization.instance
        assert dscinitialization.kind == "DSCInitialization"

    def test_update_dscinitialization(self, dscinitialization):
        """Test updating DSCInitialization"""
        resource_dict = dscinitialization.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        dscinitialization.update(resource_dict=resource_dict)
        assert dscinitialization.labels["updated"] == "true"

    def test_delete_dscinitialization(self, dscinitialization):
        """Test deleting DSCInitialization"""
        dscinitialization.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
