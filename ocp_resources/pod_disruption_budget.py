from ocp_resources.resource import NamespacedResource


class PodDisruptionBudget(NamespacedResource):
    """
    PodDisruptionBudget object
    """

    api_group = NamespacedResource.ApiGroup.POLICY

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        min_available=None,
        max_unavailable=None,
        selector=None,
        teardown=True,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.min_available = min_available
        self.max_unavailable = max_unavailable
        self.selector = selector

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        update_dict = {
            "spec": {
                "selector": self.selector,
            },
        }

        if self.min_available is not None:
            update_dict["spec"]["minAvailable"] = self.min_available

        if self.max_unavailable is not None:
            update_dict["spec"]["maxUnavailable"] = self.max_unavailable

        res.update(update_dict)

        return res
