from resources.resource import NamespacedResource


class Subscription(NamespacedResource):
    api_group = "operators.coreos.com"

    def __init__(
        self,
        name,
        namespace,
        source,
        source_namespace,
        install_plan_approval,
        channel,
        starting_csv,
        teardown=False,
    ):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.source = source
        self.source_namespace = source_namespace
        self.channel = channel
        self.install_plan_approval = install_plan_approval
        self.starting_csv = starting_csv

    def to_dict(self):
        res = super()._base_body()
        res.update(
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

        return res
