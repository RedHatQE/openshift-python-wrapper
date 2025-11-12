import pytest

from ocp_resources.notebook import Notebook


@pytest.mark.incremental
class TestNotebook:
    @pytest.fixture(scope="class")
    def notebook(self, fake_client):
        return Notebook(
            client=fake_client,
            name="test-notebook",
            namespace="default",
        )

    def test_01_create_notebook(self, notebook):
        """Test creating Notebook"""
        deployed_resource = notebook.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-notebook"
        assert notebook.exists

    def test_02_get_notebook(self, notebook):
        """Test getting Notebook"""
        assert notebook.instance
        assert notebook.kind == "Notebook"

    def test_03_update_notebook(self, notebook):
        """Test updating Notebook"""
        resource_dict = notebook.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        notebook.update(resource_dict=resource_dict)
        assert notebook.labels["updated"] == "true"

    def test_04_delete_notebook(self, notebook):
        """Test deleting Notebook"""
        notebook.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not notebook.exists
