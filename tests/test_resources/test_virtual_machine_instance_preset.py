import pytest

from ocp_resources.virtual_machine_instance_preset import VirtualMachineInstancePreset


@pytest.mark.incremental
class TestVirtualMachineInstancePreset:
    @pytest.fixture(scope="class")
    def virtualmachineinstancepreset(self, fake_client):
        return VirtualMachineInstancePreset(
            client=fake_client,
            name="test-virtualmachineinstancepreset",
            namespace="default",
            selector={"matchLabels": {"app": "test"}},
        )

    def test_01_create_virtualmachineinstancepreset(self, virtualmachineinstancepreset):
        """Test creating VirtualMachineInstancePreset"""
        deployed_resource = virtualmachineinstancepreset.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineinstancepreset"
        assert virtualmachineinstancepreset.exists

    def test_02_get_virtualmachineinstancepreset(self, virtualmachineinstancepreset):
        """Test getting VirtualMachineInstancePreset"""
        assert virtualmachineinstancepreset.instance
        assert virtualmachineinstancepreset.kind == "VirtualMachineInstancePreset"

    def test_03_update_virtualmachineinstancepreset(self, virtualmachineinstancepreset):
        """Test updating VirtualMachineInstancePreset"""
        resource_dict = virtualmachineinstancepreset.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineinstancepreset.update(resource_dict=resource_dict)
        assert virtualmachineinstancepreset.labels["updated"] == "true"

    def test_04_delete_virtualmachineinstancepreset(self, virtualmachineinstancepreset):
        """Test deleting VirtualMachineInstancePreset"""
        virtualmachineinstancepreset.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not virtualmachineinstancepreset.exists
