from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class PodMetrics(NamespacedResource):
    """
    PodMetrics object. API reference:
    https://docs.openshift.com/container-platform/4.12/nodes/pods/nodes-pods-autoscaling.html
    """

    api_group = NamespacedResource.ApiGroup.METRICS_K8S_IO
    api_version = NamespacedResource.ApiVersion.V1BETA1

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        containers=None,
        timestamp=None,
        window=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the endpoints resource
            namespace (str): Namespace of endpoints resource
            client: (DynamicClient): DynamicClient for api calls
            containers (list): list of containers
            timestamp (str): timestamp
            window (str): stabilization window
            teardown (bool): Indicates if the resource should be torn down at the end
            privileged_client (DynamicClient): Privileged client for api calls
            yaml_file (str): yaml file for the resource.
            delete_timeout (int): timeout associated with delete action
        """
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.containers = containers
        self.timestamp = timestamp
        self.window = window

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "containers": self.containers,
                    "timestamp": self.timestamp,
                    "window": self.window,
                }
            )
