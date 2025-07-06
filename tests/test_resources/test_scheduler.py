import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.scheduler import Scheduler


@pytest.mark.incremental
class TestScheduler:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def scheduler(self, client):
        return Scheduler(
            client=client,
            name="test-scheduler",
        )

    def test_01_create_scheduler(self, scheduler):
        """Test creating Scheduler"""
        deployed_resource = scheduler.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-scheduler"
        assert scheduler.exists

    def test_02_get_scheduler(self, scheduler):
        """Test getting Scheduler"""
        assert scheduler.instance
        assert scheduler.kind == "Scheduler"

    def test_03_update_scheduler(self, scheduler):
        """Test updating Scheduler"""
        resource_dict = scheduler.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        scheduler.update(resource_dict=resource_dict)
        assert scheduler.labels["updated"] == "true"

    def test_04_delete_scheduler(self, scheduler):
        """Test deleting Scheduler"""
        scheduler.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not scheduler.exists
