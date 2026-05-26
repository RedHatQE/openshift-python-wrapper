import pytest

from ocp_resources.operator import Operator


@pytest.mark.incremental
class TestOperator:
    @pytest.fixture(scope="class")
    def operator(self, fake_client):
        return Operator(
            client=fake_client,
            name="test-operator",
        )

    def test_01_create_operator(self, operator):
        """Test creating Operator"""
        deployed_resource = operator.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-operator"
        assert operator.exists

    def test_02_get_operator(self, operator):
        """Test getting Operator"""
        assert operator.instance
        assert operator.kind == "Operator"

    def test_03_update_operator(self, operator):
        """Test updating Operator"""
        resource_dict = operator.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        operator.update(resource_dict=resource_dict)
        assert operator.labels["updated"] == "true"

    def test_04_delete_operator(self, operator):
        """Test deleting Operator"""
        operator.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not operator.exists
