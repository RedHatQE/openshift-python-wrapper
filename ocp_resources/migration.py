from ocp_resources.constants import TIMEOUT_4MINUTES
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
        name=None,
        namespace=None,
        plan_name=None,
        plan_namespace=None,
        cut_over=None,
        client=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.plan_name = plan_name
        self.plan_namespace = plan_namespace
        self.cut_over = cut_over
        self.condition_message_succeeded = self.ConditionMessage.MIGRATION_SUCCEEDED

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res.update({
                "spec": {
                    "plan": {
                        "name": self.plan_name,
                        "namespace": self.plan_namespace,
                    }
                }
            })

            if self.cut_over:
                self.res["spec"]["cutover"] = self.cut_over.strftime(format="%Y-%m-%dT%H:%M:%SZ")
