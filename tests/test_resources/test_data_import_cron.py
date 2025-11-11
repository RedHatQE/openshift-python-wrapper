import pytest

from ocp_resources.data_import_cron import DataImportCron


@pytest.mark.incremental
class TestDataImportCron:
    @pytest.fixture(scope="class")
    def dataimportcron(self, fake_client):
        return DataImportCron(
            client=fake_client,
            name="test-dataimportcron",
            namespace="default",
            managed_data_source="test-managed-data-source",
            schedule="0 2 * * *",
            template={
                "metadata": {"labels": {"app": "test"}},
                "spec": {
                    "source": {"http": {"url": "http://example.com/disk.qcow2"}},
                    "pvc": {"accessModes": ["ReadWriteOnce"], "resources": {"requests": {"storage": "1Gi"}}},
                },
            },
        )

    def test_01_create_dataimportcron(self, dataimportcron):
        """Test creating DataImportCron"""
        deployed_resource = dataimportcron.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-dataimportcron"
        assert dataimportcron.exists

    def test_02_get_dataimportcron(self, dataimportcron):
        """Test getting DataImportCron"""
        assert dataimportcron.instance
        assert dataimportcron.kind == "DataImportCron"

    def test_03_update_dataimportcron(self, dataimportcron):
        """Test updating DataImportCron"""
        resource_dict = dataimportcron.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        dataimportcron.update(resource_dict=resource_dict)
        assert dataimportcron.labels["updated"] == "true"

    def test_04_delete_dataimportcron(self, dataimportcron):
        """Test deleting DataImportCron"""
        dataimportcron.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not dataimportcron.exists
