from .resource import NamespacedResource, Resource


class Node(Resource):
    """
    Node object, inherited from Resource.
    """

    api_version = "v1"

    class Status(NamespacedResource.Status):
        READY = "Ready"
        SCHEDULING_DISABLED = "Ready,SchedulingDisabled"

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
