import pytest

from ocp_resources.namespace import Namespace


@pytest.mark.incremental
class TestNamespace:
    @pytest.fixture(scope="class")
    def namespace(self, fake_client):
        return Namespace(
            client=fake_client,
            name="test-namespace",
        )

    def test_01_create_namespace(self, namespace):
        """Test creating Namespace"""
        deployed_resource = namespace.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-namespace"
        assert namespace.exists

    def test_02_get_namespace(self, namespace):
        """Test getting Namespace"""
        assert namespace.instance
        assert namespace.kind == "Namespace"

    def test_03_update_namespace(self, namespace):
        """Test updating Namespace"""
        resource_dict = namespace.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        namespace.update(resource_dict=resource_dict)
        assert namespace.labels["updated"] == "true"

    def test_04_delete_namespace(self, namespace):
        """Test deleting Namespace"""
        namespace.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not namespace.exists
