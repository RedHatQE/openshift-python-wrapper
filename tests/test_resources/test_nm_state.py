import pytest

from ocp_resources.nm_state import NMState


@pytest.mark.incremental
class TestNMState:
    @pytest.fixture(scope="class")
    def nmstate(self, fake_client):
        return NMState(
            client=fake_client,
            name="test-nmstate",
        )

    def test_01_create_nmstate(self, nmstate):
        """Test creating NMState"""
        deployed_resource = nmstate.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-nmstate"
        assert nmstate.exists

    def test_02_get_nmstate(self, nmstate):
        """Test getting NMState"""
        assert nmstate.instance
        assert nmstate.kind == "NMState"

    def test_03_update_nmstate(self, nmstate):
        """Test updating NMState"""
        resource_dict = nmstate.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        nmstate.update(resource_dict=resource_dict)
        assert nmstate.labels["updated"] == "true"

    def test_04_delete_nmstate(self, nmstate):
        """Test deleting NMState"""
        nmstate.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not nmstate.exists
