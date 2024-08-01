# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class AAQ(Resource):
    """
    AAQ is the AAQ Operator CRD
    """

    api_group: str = Resource.ApiGroup.AAQ_KUBEVIRT_IO

    def __init__(
        self,
        cert_config: Optional[Dict[str, Any]] = None,
        configuration: Optional[Dict[str, Any]] = None,
        image_pull_policy: Optional[str] = "",
        infra: Optional[Dict[str, Any]] = None,
        namespace_selector: Optional[Dict[str, Any]] = None,
        priority_class: Optional[str] = "",
        workload: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            cert_config(Dict[Any, Any]): certificate configuration

              FIELDS:
                ca	<Object>
                  CA configuration CA certs are kept in the CA bundle as long as they are
                  valid

                server	<Object>
                  Server configuration Certs are rotated and discarded

            configuration(Dict[Any, Any]): holds aaq configurations.

              FIELDS:
                allowApplicationAwareClusterResourceQuota	<boolean>
                  AllowApplicationAwareClusterResourceQuota can be set to true to allow
                  creation and management of ApplicationAwareClusterResourceQuota. Defaults to
                  false

                sidecarEvaluators	<[]Object>
                  SidecarEvaluators allow custom quota counting for external operator

                vmiCalculatorConfiguration	<Object>
                  VmiCalculatorConfiguration determine how resource allocation will be done
                  with ApplicationAwareResourceQuota

            image_pull_policy(str): PullPolicy describes a policy for if/when to pull a container image

            infra(Dict[Any, Any]): Rules on which nodes AAQ infrastructure pods will be scheduled

              FIELDS:
                affinity	<Object>
                  affinity enables pod affinity/anti-affinity placement expanding the types of
                  constraints that can be expressed with nodeSelector. affinity is going to be
                  applied to the relevant kind of pods in parallel with nodeSelector See
                  https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity

                nodeSelector	<map[string]string>
                  nodeSelector is the node selector applied to the relevant kind of pods It
                  specifies a map of key-value pairs: for the pod to be eligible to run on a
                  node, the node must have each of the indicated key-value pairs as labels (it
                  can have additional labels as well). See
                  https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector

                tolerations	<[]Object>
                  tolerations is a list of tolerations applied to the relevant kind of pods
                  See https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
                  for more info. These are additional tolerations other than default ones.

            namespace_selector(Dict[Any, Any]): namespaces where pods should be gated before scheduling Defaults to
              targeting namespaces with an "application-aware-quota/enable-gating" label
              key.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            priority_class(str): PriorityClass of the AAQ control plane

            workload(Dict[Any, Any]): Restrict on which nodes AAQ workload pods will be scheduled

              FIELDS:
                affinity	<Object>
                  affinity enables pod affinity/anti-affinity placement expanding the types of
                  constraints that can be expressed with nodeSelector. affinity is going to be
                  applied to the relevant kind of pods in parallel with nodeSelector See
                  https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity

                nodeSelector	<map[string]string>
                  nodeSelector is the node selector applied to the relevant kind of pods It
                  specifies a map of key-value pairs: for the pod to be eligible to run on a
                  node, the node must have each of the indicated key-value pairs as labels (it
                  can have additional labels as well). See
                  https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector

                tolerations	<[]Object>
                  tolerations is a list of tolerations applied to the relevant kind of pods
                  See https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
                  for more info. These are additional tolerations other than default ones.

        """
        super().__init__(**kwargs)

        self.cert_config = cert_config
        self.configuration = configuration
        self.image_pull_policy = image_pull_policy
        self.infra = infra
        self.namespace_selector = namespace_selector
        self.priority_class = priority_class
        self.workload = workload

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cert_config:
                _spec["certConfig"] = self.cert_config

            if self.configuration:
                _spec["configuration"] = self.configuration

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.infra:
                _spec["infra"] = self.infra

            if self.namespace_selector:
                _spec["namespaceSelector"] = self.namespace_selector

            if self.priority_class:
                _spec["priorityClass"] = self.priority_class

            if self.workload:
                _spec["workload"] = self.workload
