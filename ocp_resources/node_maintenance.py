from ocp_resources.resource import Resource
from ocp_resources.utils.constants import TIMEOUT_4MINUTES


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
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.node = node
        self.reason = reason

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            assert self.node, "node is mandatory for create"
            self.res["spec"] = {"nodeName": self.node.name, "reason": self.reason}
