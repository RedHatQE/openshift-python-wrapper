import pytest

from ocp_resources.cdi import CDI


@pytest.mark.incremental
class TestCDI:
    @pytest.fixture(scope="class")
    def cdi(self, fake_client):
        return CDI(
            client=fake_client,
            name="test-cdi",
        )

    def test_01_create_cdi(self, cdi):
        """Test creating CDI"""
        deployed_resource = cdi.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-cdi"
        assert cdi.exists

    def test_02_get_cdi(self, cdi):
        """Test getting CDI"""
        assert cdi.instance
        assert cdi.kind == "CDI"

    def test_03_update_cdi(self, cdi):
        """Test updating CDI"""
        resource_dict = cdi.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        cdi.update(resource_dict=resource_dict)
        assert cdi.labels["updated"] == "true"

    def test_04_delete_cdi(self, cdi):
        """Test deleting CDI"""
        cdi.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not cdi.exists
