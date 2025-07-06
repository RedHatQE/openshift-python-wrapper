import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.operator import Operator


class TestOperator:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def operator(self, client):
        return Operator(
            client=client,
            name="test-operator",
        )

    def test_create_operator(self, operator):
        """Test creating Operator"""
        deployed_resource = operator.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-operator"
        assert operator.exists

    def test_get_operator(self, operator):
        """Test getting Operator"""
        assert operator.instance
        assert operator.kind == "Operator"

    def test_update_operator(self, operator):
        """Test updating Operator"""
        resource_dict = operator.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        operator.update(resource_dict=resource_dict)
        assert operator.labels["updated"] == "true"

    def test_delete_operator(self, operator):
        """Test deleting Operator"""
        operator.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not operator.exists
