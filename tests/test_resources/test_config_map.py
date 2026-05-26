import pytest

from ocp_resources.config_map import ConfigMap


@pytest.mark.incremental
class TestConfigMap:
    @pytest.fixture(scope="class")
    def configmap(self, fake_client):
        return ConfigMap(
            client=fake_client,
            name="test-configmap",
            namespace="default",
            data={"key1": "value1"},
        )

    def test_01_create_configmap(self, configmap):
        """Test creating ConfigMap"""
        deployed_resource = configmap.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-configmap"
        assert configmap.exists

    def test_02_get_configmap(self, configmap):
        """Test getting ConfigMap"""
        assert configmap.instance
        assert configmap.kind == "ConfigMap"

    def test_03_update_configmap(self, configmap):
        """Test updating ConfigMap"""
        resource_dict = configmap.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        configmap.update(resource_dict=resource_dict)
        assert configmap.labels["updated"] == "true"

    def test_04_delete_configmap(self, configmap):
        """Test deleting ConfigMap"""
        configmap.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not configmap.exists
