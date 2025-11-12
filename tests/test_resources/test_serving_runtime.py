import pytest

from ocp_resources.serving_runtime import ServingRuntime


@pytest.mark.incremental
class TestServingRuntime:
    @pytest.fixture(scope="class")
    def servingruntime(self, fake_client):
        return ServingRuntime(
            client=fake_client,
            name="test-servingruntime",
            namespace="default",
            containers=["test-containers"],
        )

    def test_01_create_servingruntime(self, servingruntime):
        """Test creating ServingRuntime"""
        deployed_resource = servingruntime.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-servingruntime"
        assert servingruntime.exists

    def test_02_get_servingruntime(self, servingruntime):
        """Test getting ServingRuntime"""
        assert servingruntime.instance
        assert servingruntime.kind == "ServingRuntime"

    def test_03_update_servingruntime(self, servingruntime):
        """Test updating ServingRuntime"""
        resource_dict = servingruntime.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        servingruntime.update(resource_dict=resource_dict)
        assert servingruntime.labels["updated"] == "true"

    def test_04_delete_servingruntime(self, servingruntime):
        """Test deleting ServingRuntime"""
        servingruntime.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not servingruntime.exists
