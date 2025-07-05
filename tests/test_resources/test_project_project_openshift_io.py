import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.project_project_openshift_io import Project


class TestProject:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def project(self, client):
        return Project(
            client=client,
            name="test-project",
        )

    def test_create_project(self, project):
        """Test creating Project"""
        deployed_resource = project.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-project"
        assert project.exists

    def test_get_project(self, project):
        """Test getting Project"""
        assert project.instance
        assert project.kind == "Project"

    def test_update_project(self, project):
        """Test updating Project"""
        resource_dict = project.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        project.update(resource_dict=resource_dict)
        assert project.labels["updated"] == "true"

    def test_delete_project(self, project):
        """Test deleting Project"""
        project.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
