import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.virtual_machine_preference import VirtualMachinePreference


class TestVirtualMachinePreference:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def virtualmachinepreference(self, client):
        return VirtualMachinePreference(
            client=client,
            name="test-virtualmachinepreference",
            namespace="default",
        )

    def test_create_virtualmachinepreference(self, virtualmachinepreference):
        """Test creating VirtualMachinePreference"""
        deployed_resource = virtualmachinepreference.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachinepreference"
        assert virtualmachinepreference.exists

    def test_get_virtualmachinepreference(self, virtualmachinepreference):
        """Test getting VirtualMachinePreference"""
        assert virtualmachinepreference.instance
        assert virtualmachinepreference.kind == "VirtualMachinePreference"

    def test_update_virtualmachinepreference(self, virtualmachinepreference):
        """Test updating VirtualMachinePreference"""
        resource_dict = virtualmachinepreference.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachinepreference.update(resource_dict=resource_dict)
        assert virtualmachinepreference.labels["updated"] == "true"

    def test_delete_virtualmachinepreference(self, virtualmachinepreference):
        """Test deleting VirtualMachinePreference"""
        virtualmachinepreference.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
