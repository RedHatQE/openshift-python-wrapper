import pytest

from ocp_resources.user_defined_network import UserDefinedNetwork


@pytest.mark.incremental
class TestUserDefinedNetwork:
    @pytest.fixture(scope="class")
    def userdefinednetwork(self, fake_client):
        return UserDefinedNetwork(
            client=fake_client,
            name="test-userdefinednetwork",
            namespace="default",
            topology="Layer2",
        )

    def test_01_create_userdefinednetwork(self, userdefinednetwork):
        """Test creating UserDefinedNetwork"""
        deployed_resource = userdefinednetwork.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-userdefinednetwork"
        assert userdefinednetwork.exists

    def test_02_get_userdefinednetwork(self, userdefinednetwork):
        """Test getting UserDefinedNetwork"""
        assert userdefinednetwork.instance
        assert userdefinednetwork.kind == "UserDefinedNetwork"

    def test_03_update_userdefinednetwork(self, userdefinednetwork):
        """Test updating UserDefinedNetwork"""
        resource_dict = userdefinednetwork.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        userdefinednetwork.update(resource_dict=resource_dict)
        assert userdefinednetwork.labels["updated"] == "true"

    def test_04_delete_userdefinednetwork(self, userdefinednetwork):
        """Test deleting UserDefinedNetwork"""
        userdefinednetwork.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not userdefinednetwork.exists
