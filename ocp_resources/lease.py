from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class Lease(NamespacedResource):
    """
    Lease object. API reference:
    https://docs.openshift.com/container-platform/4.12/rest_api/metadata_apis/lease-coordination-k8s-io-v1.html
    """

    api_group = NamespacedResource.ApiGroup.COORDINATION_K8S_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        holder_identity=None,
        lease_duration_seconds=None,
        lease_transitions=None,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the endpoints resource
            namespace (str): Namespace of endpoints resource
            client: (DynamicClient): DynamicClient for api calls
            teardown (bool): Indicates if the resource should be torn down at the end
            holder_identity (str): identify of the holder of the current lease
            lease_duration_seconds (int): duration that candidates for a lease need to wait to force acquire it.
            lease_transitions (int):  number of transitions of a lease between holders.
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
        self.holder_identity = holder_identity
        self.lease_transitions = lease_transitions
        self.lease_duration_seconds = lease_duration_seconds

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "holderIdentity": self.holder_identity,
                        "leaseDurationSeconds": self.lease_duration_seconds,
                        "leaseTransitions": self.lease_transitions,
                    }
                }
            )
