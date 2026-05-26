import pytest

from ocp_resources.virtual_machine_preference import VirtualMachinePreference


@pytest.mark.incremental
class TestVirtualMachinePreference:
    @pytest.fixture(scope="class")
    def virtualmachinepreference(self, fake_client):
        return VirtualMachinePreference(
            client=fake_client,
            name="test-virtualmachinepreference",
            namespace="default",
        )

    def test_01_create_virtualmachinepreference(self, virtualmachinepreference):
        """Test creating VirtualMachinePreference"""
        deployed_resource = virtualmachinepreference.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachinepreference"
        assert virtualmachinepreference.exists

    def test_02_get_virtualmachinepreference(self, virtualmachinepreference):
        """Test getting VirtualMachinePreference"""
        assert virtualmachinepreference.instance
        assert virtualmachinepreference.kind == "VirtualMachinePreference"

    def test_03_update_virtualmachinepreference(self, virtualmachinepreference):
        """Test updating VirtualMachinePreference"""
        resource_dict = virtualmachinepreference.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachinepreference.update(resource_dict=resource_dict)
        assert virtualmachinepreference.labels["updated"] == "true"

    def test_04_delete_virtualmachinepreference(self, virtualmachinepreference):
        """Test deleting VirtualMachinePreference"""
        virtualmachinepreference.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not virtualmachinepreference.exists
