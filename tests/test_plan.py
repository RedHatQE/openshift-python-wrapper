from typing import Any

import pytest

from ocp_resources.plan import Plan


@pytest.mark.incremental
class TestPlanConvertorFields:
    @pytest.fixture(scope="class")
    def plan_with_convertor_fields(self, fake_client: Any) -> Plan:
        """Create a Plan with convertor labels and affinity.

        Args:
            fake_client: Fake Kubernetes client for testing.

        Returns:
            Plan instance with convertor_labels and convertor_affinity set.
        """
        return Plan(
            client=fake_client,
            name="test-plan-convertor-fields",
            namespace="default",
            source_provider_name="source-provider",
            source_provider_namespace="default",
            destination_provider_name="destination-provider",
            destination_provider_namespace="default",
            storage_map_name="storage-map",
            storage_map_namespace="default",
            network_map_name="network-map",
            network_map_namespace="default",
            virtual_machines_list=[{"id": "vm-id-x"}],
            convertor_labels={"key": "value"},
            convertor_affinity={
                "nodeAffinity": {
                    "requiredDuringSchedulingIgnoredDuringExecution": {
                        "nodeSelectorTerms": [{"matchExpressions": [{"key": "k", "operator": "Exists"}]}]
                    }
                }
            },
        )

    @pytest.fixture(scope="class")
    def plan_without_convertor_fields(self, fake_client: Any) -> Plan:
        """Create a Plan without convertor labels and affinity.

        Args:
            fake_client: Fake Kubernetes client for testing.

        Returns:
            Plan instance without convertor_labels or convertor_affinity.
        """
        return Plan(
            client=fake_client,
            name="test-plan-no-convertor-fields",
            namespace="default",
            source_provider_name="source-provider",
            source_provider_namespace="default",
            destination_provider_name="destination-provider",
            destination_provider_namespace="default",
            storage_map_name="storage-map",
            storage_map_namespace="default",
            network_map_name="network-map",
            network_map_namespace="default",
            virtual_machines_list=[{"id": "vm-id-x"}],
        )

    def test_01_create_plan_with_convertor_fields(self, plan_with_convertor_fields: Plan) -> None:
        """Test creating a Plan with convertor labels and affinity.

        Args:
            plan_with_convertor_fields: Plan with convertor fields set.
        """
        deployed_resource = plan_with_convertor_fields.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-plan-convertor-fields"
        assert plan_with_convertor_fields.exists

    def test_02_convertor_fields_in_dict(self, plan_with_convertor_fields: Plan) -> None:
        """Test convertorLabels and convertorAffinity are emitted in to_dict.

        Args:
            plan_with_convertor_fields: Plan with convertor fields set.
        """
        plan_with_convertor_fields.to_dict()
        spec = plan_with_convertor_fields.res["spec"]
        assert spec["convertorLabels"] == {"key": "value"}
        assert spec["convertorAffinity"] == {
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [{"matchExpressions": [{"key": "k", "operator": "Exists"}]}]
                }
            }
        }

    def test_03_create_plan_without_convertor_fields(self, plan_without_convertor_fields: Plan) -> None:
        """Test creating a Plan without convertor labels and affinity.

        Args:
            plan_without_convertor_fields: Plan without convertor fields.
        """
        deployed_resource = plan_without_convertor_fields.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-plan-no-convertor-fields"
        assert plan_without_convertor_fields.exists

    def test_04_convertor_fields_absent_when_not_set(self, plan_without_convertor_fields: Plan) -> None:
        """Test convertorLabels and convertorAffinity are absent when not passed.

        Args:
            plan_without_convertor_fields: Plan without convertor fields.
        """
        plan_without_convertor_fields.to_dict()
        spec = plan_without_convertor_fields.res["spec"]
        assert "convertorLabels" not in spec
        assert "convertorAffinity" not in spec

    def test_05_delete_plans(
        self,
        plan_with_convertor_fields: Plan,
        plan_without_convertor_fields: Plan,
    ) -> None:
        """Test deleting Plans.

        Args:
            plan_with_convertor_fields: Plan with convertor fields set.
            plan_without_convertor_fields: Plan without convertor fields.
        """
        plan_with_convertor_fields.clean_up(wait=False)
        assert not plan_with_convertor_fields.exists
        plan_without_convertor_fields.clean_up(wait=False)
        assert not plan_without_convertor_fields.exists
