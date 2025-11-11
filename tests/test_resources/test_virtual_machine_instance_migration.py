import pytest

from ocp_resources.virtual_machine_instance_migration import VirtualMachineInstanceMigration


@pytest.mark.incremental
class TestVirtualMachineInstanceMigration:
    @pytest.fixture(scope="class")
    def virtualmachineinstancemigration(self, fake_client):
        return VirtualMachineInstanceMigration(
            client=fake_client,
            name="test-virtualmachineinstancemigration",
            namespace="default",
        )

    def test_01_create_virtualmachineinstancemigration(self, virtualmachineinstancemigration):
        """Test creating VirtualMachineInstanceMigration"""
        deployed_resource = virtualmachineinstancemigration.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineinstancemigration"
        assert virtualmachineinstancemigration.exists

    def test_02_get_virtualmachineinstancemigration(self, virtualmachineinstancemigration):
        """Test getting VirtualMachineInstanceMigration"""
        assert virtualmachineinstancemigration.instance
        assert virtualmachineinstancemigration.kind == "VirtualMachineInstanceMigration"

    def test_03_update_virtualmachineinstancemigration(self, virtualmachineinstancemigration):
        """Test updating VirtualMachineInstanceMigration"""
        resource_dict = virtualmachineinstancemigration.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineinstancemigration.update(resource_dict=resource_dict)
        assert virtualmachineinstancemigration.labels["updated"] == "true"

    def test_04_delete_virtualmachineinstancemigration(self, virtualmachineinstancemigration):
        """Test deleting VirtualMachineInstanceMigration"""
        virtualmachineinstancemigration.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not virtualmachineinstancemigration.exists
