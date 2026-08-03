# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import Resource


class ClusterQueue(Resource):
    """
    ClusterQueue is the Schema for the clusterQueue API.
    """

    api_group: str = Resource.ApiGroup.KUEUE_X_K8S_IO

    def __init__(
        self,
        admission_checks: list[Any] | None = None,
        admission_checks_strategy: dict[str, Any] | None = None,
        admission_scope: dict[str, Any] | None = None,
        cohort: str | None = None,
        cohort_name: str | None = None,
        fair_sharing: dict[str, Any] | None = None,
        flavor_fungibility: dict[str, Any] | None = None,
        namespace_selector: dict[str, Any] | None = None,
        preemption: dict[str, Any] | None = None,
        queueing_strategy: str | None = None,
        resource_groups: list[Any] | None = None,
        stop_policy: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            admission_checks (list[Any]): admissionChecks lists the AdmissionChecks required by this
              ClusterQueue. Cannot be used along with AdmissionCheckStrategy.
              Available in kueue.x-k8s.io/v1beta1.

            admission_checks_strategy (dict[str, Any]): admissionCheckStrategy defines a list of strategies to determine which
              ResourceFlavors require AdmissionChecks.

            admission_scope (dict[str, Any]): admissionScope indicates whether the ClusterQueue participates in
              AdmissionFairSharing. Available in kueue.x-k8s.io/v1beta2+.

            cohort (str): cohort that this ClusterQueue belongs to. CQs that belong to the same
              cohort can borrow unused resources from each other.
              Available in kueue.x-k8s.io/v1beta1.

            cohort_name (str): cohortName that this ClusterQueue belongs to. CQs that belong to the
              same cohort can borrow unused resources from each other. A CQ can
              be a member of a single borrowing cohort. A workload submitted to
              a queue referencing this CQ can borrow quota from any CQ in the
              cohort. Only quota for the [resource, flavor] pairs listed in the
              CQ can be borrowed. If empty, this ClusterQueue cannot borrow from
              any other ClusterQueue and vice versa. A cohort is a name that
              links CQs together, but it doesn't reference any object.
              Available in kueue.x-k8s.io/v1beta2+.

            fair_sharing (dict[str, Any]): fairSharing defines the properties of the ClusterQueue when
              participating in FairSharing.  The values are only relevant if
              FairSharing is enabled in the Kueue configuration.

            flavor_fungibility (dict[str, Any]): flavorFungibility defines whether a workload should try the next
              flavor before borrowing or preempting in the flavor being
              evaluated.

            namespace_selector (dict[str, Any]): namespaceSelector defines which namespaces are allowed to submit
              workloads to this clusterQueue. Beyond this basic support for
              policy, a policy agent like Gatekeeper should be used to enforce
              more advanced policies. Defaults to null which is a nothing
              selector (no namespaces eligible). If set to an empty selector
              `{}`, then all namespaces are eligible.

            preemption (dict[str, Any]): preemption defines the preemption policies for the ClusterQueue.

            queueing_strategy (str): QueueingStrategy indicates the queueing strategy of the workloads
              across the queues in this ClusterQueue. Current Supported
              Strategies:  - StrictFIFO: workloads are ordered strictly by
              creation time. Older workloads that can't be admitted will block
              admitting newer workloads even if they fit available quota. -
              BestEffortFIFO: workloads are ordered by creation time, however
              older workloads that can't be admitted will not block admitting
              newer workloads that fit existing quota.

            resource_groups (list[Any]): resourceGroups describes groups of resources. Each resource group
              defines the list of resources and a list of flavors that provide
              quotas for these resources. Each resource and each flavor can only
              form part of one resource group. resourceGroups can be up to 16.

            stop_policy (str): stopPolicy - if set to a value different from None, the ClusterQueue
              is considered Inactive, no new reservation being made.  Depending
              on its value, its associated workloads will:  - None - Workloads
              are admitted - HoldAndDrain - Admitted workloads are evicted and
              Reserving workloads will cancel the reservation. - Hold - Admitted
              workloads will run to completion and Reserving workloads will
              cancel the reservation.

        """
        super().__init__(**kwargs)

        self.admission_checks = admission_checks
        self.admission_checks_strategy = admission_checks_strategy
        self.admission_scope = admission_scope
        self.cohort = cohort
        self.cohort_name = cohort_name
        self.fair_sharing = fair_sharing
        self.flavor_fungibility = flavor_fungibility
        self.namespace_selector = namespace_selector
        self.preemption = preemption
        self.queueing_strategy = queueing_strategy
        self.resource_groups = resource_groups
        self.stop_policy = stop_policy

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.admission_checks is not None:
                _spec["admissionChecks"] = self.admission_checks

            if self.admission_checks_strategy is not None:
                _spec["admissionChecksStrategy"] = self.admission_checks_strategy

            if self.admission_scope is not None:
                _spec["admissionScope"] = self.admission_scope

            if self.cohort is not None:
                _spec["cohort"] = self.cohort

            if self.cohort_name is not None:
                _spec["cohortName"] = self.cohort_name

            if self.fair_sharing is not None:
                _spec["fairSharing"] = self.fair_sharing

            if self.flavor_fungibility is not None:
                _spec["flavorFungibility"] = self.flavor_fungibility

            if self.namespace_selector is not None:
                _spec["namespaceSelector"] = self.namespace_selector

            if self.preemption is not None:
                _spec["preemption"] = self.preemption

            if self.queueing_strategy is not None:
                _spec["queueingStrategy"] = self.queueing_strategy

            if self.resource_groups is not None:
                _spec["resourceGroups"] = self.resource_groups

            if self.stop_policy is not None:
                _spec["stopPolicy"] = self.stop_policy

    # End of generated code
