import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.data_import_cron import DataImportCron


class TestDataImportCron:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def dataimportcron(self, client):
        return DataImportCron(
            client=client,
            name="test-dataimportcron",
            namespace="default",
            managed_data_source={"key1": "value1"},
            schedule="test-schedule",
            template={
                "metadata": {"labels": {"app": "test"}},
                "spec": {"containers": [{"name": "test-container", "image": "nginx:latest"}]},
            },
        )

    def test_create_dataimportcron(self, dataimportcron):
        """Test creating DataImportCron"""
        deployed_resource = dataimportcron.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-dataimportcron"
        assert dataimportcron.exists

    def test_get_dataimportcron(self, dataimportcron):
        """Test getting DataImportCron"""
        assert dataimportcron.instance
        assert dataimportcron.kind == "DataImportCron"

    def test_update_dataimportcron(self, dataimportcron):
        """Test updating DataImportCron"""
        resource_dict = dataimportcron.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        dataimportcron.update(resource_dict=resource_dict)
        assert dataimportcron.labels["updated"] == "true"

    def test_delete_dataimportcron(self, dataimportcron):
        """Test deleting DataImportCron"""
        dataimportcron.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not dataimportcron.exists
