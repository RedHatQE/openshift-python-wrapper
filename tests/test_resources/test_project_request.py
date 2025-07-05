import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.project_request import ProjectRequest


class TestProjectRequest:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def projectrequest(self, client):
        return ProjectRequest(
            client=client,
            name="test-projectrequest",
        )

    def test_create_projectrequest(self, projectrequest):
        """Test creating ProjectRequest"""
        deployed_resource = projectrequest.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-projectrequest"
        assert projectrequest.exists

    def test_get_projectrequest(self, projectrequest):
        """Test getting ProjectRequest"""
        assert projectrequest.instance
        assert projectrequest.kind == "ProjectRequest"

    def test_update_projectrequest(self, projectrequest):
        """Test updating ProjectRequest"""
        resource_dict = projectrequest.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        projectrequest.update(resource_dict=resource_dict)
        assert projectrequest.labels["updated"] == "true"

    def test_delete_projectrequest(self, projectrequest):
        """Test deleting ProjectRequest"""
        projectrequest.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
