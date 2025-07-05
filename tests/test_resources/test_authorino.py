import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.authorino import Authorino


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
            listener="test-listener",
            oidc_server="test-oidc_server",
        )

    def test_create_authorino(self, authorino):
        """Test creating Authorino"""
        deployed_resource = authorino.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-authorino"
        assert authorino.exists

    def test_get_authorino(self, authorino):
        """Test getting Authorino"""
        assert authorino.instance
        assert authorino.kind == "Authorino"

    def test_update_authorino(self, authorino):
        """Test updating Authorino"""
        resource_dict = authorino.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        authorino.update(resource_dict=resource_dict)
        assert authorino.labels["updated"] == "true"

    def test_delete_authorino(self, authorino):
        """Test deleting Authorino"""
        authorino.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
