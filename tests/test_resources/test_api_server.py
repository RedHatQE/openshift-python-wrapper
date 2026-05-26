import pytest

from ocp_resources.api_server import APIServer


@pytest.mark.incremental
class TestAPIServer:
    @pytest.fixture(scope="class")
    def apiserver(self, fake_client):
        return APIServer(
            client=fake_client,
            name="test-apiserver",
        )

    def test_01_create_apiserver(self, apiserver):
        """Test creating APIServer"""
        deployed_resource = apiserver.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-apiserver"
        assert apiserver.exists

    def test_02_get_apiserver(self, apiserver):
        """Test getting APIServer"""
        assert apiserver.instance
        assert apiserver.kind == "APIServer"

    def test_03_update_apiserver(self, apiserver):
        """Test updating APIServer"""
        resource_dict = apiserver.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        apiserver.update(resource_dict=resource_dict)
        assert apiserver.labels["updated"] == "true"

    def test_04_delete_apiserver(self, apiserver):
        """Test deleting APIServer"""
        apiserver.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not apiserver.exists
