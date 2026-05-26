import pytest

from ocp_resources.kube_descheduler import KubeDescheduler


@pytest.mark.incremental
class TestKubeDescheduler:
    @pytest.fixture(scope="class")
    def kubedescheduler(self, fake_client):
        return KubeDescheduler(
            client=fake_client,
            name="test-kubedescheduler",
            namespace="default",
        )

    def test_01_create_kubedescheduler(self, kubedescheduler):
        """Test creating KubeDescheduler"""
        deployed_resource = kubedescheduler.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-kubedescheduler"
        assert kubedescheduler.exists

    def test_02_get_kubedescheduler(self, kubedescheduler):
        """Test getting KubeDescheduler"""
        assert kubedescheduler.instance
        assert kubedescheduler.kind == "KubeDescheduler"

    def test_03_update_kubedescheduler(self, kubedescheduler):
        """Test updating KubeDescheduler"""
        resource_dict = kubedescheduler.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        kubedescheduler.update(resource_dict=resource_dict)
        assert kubedescheduler.labels["updated"] == "true"

    def test_04_delete_kubedescheduler(self, kubedescheduler):
        """Test deleting KubeDescheduler"""
        kubedescheduler.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not kubedescheduler.exists
