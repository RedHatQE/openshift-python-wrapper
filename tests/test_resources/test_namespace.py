import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.namespace import Namespace


class TestNamespace:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def namespace(self, client):
        return Namespace(
            client=client,
            name="test-namespace",
        )

    def test_create_namespace(self, namespace):
        """Test creating Namespace"""
        deployed_resource = namespace.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-namespace"
        assert namespace.exists

    def test_get_namespace(self, namespace):
        """Test getting Namespace"""
        assert namespace.instance
        assert namespace.kind == "Namespace"

    def test_update_namespace(self, namespace):
        """Test updating Namespace"""
        resource_dict = namespace.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        namespace.update(resource_dict=resource_dict)
        assert namespace.labels["updated"] == "true"

    def test_delete_namespace(self, namespace):
        """Test deleting Namespace"""
        namespace.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
