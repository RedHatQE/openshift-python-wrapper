import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.prometheus import Prometheus


class TestPrometheus:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def prometheus(self, client):
        return Prometheus(
            client=client,
            name="test-prometheus",
            namespace="default",
        )

    def test_create_prometheus(self, prometheus):
        """Test creating Prometheus"""
        deployed_resource = prometheus.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-prometheus"
        assert prometheus.exists

    def test_get_prometheus(self, prometheus):
        """Test getting Prometheus"""
        assert prometheus.instance
        assert prometheus.kind == "Prometheus"

    def test_update_prometheus(self, prometheus):
        """Test updating Prometheus"""
        resource_dict = prometheus.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        prometheus.update(resource_dict=resource_dict)
        assert prometheus.labels["updated"] == "true"

    def test_delete_prometheus(self, prometheus):
        """Test deleting Prometheus"""
        prometheus.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not prometheus.exists
