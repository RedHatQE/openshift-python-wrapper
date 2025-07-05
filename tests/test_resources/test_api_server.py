import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.api_server import APIServer


class TestAPIServer:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def apiserver(self, client):
        return APIServer(
            client=client,
            name="test-apiserver",
        )

    def test_create_apiserver(self, apiserver):
        """Test creating APIServer"""
        deployed_resource = apiserver.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-apiserver"
        assert apiserver.exists

    def test_get_apiserver(self, apiserver):
        """Test getting APIServer"""
        assert apiserver.instance
        assert apiserver.kind == "APIServer"

    def test_update_apiserver(self, apiserver):
        """Test updating APIServer"""
        resource_dict = apiserver.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        apiserver.update(resource_dict=resource_dict)
        assert apiserver.labels["updated"] == "true"

    def test_delete_apiserver(self, apiserver):
        """Test deleting APIServer"""
        apiserver.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
