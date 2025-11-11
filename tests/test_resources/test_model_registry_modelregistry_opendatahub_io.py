import pytest

from ocp_resources.model_registry_modelregistry_opendatahub_io import ModelRegistry


@pytest.mark.incremental
class TestModelRegistry:
    @pytest.fixture(scope="class")
    def modelregistry(self, fake_client):
        return ModelRegistry(
            client=fake_client,
            name="test-modelregistry",
            namespace="default",
            grpc={"test-grpc": "test-value"},
            rest={"test-rest": "test-value"},
        )

    def test_01_create_modelregistry(self, modelregistry):
        """Test creating ModelRegistry"""
        deployed_resource = modelregistry.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-modelregistry"
        assert modelregistry.exists

    def test_02_get_modelregistry(self, modelregistry):
        """Test getting ModelRegistry"""
        assert modelregistry.instance
        assert modelregistry.kind == "ModelRegistry"

    def test_03_update_modelregistry(self, modelregistry):
        """Test updating ModelRegistry"""
        resource_dict = modelregistry.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        modelregistry.update(resource_dict=resource_dict)
        assert modelregistry.labels["updated"] == "true"

    def test_04_delete_modelregistry(self, modelregistry):
        """Test deleting ModelRegistry"""
        modelregistry.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not modelregistry.exists
