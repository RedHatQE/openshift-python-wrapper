import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.machine import Machine


@pytest.mark.incremental
class TestMachine:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def machine(self, client):
        return Machine(
            client=client,
            name="test-machine",
            namespace="default",
        )

    def test_01_create_machine(self, machine):
        """Test creating Machine"""
        deployed_resource = machine.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-machine"
        assert machine.exists

    def test_02_get_machine(self, machine):
        """Test getting Machine"""
        assert machine.instance
        assert machine.kind == "Machine"

    def test_03_update_machine(self, machine):
        """Test updating Machine"""
        resource_dict = machine.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        machine.update(resource_dict=resource_dict)
        assert machine.labels["updated"] == "true"

    def test_04_delete_machine(self, machine):
        """Test deleting Machine"""
        machine.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not machine.exists
