import pytest

from ocp_resources.cdi_config import CDIConfig


@pytest.mark.incremental
class TestCDIConfig:
    @pytest.fixture(scope="class")
    def cdiconfig(self, fake_client):
        return CDIConfig(
            client=fake_client,
            name="test-cdiconfig",
        )

    def test_01_create_cdiconfig(self, cdiconfig):
        """Test creating CDIConfig"""
        deployed_resource = cdiconfig.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-cdiconfig"
        assert cdiconfig.exists

    def test_02_get_cdiconfig(self, cdiconfig):
        """Test getting CDIConfig"""
        assert cdiconfig.instance
        assert cdiconfig.kind == "CDIConfig"

    def test_03_update_cdiconfig(self, cdiconfig):
        """Test updating CDIConfig"""
        resource_dict = cdiconfig.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        cdiconfig.update(resource_dict=resource_dict)
        assert cdiconfig.labels["updated"] == "true"

    def test_04_delete_cdiconfig(self, cdiconfig):
        """Test deleting CDIConfig"""
        cdiconfig.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not cdiconfig.exists
