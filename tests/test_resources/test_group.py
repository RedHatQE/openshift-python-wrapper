import pytest

from ocp_resources.group import Group


@pytest.mark.incremental
class TestGroup:
    @pytest.fixture(scope="class")
    def group(self, fake_client):
        return Group(
            client=fake_client,
            name="test-group",
            users=["test-users"],
        )

    def test_01_create_group(self, group):
        """Test creating Group"""
        deployed_resource = group.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-group"
        assert group.exists

    def test_02_get_group(self, group):
        """Test getting Group"""
        assert group.instance
        assert group.kind == "Group"

    def test_03_update_group(self, group):
        """Test updating Group"""
        resource_dict = group.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        group.update(resource_dict=resource_dict)
        assert group.labels["updated"] == "true"

    def test_04_delete_group(self, group):
        """Test deleting Group"""
        group.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not group.exists
