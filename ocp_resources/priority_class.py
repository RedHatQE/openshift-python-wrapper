from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import Resource


class PriorityClass(Resource):
    """
    Priority Class object.
    """

    api_group = Resource.ApiGroup.SCHEDULING_K8S_IO

    def __init__(
        self,
        name=None,
        client=None,
        teardown=True,
        value=None,
        global_default=False,
        description=None,
        preemption_policy=None,
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
        self.value = value
        self.global_default = global_default
        self.description = description
        self.preemption_policy = preemption_policy

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        if self.value:
            res["value"] = self.value
        if self.global_default:
            res["globalDefault"] = self.global_default
        if self.description:
            res["description"] = self.description
        if self.preemption_policy:
            res["preemptionPolicy"] = self.preemption_policy
        return res
