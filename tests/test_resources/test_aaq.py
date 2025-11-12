import pytest

from ocp_resources.aaq import AAQ


@pytest.mark.incremental
class TestAAQ:
    @pytest.fixture(scope="class")
    def aaq(self, fake_client):
        return AAQ(
            client=fake_client,
            name="test-aaq",
        )

    def test_01_create_aaq(self, aaq):
        """Test creating AAQ"""
        deployed_resource = aaq.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-aaq"
        assert aaq.exists

    def test_02_get_aaq(self, aaq):
        """Test getting AAQ"""
        assert aaq.instance
        assert aaq.kind == "AAQ"

    def test_03_update_aaq(self, aaq):
        """Test updating AAQ"""
        resource_dict = aaq.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        aaq.update(resource_dict=resource_dict)
        assert aaq.labels["updated"] == "true"

    def test_04_delete_aaq(self, aaq):
        """Test deleting AAQ"""
        aaq.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not aaq.exists
