import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.llama_stack_distribution import LlamaStackDistribution


@pytest.mark.incremental
class TestLlamaStackDistribution:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def llamastackdistribution(self, client):
        return LlamaStackDistribution(
            client=client,
            name="test-llamastackdistribution",
            namespace="default",
            server={"test-server": "test-value"},
        )

    def test_01_create_llamastackdistribution(self, llamastackdistribution):
        """Test creating LlamaStackDistribution"""
        deployed_resource = llamastackdistribution.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-llamastackdistribution"
        assert llamastackdistribution.exists

    def test_02_get_llamastackdistribution(self, llamastackdistribution):
        """Test getting LlamaStackDistribution"""
        assert llamastackdistribution.instance
        assert llamastackdistribution.kind == "LlamaStackDistribution"

    def test_03_update_llamastackdistribution(self, llamastackdistribution):
        """Test updating LlamaStackDistribution"""
        resource_dict = llamastackdistribution.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        llamastackdistribution.update(resource_dict=resource_dict)
        assert llamastackdistribution.labels["updated"] == "true"

    def test_04_delete_llamastackdistribution(self, llamastackdistribution):
        """Test deleting LlamaStackDistribution"""
        llamastackdistribution.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not llamastackdistribution.exists
