from ocp_resources.resource import TIMEOUT, Resource


class NodeMaintenance(Resource):
    """
    Node Maintenance object, inherited from Resource.
    """

    api_group = Resource.ApiGroup.NODEMAINTENANCE_KUBEVIRT_IO

    class Status(Resource.Status):
        RUNNING = "Running"

    def __init__(
        self,
        name,
        client=None,
        node=None,
        reason="TEST Reason",
        teardown=True,
        timeout=TIMEOUT,
    ):
        super().__init__(name=name, client=client, teardown=teardown, timeout=timeout)
        self.node = node
        self.reason = reason

    def to_dict(self):
        assert self.node, "node is mandatory for create"
        res = super().to_dict()
        res["spec"] = {"nodeName": self.node.name, "reason": self.reason}
        return res
