import pytest

from ocp_resources.lm_eval_job import LMEvalJob


@pytest.mark.incremental
class TestLMEvalJob:
    @pytest.fixture(scope="class")
    def lmevaljob(self, fake_client):
        return LMEvalJob(
            client=fake_client,
            name="test-lmevaljob",
            namespace="default",
            model="test-model",
            task_list={"test-task_list": "test-value"},
        )

    def test_01_create_lmevaljob(self, lmevaljob):
        """Test creating LMEvalJob"""
        deployed_resource = lmevaljob.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-lmevaljob"
        assert lmevaljob.exists

    def test_02_get_lmevaljob(self, lmevaljob):
        """Test getting LMEvalJob"""
        assert lmevaljob.instance
        assert lmevaljob.kind == "LMEvalJob"

    def test_03_update_lmevaljob(self, lmevaljob):
        """Test updating LMEvalJob"""
        resource_dict = lmevaljob.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        lmevaljob.update(resource_dict=resource_dict)
        assert lmevaljob.labels["updated"] == "true"

    def test_04_delete_lmevaljob(self, lmevaljob):
        """Test deleting LMEvalJob"""
        lmevaljob.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not lmevaljob.exists
