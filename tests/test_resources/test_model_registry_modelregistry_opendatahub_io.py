import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.model_registry_modelregistry_opendatahub_io import ModelRegistry


class TestModelRegistry:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def modelregistry(self, client):
        return ModelRegistry(
            client=client,
            name="test-modelregistry",
            namespace="default",
            grpc="test-grpc",
            rest="test-rest",
        )

    def test_create_modelregistry(self, modelregistry):
        """Test creating ModelRegistry"""
        deployed_resource = modelregistry.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-modelregistry"
        assert modelregistry.exists

    def test_get_modelregistry(self, modelregistry):
        """Test getting ModelRegistry"""
        assert modelregistry.instance
        assert modelregistry.kind == "ModelRegistry"

    def test_update_modelregistry(self, modelregistry):
        """Test updating ModelRegistry"""
        resource_dict = modelregistry.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        modelregistry.update(resource_dict=resource_dict)
        assert modelregistry.labels["updated"] == "true"

    def test_delete_modelregistry(self, modelregistry):
        """Test deleting ModelRegistry"""
        modelregistry.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
