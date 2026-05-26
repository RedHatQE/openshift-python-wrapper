import pytest

from ocp_resources.service_serving_knative_dev import Service


@pytest.mark.incremental
class TestService:
    @pytest.fixture(scope="class")
    def service(self, fake_client):
        return Service(
            client=fake_client,
            name="test-service",
            namespace="default",
            template={"spec": {"containers": [{"image": "nginx:latest", "name": "nginx"}]}},
            traffic=[{"percent": 100, "latestRevision": True}],
        )

    def test_01_create_service(self, service):
        """Test creating Service"""
        deployed_resource = service.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-service"
        assert service.exists

    def test_02_get_service(self, service):
        """Test getting Service"""
        assert service.instance
        assert service.kind == "Service"

    def test_03_update_service(self, service):
        """Test updating Service"""
        resource_dict = service.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        service.update(resource_dict=resource_dict)
        assert service.labels["updated"] == "true"

    def test_04_delete_service(self, service):
        """Test deleting Service"""
        service.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not service.exists
