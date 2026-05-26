import pytest

from ocp_resources.maria_db import MariaDB


@pytest.mark.incremental
class TestMariaDB:
    @pytest.fixture(scope="class")
    def mariadb(self, fake_client):
        return MariaDB(
            client=fake_client,
            name="test-mariadb",
            namespace="default",
        )

    def test_01_create_mariadb(self, mariadb):
        """Test creating MariaDB"""
        deployed_resource = mariadb.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-mariadb"
        assert mariadb.exists

    def test_02_get_mariadb(self, mariadb):
        """Test getting MariaDB"""
        assert mariadb.instance
        assert mariadb.kind == "MariaDB"

    def test_03_update_mariadb(self, mariadb):
        """Test updating MariaDB"""
        resource_dict = mariadb.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        mariadb.update(resource_dict=resource_dict)
        assert mariadb.labels["updated"] == "true"

    def test_04_delete_mariadb(self, mariadb):
        """Test deleting MariaDB"""
        mariadb.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not mariadb.exists
