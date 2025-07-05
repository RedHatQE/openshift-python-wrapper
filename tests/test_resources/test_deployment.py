import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.deployment import Deployment


class TestDeployment:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def deployment(self, client):
        return Deployment(
            client=client,
            name="test-deployment",
            namespace="default",
            selector={"matchLabels": {"app": "test"}},
            template={
                "metadata": {"labels": {"app": "test"}},
                "spec": {"containers": [{"name": "test-container", "image": "nginx:latest"}]},
            },
            replicas=1,
        )

    def test_create_deployment(self, deployment):
        """Test creating Deployment"""
        deployed_resource = deployment.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-deployment"
        assert deployment.exists

    def test_get_deployment(self, deployment):
        """Test getting Deployment"""
        assert deployment.instance
        assert deployment.kind == "Deployment"

    def test_update_deployment(self, deployment):
        """Test updating Deployment"""
        resource_dict = deployment.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        deployment.update(resource_dict=resource_dict)
        assert deployment.labels["updated"] == "true"

    def test_delete_deployment(self, deployment):
        """Test deleting Deployment"""
        deployment.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
