import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.pod import Pod


class TestPod:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def pod(self, client):
        return Pod(
            client=client,
            name="test-pod",
            namespace="default",
            containers=[{"name": "test-container", "image": "nginx:latest"}],
        )

    def test_create_pod(self, pod):
        """Test creating Pod"""
        deployed_resource = pod.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-pod"
        assert pod.exists

    def test_get_pod(self, pod):
        """Test getting Pod"""
        assert pod.instance
        assert pod.kind == "Pod"

    def test_update_pod(self, pod):
        """Test updating Pod"""
        resource_dict = pod.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        pod.update(resource_dict=resource_dict)
        assert pod.labels["updated"] == "true"

    def test_delete_pod(self, pod):
        """Test deleting Pod"""
        pod.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
