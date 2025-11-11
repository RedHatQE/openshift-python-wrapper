import pytest

from ocp_resources.inference_graph import InferenceGraph


@pytest.mark.incremental
class TestInferenceGraph:
    @pytest.fixture(scope="class")
    def inferencegraph(self, fake_client):
        return InferenceGraph(
            client=fake_client,
            name="test-inferencegraph",
            namespace="default",
            nodes={"test-nodes": "test-value"},
        )

    def test_01_create_inferencegraph(self, inferencegraph):
        """Test creating InferenceGraph"""
        deployed_resource = inferencegraph.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-inferencegraph"
        assert inferencegraph.exists

    def test_02_get_inferencegraph(self, inferencegraph):
        """Test getting InferenceGraph"""
        assert inferencegraph.instance
        assert inferencegraph.kind == "InferenceGraph"

    def test_03_update_inferencegraph(self, inferencegraph):
        """Test updating InferenceGraph"""
        resource_dict = inferencegraph.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        inferencegraph.update(resource_dict=resource_dict)
        assert inferencegraph.labels["updated"] == "true"

    def test_04_delete_inferencegraph(self, inferencegraph):
        """Test deleting InferenceGraph"""
        inferencegraph.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not inferencegraph.exists
