import pytest

from ocp_resources.mariadb_operator import MariadbOperator


@pytest.mark.incremental
class TestMariadbOperator:
    @pytest.fixture(scope="class")
    def mariadboperator(self, fake_client):
        return MariadbOperator(
            client=fake_client,
            name="test-mariadboperator",
            namespace="default",
        )

    def test_01_create_mariadboperator(self, mariadboperator):
        """Test creating MariadbOperator"""
        deployed_resource = mariadboperator.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-mariadboperator"
        assert mariadboperator.exists

    def test_02_get_mariadboperator(self, mariadboperator):
        """Test getting MariadbOperator"""
        assert mariadboperator.instance
        assert mariadboperator.kind == "MariadbOperator"

    def test_03_update_mariadboperator(self, mariadboperator):
        """Test updating MariadbOperator"""
        resource_dict = mariadboperator.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        mariadboperator.update(resource_dict=resource_dict)
        assert mariadboperator.labels["updated"] == "true"

    def test_04_delete_mariadboperator(self, mariadboperator):
        """Test deleting MariadbOperator"""
        mariadboperator.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not mariadboperator.exists
