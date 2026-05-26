import pytest

from ocp_resources.pod import Pod


@pytest.mark.incremental
class TestPod:
    @pytest.fixture(scope="class")
    def pod(self, fake_client):
        return Pod(
            client=fake_client,
            name="test-pod",
            namespace="default",
            containers=[{"name": "test-container", "image": "nginx:latest"}],
        )

    def test_01_create_pod(self, pod):
        """Test creating Pod"""
        deployed_resource = pod.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-pod"
        assert pod.exists

    def test_02_get_pod(self, pod):
        """Test getting Pod"""
        assert pod.instance
        assert pod.kind == "Pod"

    def test_03_update_pod(self, pod):
        """Test updating Pod"""
        resource_dict = pod.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        pod.update(resource_dict=resource_dict)
        assert pod.labels["updated"] == "true"

    def test_04_delete_pod(self, pod):
        """Test deleting Pod"""
        pod.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not pod.exists
