import pytest

from ocp_resources.virtual_machine_export import VirtualMachineExport


@pytest.mark.incremental
class TestVirtualMachineExport:
    @pytest.fixture(scope="class")
    def virtualmachineexport(self, fake_client):
        return VirtualMachineExport(
            client=fake_client,
            name="test-virtualmachineexport",
            namespace="default",
            source={"test-source": "test-value"},
        )

    def test_01_create_virtualmachineexport(self, virtualmachineexport):
        """Test creating VirtualMachineExport"""
        deployed_resource = virtualmachineexport.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineexport"
        assert virtualmachineexport.exists

    def test_02_get_virtualmachineexport(self, virtualmachineexport):
        """Test getting VirtualMachineExport"""
        assert virtualmachineexport.instance
        assert virtualmachineexport.kind == "VirtualMachineExport"

    def test_03_update_virtualmachineexport(self, virtualmachineexport):
        """Test updating VirtualMachineExport"""
        resource_dict = virtualmachineexport.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineexport.update(resource_dict=resource_dict)
        assert virtualmachineexport.labels["updated"] == "true"

    def test_04_delete_virtualmachineexport(self, virtualmachineexport):
        """Test deleting VirtualMachineExport"""
        virtualmachineexport.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not virtualmachineexport.exists
