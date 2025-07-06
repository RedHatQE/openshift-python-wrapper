import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.image_content_source_policy import ImageContentSourcePolicy


@pytest.mark.incremental
class TestImageContentSourcePolicy:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def imagecontentsourcepolicy(self, client):
        return ImageContentSourcePolicy(
            client=client,
            name="test-imagecontentsourcepolicy",
        )

    def test_01_create_imagecontentsourcepolicy(self, imagecontentsourcepolicy):
        """Test creating ImageContentSourcePolicy"""
        deployed_resource = imagecontentsourcepolicy.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-imagecontentsourcepolicy"
        assert imagecontentsourcepolicy.exists

    def test_02_get_imagecontentsourcepolicy(self, imagecontentsourcepolicy):
        """Test getting ImageContentSourcePolicy"""
        assert imagecontentsourcepolicy.instance
        assert imagecontentsourcepolicy.kind == "ImageContentSourcePolicy"

    def test_03_update_imagecontentsourcepolicy(self, imagecontentsourcepolicy):
        """Test updating ImageContentSourcePolicy"""
        resource_dict = imagecontentsourcepolicy.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        imagecontentsourcepolicy.update(resource_dict=resource_dict)
        assert imagecontentsourcepolicy.labels["updated"] == "true"

    def test_04_delete_imagecontentsourcepolicy(self, imagecontentsourcepolicy):
        """Test deleting ImageContentSourcePolicy"""
        imagecontentsourcepolicy.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not imagecontentsourcepolicy.exists
