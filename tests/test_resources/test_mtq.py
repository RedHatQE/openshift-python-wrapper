import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.mtq import MTQ


@pytest.mark.incremental
class TestMTQ:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def mtq(self, client):
        return MTQ(
            client=client,
            name="test-mtq",
        )

    def test_01_create_mtq(self, mtq):
        """Test creating MTQ"""
        deployed_resource = mtq.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-mtq"
        assert mtq.exists

    def test_02_get_mtq(self, mtq):
        """Test getting MTQ"""
        assert mtq.instance
        assert mtq.kind == "MTQ"

    def test_03_update_mtq(self, mtq):
        """Test updating MTQ"""
        resource_dict = mtq.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        mtq.update(resource_dict=resource_dict)
        assert mtq.labels["updated"] == "true"

    def test_04_delete_mtq(self, mtq):
        """Test deleting MTQ"""
        mtq.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not mtq.exists
