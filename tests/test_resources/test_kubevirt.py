import pytest

from ocp_resources.kubevirt import KubeVirt


@pytest.mark.incremental
class TestKubeVirt:
    @pytest.fixture(scope="class")
    def kubevirt(self, fake_client):
        return KubeVirt(
            client=fake_client,
            name="test-kubevirt",
            namespace="default",
        )

    def test_01_create_kubevirt(self, kubevirt):
        """Test creating KubeVirt"""
        deployed_resource = kubevirt.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-kubevirt"
        assert kubevirt.exists

    def test_02_get_kubevirt(self, kubevirt):
        """Test getting KubeVirt"""
        assert kubevirt.instance
        assert kubevirt.kind == "KubeVirt"

    def test_03_update_kubevirt(self, kubevirt):
        """Test updating KubeVirt"""
        resource_dict = kubevirt.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        kubevirt.update(resource_dict=resource_dict)
        assert kubevirt.labels["updated"] == "true"

    def test_04_delete_kubevirt(self, kubevirt):
        """Test deleting KubeVirt"""
        kubevirt.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not kubevirt.exists
