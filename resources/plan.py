import logging

from .resource import NamespacedResource
from .utils import wait_for_mtv_resource_status


LOGGER = logging.getLogger(__name__)


class Plan(NamespacedResource):
    """
    Plan Resource
    https://github.com/konveyor/forklift-controller/blob/master/config/crds/forklift_v1alpha1_plan.yaml
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    class StatusCondition:
        class Message:
            READY = "The migration plan is ready."
            SUCCEEDED = "The plan execution has SUCCEEDED."

        class Type:
            SUCCEEDED = "Succeeded"

    def __init__(
        self,
        name,
        namespace,
        destination_provider_name,
        destination_provider_namespace,
        source_provider_name,
        source_provider_namespace,
        migration_map,
        vms,
        target_namespace=None,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace
        self.migration_map = migration_map
        self.vms = vms
        self.target_namespace = target_namespace

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "map": self.migration_map,
                    "vms": self.vms,
                    "targetNamespace": self.target_namespace,
                    "provider": {
                        "source": {
                            "name": self.source_provider_name,
                            "namespace": self.source_provider_namespace,
                        },
                        "destination": {
                            "name": self.destination_provider_name,
                            "namespace": self.destination_provider_namespace,
                        },
                    },
                }
            }
        )
        return res

    def wait_for_ready(self, timeout=600):
        wait_for_mtv_resource_status(
            mtv_resource=self,
            timeout=timeout,
            condition_message=self.StatusCondition.Message.READY,
            condition_status=NamespacedResource.Condition.Status.TRUE,
            condition_type=NamespacedResource.Condition.READY,
        )

    def wait_for_succeeded(self, timeout=600):
        wait_for_mtv_resource_status(
            mtv_resource=self,
            timeout=timeout,
            condition_message=self.StatusCondition.Message.SUCCEEDED,
            condition_status=NamespacedResource.Condition.Status.TRUE,
            condition_type=self.StatusCondition.Type.SUCCEEDED,
        )
