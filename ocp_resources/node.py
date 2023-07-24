from ocp_resources.resource import Resource


class Node(Resource):
    """
    Node object, inherited from Resource.
    """

    api_version = Resource.ApiVersion.V1

    class Status(Resource.Status):
        READY = "Ready"
        SCHEDULING_DISABLED = "Ready,SchedulingDisabled"

    @property
    def kubelet_ready(self):
        return any(
            stat
            for stat in self.instance.status.conditions
            if stat["reason"] == "KubeletReady"
            and stat["status"] == self.Condition.Status.TRUE
        )

    @property
    def machine_name(self):
        return self.instance.metadata.annotations[
            f"{self.ApiGroup.MACHINE_OPENSHIFT_IO}/machine"
        ].split("/")[-1]

    @property
    def internal_ip(self):
        for addr in self.instance.status.addresses:
            if addr.type == "InternalIP":
                return addr.address

    @property
    def hostname(self):
        return self.labels["kubernetes.io/hostname"]

    @property
    def taints(self):
        return self.instance.get("spec", {}).get("taints")
