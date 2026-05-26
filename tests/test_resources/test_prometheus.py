import pytest

from ocp_resources.prometheus import Prometheus


@pytest.mark.incremental
class TestPrometheus:
    @pytest.fixture(scope="class")
    def prometheus(self, fake_client):
        return Prometheus(
            client=fake_client,
            name="test-prometheus",
            namespace="default",
        )

    def test_01_create_prometheus(self, prometheus):
        """Test creating Prometheus"""
        deployed_resource = prometheus.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-prometheus"
        assert prometheus.exists

    def test_02_get_prometheus(self, prometheus):
        """Test getting Prometheus"""
        assert prometheus.instance
        assert prometheus.kind == "Prometheus"

    def test_03_update_prometheus(self, prometheus):
        """Test updating Prometheus"""
        resource_dict = prometheus.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        prometheus.update(resource_dict=resource_dict)
        assert prometheus.labels["updated"] == "true"

    def test_04_delete_prometheus(self, prometheus):
        """Test deleting Prometheus"""
        prometheus.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not prometheus.exists
