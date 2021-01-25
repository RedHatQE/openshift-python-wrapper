from resources.resource import NamespacedResource, Resource


class Node(Resource):
    """
    Node object, inherited from Resource.
    """

    api_version = Resource.ApiVersion.V1

    class Status(NamespacedResource.Status):
        READY = "Ready"
        SCHEDULING_DISABLED = "Ready,SchedulingDisabled"

    def __init__(
        self,
        name,
        client=None,
        teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)

    @property
    def kubelet_ready(self):
        return any(
            [
                stat
                for stat in self.instance.status.conditions
                if stat["reason"] == "KubeletReady"
                and stat["status"] == self.Condition.Status.TRUE
            ]
        )

    @property
    def machine_name(self):
        return self.instance.metadata.annotations[
            f"{self.ApiGroup.MACHINE_OPENSHIFT_IO}/machine"
        ].split("/")[-1]
