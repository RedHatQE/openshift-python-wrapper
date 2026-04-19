import pytest

from ocp_resources.data_protection_application import DataProtectionApplication


@pytest.mark.incremental
class TestDataProtectionApplication:
    @pytest.fixture(scope="class")
    def dataprotectionapplication(self, fake_client):
        return DataProtectionApplication(
            client=fake_client,
            name="test-dataprotectionapplication",
            namespace="default",
            configuration={"test-configuration": "test-value"},
        )

    def test_01_create_dataprotectionapplication(self, dataprotectionapplication):
        """Test creating DataProtectionApplication"""
        deployed_resource = dataprotectionapplication.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-dataprotectionapplication"
        assert dataprotectionapplication.exists

    def test_02_get_dataprotectionapplication(self, dataprotectionapplication):
        """Test getting DataProtectionApplication"""
        assert dataprotectionapplication.instance
        assert dataprotectionapplication.kind == "DataProtectionApplication"

    def test_03_update_dataprotectionapplication(self, dataprotectionapplication):
        """Test updating DataProtectionApplication"""
        resource_dict = dataprotectionapplication.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        dataprotectionapplication.update(resource_dict=resource_dict)
        assert dataprotectionapplication.labels["updated"] == "true"

    def test_04_delete_dataprotectionapplication(self, dataprotectionapplication):
        """Test deleting DataProtectionApplication"""
        dataprotectionapplication.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not dataprotectionapplication.exists
