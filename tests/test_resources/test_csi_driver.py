import pytest

from ocp_resources.csi_driver import CSIDriver


@pytest.mark.incremental
class TestCSIDriver:
    @pytest.fixture(scope="class")
    def csidriver(self, fake_client):
        return CSIDriver(
            client=fake_client,
            name="test-csidriver",
        )

    def test_01_create_csidriver(self, csidriver):
        """Test creating CSIDriver"""
        deployed_resource = csidriver.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-csidriver"
        assert csidriver.exists

    def test_02_get_csidriver(self, csidriver):
        """Test getting CSIDriver"""
        assert csidriver.instance
        assert csidriver.kind == "CSIDriver"

    def test_03_update_csidriver(self, csidriver):
        """Test updating CSIDriver"""
        resource_dict = csidriver.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        csidriver.update(resource_dict=resource_dict)
        assert csidriver.labels["updated"] == "true"

    def test_04_delete_csidriver(self, csidriver):
        """Test deleting CSIDriver"""
        csidriver.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not csidriver.exists
