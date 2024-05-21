from ocp_resources.constants import TIMEOUT_4MINUTES
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
        self.min_available = min_available
        self.max_unavailable = max_unavailable
        self.selector = selector

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            update_dict = {
                "spec": {
                    "selector": self.selector,
                },
            }

            if self.min_available is not None:
                update_dict["spec"]["minAvailable"] = self.min_available

            if self.max_unavailable is not None:
                update_dict["spec"]["maxUnavailable"] = self.max_unavailable

            self.res.update(update_dict)
