import pytest

from ocp_resources.console_config_openshift_io import Console


@pytest.mark.incremental
class TestConsole:
    @pytest.fixture(scope="class")
    def console(self, fake_client):
        return Console(
            client=fake_client,
            name="test-console",
        )

    def test_01_create_console(self, console):
        """Test creating Console"""
        deployed_resource = console.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-console"
        assert console.exists

    def test_02_get_console(self, console):
        """Test getting Console"""
        assert console.instance
        assert console.kind == "Console"

    def test_03_update_console(self, console):
        """Test updating Console"""
        resource_dict = console.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        console.update(resource_dict=resource_dict)
        assert console.labels["updated"] == "true"

    def test_04_delete_console(self, console):
        """Test deleting Console"""
        console.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not console.exists
