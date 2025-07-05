import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.ssp import SSP


class TestSSP:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def ssp(self, client):
        return SSP(
            client=client,
            name="test-ssp",
            namespace="default",
            common_templates="test-common_templates",
        )

    def test_create_ssp(self, ssp):
        """Test creating SSP"""
        deployed_resource = ssp.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-ssp"
        assert ssp.exists

    def test_get_ssp(self, ssp):
        """Test getting SSP"""
        assert ssp.instance
        assert ssp.kind == "SSP"

    def test_update_ssp(self, ssp):
        """Test updating SSP"""
        resource_dict = ssp.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        ssp.update(resource_dict=resource_dict)
        assert ssp.labels["updated"] == "true"

    def test_delete_ssp(self, ssp):
        """Test deleting SSP"""
        ssp.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
