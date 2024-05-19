from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import Resource


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
        timeout=TIMEOUT_4MINUTES,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            timeout=timeout,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.node = node
        self.reason = reason

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            assert self.node, "node is mandatory for create"
            self.res["spec"] = {"nodeName": self.node.name, "reason": self.reason}
