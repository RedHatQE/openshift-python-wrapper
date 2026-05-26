import pytest

from ocp_resources.virtual_machine_cluster_instancetype import VirtualMachineClusterInstancetype


@pytest.mark.incremental
class TestVirtualMachineClusterInstancetype:
    @pytest.fixture(scope="class")
    def virtualmachineclusterinstancetype(self, fake_client):
        return VirtualMachineClusterInstancetype(
            client=fake_client,
            name="test-virtualmachineclusterinstancetype",
            cpu={"test-cpu": "test-value"},
            memory={"test-memory": "test-value"},
        )

    def test_01_create_virtualmachineclusterinstancetype(self, virtualmachineclusterinstancetype):
        """Test creating VirtualMachineClusterInstancetype"""
        deployed_resource = virtualmachineclusterinstancetype.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineclusterinstancetype"
        assert virtualmachineclusterinstancetype.exists

    def test_02_get_virtualmachineclusterinstancetype(self, virtualmachineclusterinstancetype):
        """Test getting VirtualMachineClusterInstancetype"""
        assert virtualmachineclusterinstancetype.instance
        assert virtualmachineclusterinstancetype.kind == "VirtualMachineClusterInstancetype"

    def test_03_update_virtualmachineclusterinstancetype(self, virtualmachineclusterinstancetype):
        """Test updating VirtualMachineClusterInstancetype"""
        resource_dict = virtualmachineclusterinstancetype.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineclusterinstancetype.update(resource_dict=resource_dict)
        assert virtualmachineclusterinstancetype.labels["updated"] == "true"

    def test_04_delete_virtualmachineclusterinstancetype(self, virtualmachineclusterinstancetype):
        """Test deleting VirtualMachineClusterInstancetype"""
        virtualmachineclusterinstancetype.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not virtualmachineclusterinstancetype.exists
