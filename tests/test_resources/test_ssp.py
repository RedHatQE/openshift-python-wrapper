import pytest

from ocp_resources.ssp import SSP


@pytest.mark.incremental
class TestSSP:
    @pytest.fixture(scope="class")
    def ssp(self, fake_client):
        return SSP(
            client=fake_client,
            name="test-ssp",
            namespace="default",
            common_templates={"test-common_templates": "test-value"},
        )

    def test_01_create_ssp(self, ssp):
        """Test creating SSP"""
        deployed_resource = ssp.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-ssp"
        assert ssp.exists

    def test_02_get_ssp(self, ssp):
        """Test getting SSP"""
        assert ssp.instance
        assert ssp.kind == "SSP"

    def test_03_update_ssp(self, ssp):
        """Test updating SSP"""
        resource_dict = ssp.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        ssp.update(resource_dict=resource_dict)
        assert ssp.labels["updated"] == "true"

    def test_04_delete_ssp(self, ssp):
        """Test deleting SSP"""
        ssp.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not ssp.exists
