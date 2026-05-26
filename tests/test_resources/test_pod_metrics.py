import pytest

from ocp_resources.pod_metrics import PodMetrics


@pytest.mark.incremental
class TestPodMetrics:
    @pytest.fixture(scope="class")
    def podmetrics(self, fake_client):
        return PodMetrics(
            client=fake_client,
            name="test-podmetrics",
            namespace="default",
            containers=["test-containers"],
            timestamp="test-timestamp",
            window="test-window",
        )

    def test_01_create_podmetrics(self, podmetrics):
        """Test creating PodMetrics"""
        deployed_resource = podmetrics.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-podmetrics"
        assert podmetrics.exists

    def test_02_get_podmetrics(self, podmetrics):
        """Test getting PodMetrics"""
        assert podmetrics.instance
        assert podmetrics.kind == "PodMetrics"

    def test_03_update_podmetrics(self, podmetrics):
        """Test updating PodMetrics"""
        resource_dict = podmetrics.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        podmetrics.update(resource_dict=resource_dict)
        assert podmetrics.labels["updated"] == "true"

    def test_04_delete_podmetrics(self, podmetrics):
        """Test deleting PodMetrics"""
        podmetrics.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not podmetrics.exists
