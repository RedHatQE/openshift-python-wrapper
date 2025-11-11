import pytest

from ocp_resources.kubelet_config import KubeletConfig


@pytest.mark.incremental
class TestKubeletConfig:
    @pytest.fixture(scope="class")
    def kubeletconfig(self, fake_client):
        return KubeletConfig(
            client=fake_client,
            name="test-kubeletconfig",
        )

    def test_01_create_kubeletconfig(self, kubeletconfig):
        """Test creating KubeletConfig"""
        deployed_resource = kubeletconfig.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-kubeletconfig"
        assert kubeletconfig.exists

    def test_02_get_kubeletconfig(self, kubeletconfig):
        """Test getting KubeletConfig"""
        assert kubeletconfig.instance
        assert kubeletconfig.kind == "KubeletConfig"

    def test_03_update_kubeletconfig(self, kubeletconfig):
        """Test updating KubeletConfig"""
        resource_dict = kubeletconfig.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        kubeletconfig.update(resource_dict=resource_dict)
        assert kubeletconfig.labels["updated"] == "true"

    def test_04_delete_kubeletconfig(self, kubeletconfig):
        """Test deleting KubeletConfig"""
        kubeletconfig.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not kubeletconfig.exists
