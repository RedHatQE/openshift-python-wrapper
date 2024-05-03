from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ReclaimSpaceJob(NamespacedResource):
    """
    https://github.com/csi-addons/kubernetes-csi-addons/blob/main/docs/reclaimspace.md

    Args:
        name (str): ReclaimSpaceJob name.
        namespace (str): Namespace name.
        client (DynamicClient): Dynamic client for connecting to a remote cluster.
        teardown (bool): Indicates if this resource would need to be deleted.
        privileged_client (DynamicClient): Instance of Dynamic client.
        yaml_file (str): Yaml file for the resource.
        delete_timeout (int): Timeout associated with delete action.
        backoff_limit (int, Optional): The number of retries for a reclaim space job.
        target (dict): Volume target on which the operation would be performed.
        retryDeadlineSeconds (int, Optional): Optional. Duration in seconds relative to the start time that the
            operation may beretried.
        timeout (int, Optional): specifies the timeout in seconds for the grpc request sent to the CSI driver
    """

    api_group = NamespacedResource.ApiGroup.CSIADDONS_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        backoff_limit=None,
        target=None,
        retry_deadline_seconds=None,
        timeout=None,
        **kwargs,
    ):
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
        self.backoff_limit = backoff_limit
        self.target = target
        self.retry_deadline_seconds = retry_deadline_seconds
        self.timeout = timeout

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if not self.target:
                raise MissingRequiredArgumentError(argument="target")
            spec_dict = {}
            if self.target:
                spec_dict.update({"target": self.target})
            if self.retry_deadline_seconds:
                spec_dict.update({"retryDeadlineSeconds": self.retry_deadline_seconds})
            if self.timeout:
                spec_dict.update({"timeout": self.timeout})
            if self.backoff_limit:
                spec_dict.update({"backOffLimit": self.backoff_limit})
            if spec_dict:
                self.res.update({"spec": spec_dict})
