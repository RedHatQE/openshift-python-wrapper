from ocp_resources.resource import TIMEOUT, Resource


class NodeMaintenance(Resource):
    """
    Node Maintenance object, inherited from Resource.
    """

    api_group = Resource.ApiGroup.NODEMAINTENANCE_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        client=None,
        node=None,
        reason="TEST Reason",
        teardown=True,
        timeout=TIMEOUT,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            timeout=timeout,
            yaml_file=yaml_file,
        )
        self.node = node
        self.reason = reason

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        assert self.node, "node is mandatory for create"
        res["spec"] = {"nodeName": self.node.name, "reason": self.reason}
        return res
