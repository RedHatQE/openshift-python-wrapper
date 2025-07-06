import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.authorino import Authorino


@pytest.mark.incremental
class TestAuthorino:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def authorino(self, client):
        return Authorino(
            client=client,
            name="test-authorino",
            namespace="default",
            listener={"test-listener": "test-value"},
            oidc_server={"test-oidc_server": "test-value"},
        )

    def test_01_create_authorino(self, authorino):
        """Test creating Authorino"""
        deployed_resource = authorino.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-authorino"
        assert authorino.exists

    def test_02_get_authorino(self, authorino):
        """Test getting Authorino"""
        assert authorino.instance
        assert authorino.kind == "Authorino"

    def test_03_update_authorino(self, authorino):
        """Test updating Authorino"""
        resource_dict = authorino.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        authorino.update(resource_dict=resource_dict)
        assert authorino.labels["updated"] == "true"

    def test_04_delete_authorino(self, authorino):
        """Test deleting Authorino"""
        authorino.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not authorino.exists
