# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class LocalQueue(NamespacedResource):
    """
    LocalQueue is the Schema for the localQueues API
    """

    api_group: str = NamespacedResource.ApiGroup.KUEUE_X_K8S_IO

    def __init__(
        self,
        cluster_queue: str | None = None,
        fair_sharing: dict[str, Any] | None = None,
        stop_policy: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            cluster_queue (str): clusterQueue is a reference to a clusterQueue that backs this
              localQueue.

            fair_sharing (dict[str, Any]): fairSharing defines the properties of the LocalQueue when
              participating in AdmissionFairSharing. The values are only
              relevant if AdmissionFairSharing is enabled in the Kueue
              configuration. Available in kueue.x-k8s.io/v1beta2+.

            stop_policy (str): stopPolicy - if set to a value different from None, the LocalQueue is
              considered Inactive, no new reservation being made.  Depending on
              its value, its associated workloads will:  - None - Workloads are
              admitted - HoldAndDrain - Admitted workloads are evicted and
              Reserving workloads will cancel the reservation. - Hold - Admitted
              workloads will run to completion and Reserving workloads will
              cancel the reservation.

        """
        super().__init__(**kwargs)

        self.cluster_queue = cluster_queue
        self.fair_sharing = fair_sharing
        self.stop_policy = stop_policy

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cluster_queue is not None:
                _spec["clusterQueue"] = self.cluster_queue

            if self.fair_sharing is not None:
                _spec["fairSharing"] = self.fair_sharing

            if self.stop_policy is not None:
                _spec["stopPolicy"] = self.stop_policy

    # End of generated code
