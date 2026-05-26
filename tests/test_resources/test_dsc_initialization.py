import pytest

from ocp_resources.dsc_initialization import DSCInitialization


@pytest.mark.incremental
class TestDSCInitialization:
    @pytest.fixture(scope="class")
    def dscinitialization(self, fake_client):
        return DSCInitialization(
            client=fake_client,
            name="test-dscinitialization",
            applications_namespace="test-applications_namespace",
        )

    def test_01_create_dscinitialization(self, dscinitialization):
        """Test creating DSCInitialization"""
        deployed_resource = dscinitialization.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-dscinitialization"
        assert dscinitialization.exists

    def test_02_get_dscinitialization(self, dscinitialization):
        """Test getting DSCInitialization"""
        assert dscinitialization.instance
        assert dscinitialization.kind == "DSCInitialization"

    def test_03_update_dscinitialization(self, dscinitialization):
        """Test updating DSCInitialization"""
        resource_dict = dscinitialization.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        dscinitialization.update(resource_dict=resource_dict)
        assert dscinitialization.labels["updated"] == "true"

    def test_04_delete_dscinitialization(self, dscinitialization):
        """Test deleting DSCInitialization"""
        dscinitialization.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not dscinitialization.exists
