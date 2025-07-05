import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.virtual_machine_instancetype import VirtualMachineInstancetype


class TestVirtualMachineInstancetype:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def virtualmachineinstancetype(self, client):
        return VirtualMachineInstancetype(
            client=client,
            name="test-virtualmachineinstancetype",
            namespace="default",
            cpu="test-cpu",
            memory="test-memory",
        )

    def test_create_virtualmachineinstancetype(self, virtualmachineinstancetype):
        """Test creating VirtualMachineInstancetype"""
        deployed_resource = virtualmachineinstancetype.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineinstancetype"
        assert virtualmachineinstancetype.exists

    def test_get_virtualmachineinstancetype(self, virtualmachineinstancetype):
        """Test getting VirtualMachineInstancetype"""
        assert virtualmachineinstancetype.instance
        assert virtualmachineinstancetype.kind == "VirtualMachineInstancetype"

    def test_update_virtualmachineinstancetype(self, virtualmachineinstancetype):
        """Test updating VirtualMachineInstancetype"""
        resource_dict = virtualmachineinstancetype.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineinstancetype.update(resource_dict=resource_dict)
        assert virtualmachineinstancetype.labels["updated"] == "true"

    def test_delete_virtualmachineinstancetype(self, virtualmachineinstancetype):
        """Test deleting VirtualMachineInstancetype"""
        virtualmachineinstancetype.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
