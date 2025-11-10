import pytest

from ocp_resources.guardrails_orchestrator import GuardrailsOrchestrator


@pytest.mark.incremental
class TestGuardrailsOrchestrator:
    @pytest.fixture(scope="class")
    def guardrailsorchestrator(self, fake_client):
        return GuardrailsOrchestrator(
            client=fake_client,
            name="test-guardrailsorchestrator",
            namespace="default",
            orchestrator_config="test-orchestrator_config",
            replicas=1,
        )

    def test_01_create_guardrailsorchestrator(self, guardrailsorchestrator):
        """Test creating GuardrailsOrchestrator"""
        deployed_resource = guardrailsorchestrator.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-guardrailsorchestrator"
        assert guardrailsorchestrator.exists

    def test_02_get_guardrailsorchestrator(self, guardrailsorchestrator):
        """Test getting GuardrailsOrchestrator"""
        assert guardrailsorchestrator.instance
        assert guardrailsorchestrator.kind == "GuardrailsOrchestrator"

    def test_03_update_guardrailsorchestrator(self, guardrailsorchestrator):
        """Test updating GuardrailsOrchestrator"""
        resource_dict = guardrailsorchestrator.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        guardrailsorchestrator.update(resource_dict=resource_dict)
        assert guardrailsorchestrator.labels["updated"] == "true"

    def test_04_delete_guardrailsorchestrator(self, guardrailsorchestrator):
        """Test deleting GuardrailsOrchestrator"""
        guardrailsorchestrator.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not guardrailsorchestrator.exists
