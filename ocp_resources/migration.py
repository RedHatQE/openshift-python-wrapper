from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class Migration(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) Migration object.

    Args:
        plan_name (str): MTV Plan CR name.
        plan_namespace (str): MTV Plan CR namespace.
        cut_over (date): For Warm Migration Only.Cut Over Phase Start Date & Time.

    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name,
        namespace,
        plan_name=None,
        plan_namespace=None,
        cut_over=None,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.plan_name = plan_name
        self.plan_namespace = plan_namespace
        self.cut_over = cut_over
        self.condition_message_succeeded = self.ConditionMessage.MIGRATION_SUCCEEDED

    def to_dict(self):
        res = super().to_dict()
        res.update(
            {
                "spec": {
                    "plan": {"name": self.plan_name, "namespace": self.plan_namespace}
                }
            }
        )

        if self.cut_over:
            res["spec"]["plan"]["cutover"] = self.cut_over.strftime(
                format="%Y-%m-%dT%H:%M:%SZ"
            )

        return res
