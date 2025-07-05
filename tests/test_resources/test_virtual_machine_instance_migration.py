import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.virtual_machine_instance_migration import VirtualMachineInstanceMigration


class TestVirtualMachineInstanceMigration:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def virtualmachineinstancemigration(self, client):
        return VirtualMachineInstanceMigration(
            client=client,
            name="test-virtualmachineinstancemigration",
            namespace="default",
        )

    def test_create_virtualmachineinstancemigration(self, virtualmachineinstancemigration):
        """Test creating VirtualMachineInstanceMigration"""
        deployed_resource = virtualmachineinstancemigration.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineinstancemigration"
        assert virtualmachineinstancemigration.exists

    def test_get_virtualmachineinstancemigration(self, virtualmachineinstancemigration):
        """Test getting VirtualMachineInstanceMigration"""
        assert virtualmachineinstancemigration.instance
        assert virtualmachineinstancemigration.kind == "VirtualMachineInstanceMigration"

    def test_update_virtualmachineinstancemigration(self, virtualmachineinstancemigration):
        """Test updating VirtualMachineInstanceMigration"""
        resource_dict = virtualmachineinstancemigration.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineinstancemigration.update(resource_dict=resource_dict)
        assert virtualmachineinstancemigration.labels["updated"] == "true"

    def test_delete_virtualmachineinstancemigration(self, virtualmachineinstancemigration):
        """Test deleting VirtualMachineInstanceMigration"""
        virtualmachineinstancemigration.clean_up(wait=False)
        # Note: In real clusters, you might want to verify deletion
        # but with fake client, clean_up() removes the resource immediately
