import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.self_subject_review import SelfSubjectReview


class TestSelfSubjectReview:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def selfsubjectreview(self, client):
        return SelfSubjectReview(
            client=client,
            name="test-selfsubjectreview",
        )

    def test_create_selfsubjectreview(self, selfsubjectreview):
        """Test creating SelfSubjectReview"""
        deployed_resource = selfsubjectreview.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-selfsubjectreview"
        assert selfsubjectreview.exists

    def test_get_selfsubjectreview(self, selfsubjectreview):
        """Test getting SelfSubjectReview"""
        assert selfsubjectreview.instance
        assert selfsubjectreview.kind == "SelfSubjectReview"

    def test_update_selfsubjectreview(self, selfsubjectreview):
        """Test updating SelfSubjectReview"""
        resource_dict = selfsubjectreview.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        selfsubjectreview.update(resource_dict=resource_dict)
        assert selfsubjectreview.labels["updated"] == "true"

    def test_delete_selfsubjectreview(self, selfsubjectreview):
        """Test deleting SelfSubjectReview"""
        selfsubjectreview.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not selfsubjectreview.exists
