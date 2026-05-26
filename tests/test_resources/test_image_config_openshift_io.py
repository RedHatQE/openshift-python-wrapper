import pytest

from ocp_resources.image_config_openshift_io import Image


@pytest.mark.incremental
class TestImage:
    @pytest.fixture(scope="class")
    def image(self, fake_client):
        return Image(
            client=fake_client,
            name="test-image",
        )

    def test_01_create_image(self, image):
        """Test creating Image"""
        deployed_resource = image.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-image"
        assert image.exists

    def test_02_get_image(self, image):
        """Test getting Image"""
        assert image.instance
        assert image.kind == "Image"

    def test_03_update_image(self, image):
        """Test updating Image"""
        resource_dict = image.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        image.update(resource_dict=resource_dict)
        assert image.labels["updated"] == "true"

    def test_04_delete_image(self, image):
        """Test deleting Image"""
        image.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not image.exists
