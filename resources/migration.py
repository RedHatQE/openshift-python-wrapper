import logging

from .resource import NamespacedResource
from .utils import wait_for_mtv_resource_status


LOGGER = logging.getLogger(__name__)


class Migration(NamespacedResource):
    """
    Migration object.
    https://github.com/konveyor/forklift-controller/blob/main/config/crds/forklift.konveyor.io_migrations.yaml
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    class StatusConditions:
        class CATEGORY:
            REQUIRED = "Required"

        class MESSAGE:
            READY = "The migration is ready."
            MIGRATION_RUNNING = "The migration id RUNNING"
            MIGRATION_SUCCEEDED = "The migration has SUCCEEDED."

        class STATUS:
            TRUE = "True"

        class TYPE:
            READY = "Ready"
            RUNNING = "Running"
            SUCCEEDED = "Succeeded"

    def __init__(self, name, namespace, plan_name, plan_namespace, teardown=True):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.plan_name = plan_name
        self.plan_namespace = plan_namespace

    api_version = f"{NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO}/{NamespacedResource.ApiVersion.V1ALPHA1}"

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "plan": {"name": self.plan_name, "namespace": self.plan_namespace},
                }
            }
        )
        return res

    def wait_for_ready(self, timeout=600):
        wait_for_mtv_resource_status(
            mtv_resource=self,
            timeout=timeout,
            condition_message=self.StatusConditions.MESSAGE.READY,
            condition_status=NamespacedResource.Condition.Status.TRUE,
            condition_type=NamespacedResource.Condition.READY,
        )
