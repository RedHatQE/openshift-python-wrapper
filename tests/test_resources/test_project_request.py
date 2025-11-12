import pytest

from ocp_resources.project_project_openshift_io import Project
from ocp_resources.project_request import ProjectRequest


@pytest.mark.incremental
class TestProjectRequest:
    @pytest.fixture(scope="class")
    def projectrequest(self, fake_client):
        return ProjectRequest(
            client=fake_client,
            name="test-projectrequest",
        )

    def test_01_create_projectrequest(self, projectrequest):
        """Test creating ephemeral ProjectRequest (creates Project)"""
        # Create the ephemeral resource - this returns raw ResourceInstance
        actual_resource_instance = projectrequest.create()

        # Wrap in proper Resource object to use ocp-resources methods
        actual_resource = Project(client=projectrequest.client, name=actual_resource_instance.metadata.name)

        # Verify the actual resource was created and has correct properties
        assert actual_resource.name == "test-projectrequest"
        assert actual_resource.exists
        assert actual_resource.kind == "Project"
        # The ephemeral resource itself should not exist after creation
        assert not projectrequest.exists

    def test_02_get_projectrequest(self, projectrequest):
        """Test getting ProjectRequest properties"""
        # We can still access the ephemeral resource's properties before deployment
        assert projectrequest.kind == "ProjectRequest"
        assert projectrequest.name == "test-projectrequest"

    def test_03_delete_projectrequest(self, projectrequest):
        """Test deleting ProjectRequest (deletes Project)"""
        # First create to get the actual resource
        actual_resource_instance = projectrequest.create()

        # Wrap in proper Resource object
        actual_resource = Project(client=projectrequest.client, name=actual_resource_instance.metadata.name)
        assert actual_resource.exists

        # Clean up should delete the actual resource, not the ephemeral one
        projectrequest.clean_up(wait=False)

        # Verify the actual resource no longer exists using Resource methods
        assert not actual_resource.exists
