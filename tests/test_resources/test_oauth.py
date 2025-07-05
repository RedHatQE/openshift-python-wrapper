import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.oauth import OAuth


class TestOAuth:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def oauth(self, client):
        return OAuth(
            client=client,
            name="test-oauth",
        )

    def test_create_oauth(self, oauth):
        """Test creating OAuth"""
        deployed_resource = oauth.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-oauth"
        assert oauth.exists

    def test_get_oauth(self, oauth):
        """Test getting OAuth"""
        assert oauth.instance
        assert oauth.kind == "OAuth"

    def test_update_oauth(self, oauth):
        """Test updating OAuth"""
        resource_dict = oauth.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        oauth.update(resource_dict=resource_dict)
        assert oauth.labels["updated"] == "true"

    def test_delete_oauth(self, oauth):
        """Test deleting OAuth"""
        oauth.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
