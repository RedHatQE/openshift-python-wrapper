from __future__ import annotations

from typing import Any

from ocp_resources.resource import NamespacedResource
from ocp_resources.utils.constants import TIMEOUT_4MINUTES


class Lease(NamespacedResource):
    """
    Lease object. API reference:
    https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/lease-v1/
    """

    api_group = NamespacedResource.ApiGroup.COORDINATION_K8S_IO

    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
        teardown: bool = True,
        yaml_file: str | None = None,
        delete_timeout: int = TIMEOUT_4MINUTES,
        holder_identity: str | None = None,
        acquire_time: str | None = None,
        renew_time: str | None = None,
        lease_duration_seconds: int | None = None,
        lease_transitions: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            name (str): Name of the Lease resource
            namespace (str): Namespace of Lease resource
            teardown (bool): Indicates if the resource should be torn down at the end
            holder_identity (str, optional): identify of the holder of the current lease
            lease_duration_seconds (int, optional): duration for which candidate of a lease needs to wait to acquire it
            lease_transitions (int, optional):  number of transitions of a lease between holders.
            acquire_time (time, optional): when the current lease was acquired
            renew_time (time, optional): when current holder of the lease has last updated it
            yaml_file (str): yaml file for the resource.
            delete_timeout (int): timeout associated with delete action
        """
        super().__init__(
            name=name,
            namespace=namespace,
            teardown=teardown,
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
