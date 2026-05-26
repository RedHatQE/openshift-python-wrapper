import pytest

from ocp_resources.virtual_machine_cluster_preference import VirtualMachineClusterPreference


@pytest.mark.incremental
class TestVirtualMachineClusterPreference:
    @pytest.fixture(scope="class")
    def virtualmachineclusterpreference(self, fake_client):
        return VirtualMachineClusterPreference(
            client=fake_client,
            name="test-virtualmachineclusterpreference",
        )

    def test_01_create_virtualmachineclusterpreference(self, virtualmachineclusterpreference):
        """Test creating VirtualMachineClusterPreference"""
        deployed_resource = virtualmachineclusterpreference.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineclusterpreference"
        assert virtualmachineclusterpreference.exists

    def test_02_get_virtualmachineclusterpreference(self, virtualmachineclusterpreference):
        """Test getting VirtualMachineClusterPreference"""
        assert virtualmachineclusterpreference.instance
        assert virtualmachineclusterpreference.kind == "VirtualMachineClusterPreference"

    def test_03_update_virtualmachineclusterpreference(self, virtualmachineclusterpreference):
        """Test updating VirtualMachineClusterPreference"""
        resource_dict = virtualmachineclusterpreference.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineclusterpreference.update(resource_dict=resource_dict)
        assert virtualmachineclusterpreference.labels["updated"] == "true"

    def test_04_delete_virtualmachineclusterpreference(self, virtualmachineclusterpreference):
        """Test deleting VirtualMachineClusterPreference"""
        virtualmachineclusterpreference.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not virtualmachineclusterpreference.exists
