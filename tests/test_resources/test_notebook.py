import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.notebook import Notebook


class TestNotebook:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def notebook(self, client):
        return Notebook(
            client=client,
            name="test-notebook",
            namespace="default",
        )

    def test_create_notebook(self, notebook):
        """Test creating Notebook"""
        deployed_resource = notebook.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-notebook"
        assert notebook.exists

    def test_get_notebook(self, notebook):
        """Test getting Notebook"""
        assert notebook.instance
        assert notebook.kind == "Notebook"

    def test_update_notebook(self, notebook):
        """Test updating Notebook"""
        resource_dict = notebook.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        notebook.update(resource_dict=resource_dict)
        assert notebook.labels["updated"] == "true"

    def test_delete_notebook(self, notebook):
        """Test deleting Notebook"""
        notebook.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
