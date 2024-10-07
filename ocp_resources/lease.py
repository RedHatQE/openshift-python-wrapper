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
            name (str): Name of the Lease resource
            namespace (str): Namespace of Lease resource
            client: (DynamicClient): DynamicClient for api calls
            teardown (bool): Indicates if the resource should be torn down at the end
            holder_identity (str, optional): identify of the holder of the current lease
            lease_duration_seconds (int, optional): duration for which candidate of a lease needs to wait to acquire it
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

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if self.acquire_time:
                self.res["spec"]["acquireTime"] = self.acquire_time
            if self.renew_time:
                self.res["spec"]["renewTime"] = self.renew_time
            if self.holder_identity:
                self.res["spec"]["holderIdentity"] = self.holder_identity
            if self.lease_duration_seconds:
                self.res["spec"]["leaseDurationSeconds"] = self.lease_duration_seconds
            if self.lease_transitions:
                self.res["spec"]["leaseTransitions"] = self.lease_transitions
