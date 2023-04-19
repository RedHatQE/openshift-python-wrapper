from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class Lease(NamespacedResource):
    """
    Lease object. API reference:
    https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/lease-v1/
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
        acquire_time=None,
        renew_time=None,
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
            holder_identity (str, optional): identify of the holder of the current lease
            lease_duration_seconds (int, optional): duration that candidates for a lease need to wait to force acquire
            it.
            lease_transitions (int, optional):  number of transitions of a lease between holders.
            acquire_time (time, optional): when the current lease was acquired
            renew_time (time, optional): when current holder of the lease has last updated it
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
        self.acquire_time = acquire_time
        self.renew_time = renew_time

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "acquireTime": self.acquire_time,
                        "renewTime": self.renew_time,
                        "holderIdentity": self.holder_identity,
                        "leaseDurationSeconds": self.lease_duration_seconds,
                        "leaseTransitions": self.lease_transitions,
                    }
                }
            )
