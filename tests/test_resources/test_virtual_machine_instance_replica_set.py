import pytest

from ocp_resources.virtual_machine_instance_replica_set import VirtualMachineInstanceReplicaSet


@pytest.mark.incremental
class TestVirtualMachineInstanceReplicaSet:
    @pytest.fixture(scope="class")
    def virtualmachineinstancereplicaset(self, fake_client):
        return VirtualMachineInstanceReplicaSet(
            client=fake_client,
            name="test-virtualmachineinstancereplicaset",
            namespace="default",
            selector={"matchLabels": {"app": "test"}},
            template={
                "metadata": {"labels": {"app": "test"}},
                "spec": {"containers": [{"name": "test-container", "image": "nginx:latest"}]},
            },
        )

    def test_01_create_virtualmachineinstancereplicaset(self, virtualmachineinstancereplicaset):
        """Test creating VirtualMachineInstanceReplicaSet"""
        deployed_resource = virtualmachineinstancereplicaset.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-virtualmachineinstancereplicaset"
        assert virtualmachineinstancereplicaset.exists

    def test_02_get_virtualmachineinstancereplicaset(self, virtualmachineinstancereplicaset):
        """Test getting VirtualMachineInstanceReplicaSet"""
        assert virtualmachineinstancereplicaset.instance
        assert virtualmachineinstancereplicaset.kind == "VirtualMachineInstanceReplicaSet"

    def test_03_update_virtualmachineinstancereplicaset(self, virtualmachineinstancereplicaset):
        """Test updating VirtualMachineInstanceReplicaSet"""
        resource_dict = virtualmachineinstancereplicaset.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        virtualmachineinstancereplicaset.update(resource_dict=resource_dict)
        assert virtualmachineinstancereplicaset.labels["updated"] == "true"

    def test_04_delete_virtualmachineinstancereplicaset(self, virtualmachineinstancereplicaset):
        """Test deleting VirtualMachineInstanceReplicaSet"""
        virtualmachineinstancereplicaset.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not virtualmachineinstancereplicaset.exists
