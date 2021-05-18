from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class Migration(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) object.

    Args:
        plan_name (str): mtv plan CR name.
        plan_namespace (str): mtv plan CR namespace.

    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    class StatusConditions:
        class CATEGORY:
            REQUIRED = "Required"

        class MESSAGE:
            MIGRATION_READY = "The migration is ready."
            MIGRATION_RUNNING = "The migration is RUNNING"
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

    def to_dict(self):
        res = super().to_dict()
        res.update(
            {
                "spec": {
                    "plan": {"name": self.plan_name, "namespace": self.plan_namespace},
                }
            }
        )
        return res

    def wait_for_condition_succeeded(self):
        self._wait_for_resource_status(
            mtv_resource=self,
            condition_message=self.StatusConditions.MESSAGE.MIGRATION_SUCCEEDED,
            condition_category=self.StatusConditions.CATEGORY.REQUIRED,
            condition_status=self.StatusConditions.STATUS.TRUE,
        )
