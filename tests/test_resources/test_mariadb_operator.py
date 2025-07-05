import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.mariadb_operator import MariadbOperator


class TestMariadbOperator:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def mariadboperator(self, client):
        return MariadbOperator(
            client=client,
            name="test-mariadboperator",
            namespace="default",
        )

    def test_create_mariadboperator(self, mariadboperator):
        """Test creating MariadbOperator"""
        deployed_resource = mariadboperator.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-mariadboperator"
        assert mariadboperator.exists

    def test_get_mariadboperator(self, mariadboperator):
        """Test getting MariadbOperator"""
        assert mariadboperator.instance
        assert mariadboperator.kind == "MariadbOperator"

    def test_update_mariadboperator(self, mariadboperator):
        """Test updating MariadbOperator"""
        resource_dict = mariadboperator.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        mariadboperator.update(resource_dict=resource_dict)
        assert mariadboperator.labels["updated"] == "true"

    def test_delete_mariadboperator(self, mariadboperator):
        """Test deleting MariadbOperator"""
        mariadboperator.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
