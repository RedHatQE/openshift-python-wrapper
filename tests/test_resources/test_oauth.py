import pytest

from ocp_resources.oauth import OAuth


@pytest.mark.incremental
class TestOAuth:
    @pytest.fixture(scope="class")
    def oauth(self, fake_client):
        return OAuth(
            client=fake_client,
            name="test-oauth",
        )

    def test_01_create_oauth(self, oauth):
        """Test creating OAuth"""
        deployed_resource = oauth.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-oauth"
        assert oauth.exists

    def test_02_get_oauth(self, oauth):
        """Test getting OAuth"""
        assert oauth.instance
        assert oauth.kind == "OAuth"

    def test_03_update_oauth(self, oauth):
        """Test updating OAuth"""
        resource_dict = oauth.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        oauth.update(resource_dict=resource_dict)
        assert oauth.labels["updated"] == "true"

    def test_04_delete_oauth(self, oauth):
        """Test deleting OAuth"""
        oauth.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not oauth.exists
