# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class MTQ(Resource):
    """
    MTQ is the MTQ Operator CRD
    """

    api_group: str = Resource.ApiGroup.MTQ_KUBEVIRT_IO

    def __init__(
        self,
        cert_config: Optional[Dict[str, Any]] = None,
        image_pull_policy: Optional[str] = "",
        infra: Optional[Dict[str, Any]] = None,
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

            image_pull_policy(str): PullPolicy describes a policy for if/when to pull a container image

            infra(Dict[Any, Any]): Rules on which nodes MTQ infrastructure pods will be scheduled

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

            priority_class(str): PriorityClass of the MTQ control plane

            workload(Dict[Any, Any]): Restrict on which nodes MTQ workload pods will be scheduled

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
        self.image_pull_policy = image_pull_policy
        self.infra = infra
        self.priority_class = priority_class
        self.workload = workload

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cert_config:
                _spec["certConfig"] = self.cert_config

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.infra:
                _spec["infra"] = self.infra

            if self.priority_class:
                _spec["priorityClass"] = self.priority_class

            if self.workload:
                _spec["workload"] = self.workload
