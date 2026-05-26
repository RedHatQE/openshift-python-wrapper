import pytest

from ocp_resources.user import User


@pytest.mark.incremental
class TestUser:
    @pytest.fixture(scope="class")
    def user(self, fake_client):
        return User(
            client=fake_client,
            name="test-user",
            groups=["test-groups"],
        )

    def test_01_create_user(self, user):
        """Test creating User"""
        deployed_resource = user.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-user"
        assert user.exists

    def test_02_get_user(self, user):
        """Test getting User"""
        assert user.instance
        assert user.kind == "User"

    def test_03_update_user(self, user):
        """Test updating User"""
        resource_dict = user.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        user.update(resource_dict=resource_dict)
        assert user.labels["updated"] == "true"

    def test_04_delete_user(self, user):
        """Test deleting User"""
        user.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not user.exists
