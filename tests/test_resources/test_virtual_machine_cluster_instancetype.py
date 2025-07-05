import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.virtual_machine_cluster_instancetype import VirtualMachineClusterInstancetype


class TestVirtualMachineClusterInstancetype:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def virtualmachineclusterinstancetype(self, client):
        return VirtualMachineClusterInstancetype(
            client=client,
            name="test-virtualmachineclusterinstancetype",
            cpu="test-cpu",
            memory="test-memory",
        )

    def test_create_virtualmachineclusterinstancetype(self, virtualmachineclusterinstancetype):
        """Test creating VirtualMachineClusterInstancetype"""
        deployed_resource = virtualmachineclusterinstancetype.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineclusterinstancetype"
        assert virtualmachineclusterinstancetype.exists

    def test_get_virtualmachineclusterinstancetype(self, virtualmachineclusterinstancetype):
        """Test getting VirtualMachineClusterInstancetype"""
        assert virtualmachineclusterinstancetype.instance
        assert virtualmachineclusterinstancetype.kind == "VirtualMachineClusterInstancetype"

    def test_update_virtualmachineclusterinstancetype(self, virtualmachineclusterinstancetype):
        """Test updating VirtualMachineClusterInstancetype"""
        resource_dict = virtualmachineclusterinstancetype.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineclusterinstancetype.update(resource_dict=resource_dict)
        assert virtualmachineclusterinstancetype.labels["updated"] == "true"

    def test_delete_virtualmachineclusterinstancetype(self, virtualmachineclusterinstancetype):
        """Test deleting VirtualMachineClusterInstancetype"""
        virtualmachineclusterinstancetype.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
