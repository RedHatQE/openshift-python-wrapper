from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class Subscription(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        source=None,
        source_namespace=None,
        install_plan_approval=None,
        channel=None,
        starting_csv=None,
        node_selector=None,
        tolerations=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            client=client,
            name=name,
            namespace=namespace,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.source = source
        self.source_namespace = source_namespace
        self.channel = channel
        self.install_plan_approval = install_plan_approval
        self.starting_csv = starting_csv
        self.node_selector = node_selector
        self.tolerations = tolerations

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "sourceNamespace": self.source_namespace,
                        "source": self.source,
                        "name": self.name,
                        "channel": self.channel,
                        "installPlanApproval": self.install_plan_approval,
                        "startingCSV": self.starting_csv,
                    }
                }
            )

            if self.node_selector:
                self.res["spec"].setdefault("config", {}).setdefault(
                    "nodeSelector", {}
                ).update(self.node_selector)

            if self.tolerations:
                self.res["spec"].setdefault("config", {}).setdefault(
                    "tolerations", []
                ).append(self.tolerations)
