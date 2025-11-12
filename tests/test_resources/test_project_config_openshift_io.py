import pytest

from ocp_resources.project_config_openshift_io import Project


@pytest.mark.incremental
class TestProject:
    @pytest.fixture(scope="class")
    def project(self, fake_client):
        return Project(
            client=fake_client,
            name="test-project",
        )

    def test_01_create_project(self, project):
        """Test creating Project"""
        deployed_resource = project.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-project"
        assert project.exists

    def test_02_get_project(self, project):
        """Test getting Project"""
        assert project.instance
        assert project.kind == "Project"

    def test_03_update_project(self, project):
        """Test updating Project"""
        resource_dict = project.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        project.update(resource_dict=resource_dict)
        assert project.labels["updated"] == "true"

    def test_04_delete_project(self, project):
        """Test deleting Project"""
        project.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not project.exists
