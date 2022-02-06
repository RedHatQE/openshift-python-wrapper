from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class MachineHealthCheck(NamespacedResource):
    """
    MachineHealthCheck object.
    """

    api_group = NamespacedResource.ApiGroup.MACHINE_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        cluster_name=None,
        machineset_name=None,
        client=None,
        machine_role="worker",
        machine_type="worker",
        node_startup_timeout="120m",
        max_unhealthy=2,  # can also be a persentage, for e.g. "40%"
        unhealthy_timeout="300s",
        reboot_strategy=False,
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
        self.cluster_name = cluster_name
        self.machineset_name = machineset_name
        self.machine_role = machine_role
        self.machine_type = machine_type
        self.node_startup_timeout = node_startup_timeout
        self.max_unhealthy = max_unhealthy
        self.unhealthy_timeout = unhealthy_timeout
        self.reboot_strategy = reboot_strategy

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        if self.reboot_strategy:
            res["metadata"]["annotations"] = {
                f"{self.api_group}/remediation-strategy": "external-baremetal"
            }
        res.setdefault("spec", {})
        res["spec"]["nodeStartupTimeout"] = self.node_startup_timeout
        res["spec"]["maxUnhealthy"] = self.max_unhealthy
        res["spec"].setdefault("selector", {})
        res["spec"]["selector"]["matchLabels"] = {
            f"{self.api_group}/cluster-api-cluster": self.cluster_name,
            f"{self.api_group}/cluster-api-machine-role": self.machine_role,
            f"{self.api_group}/cluster-api-machine-type": self.machine_type,
            f"{self.api_group}/cluster-api-machineset": self.machineset_name,
        }
        res["spec"]["unhealthyConditions"] = [
            {
                "type": self.Condition.READY,
                "timeout": self.unhealthy_timeout,
                "status": self.Condition.Status.FALSE,
            },
            {
                "type": self.Condition.READY,
                "timeout": self.unhealthy_timeout,
                "status": self.Condition.Status.UNKNOWN,
            },
        ]
        return res
