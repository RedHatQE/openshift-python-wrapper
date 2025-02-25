# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class Scheduler(Resource):
    """
       Scheduler holds cluster-wide config information to run the Kubernetes Scheduler and influence its placement decisions. The canonical name for this config is `cluster`.
    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        default_node_selector: Optional[str] = "",
        masters_schedulable: Optional[bool] = None,
        policy: Optional[Dict[str, Any]] = None,
        profile: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            default_node_selector (str): defaultNodeSelector helps set the cluster-wide default node selector
              to restrict pod placement to specific nodes. This is applied to
              the pods created in all namespaces and creates an intersection
              with any existing nodeSelectors already set on a pod, additionally
              constraining that pod's selector. For example,
              defaultNodeSelector: "type=user-node,region=east" would set
              nodeSelector field in pod spec to "type=user-node,region=east" to
              all pods created in all namespaces. Namespaces having project-wide
              node selectors won't be impacted even if this field is set. This
              adds an annotation section to the namespace. For example, if a new
              namespace is created with node-selector='type=user-
              node,region=east', the annotation openshift.io/node-selector:
              type=user-node,region=east gets added to the project. When the
              openshift.io/node-selector annotation is set on the project the
              value is used in preference to the value we are setting for
              defaultNodeSelector field. For instance, openshift.io/node-
              selector: "type=user-node,region=west" means that the default of
              "type=user-node,region=east" set in defaultNodeSelector would not
              be applied.

            masters_schedulable (bool): MastersSchedulable allows masters nodes to be schedulable. When this
              flag is turned on, all the master nodes in the cluster will be
              made schedulable, so that workload pods can run on them. The
              default value for this field is false, meaning none of the master
              nodes are schedulable. Important Note: Once the workload pods
              start running on the master nodes, extreme care must be taken to
              ensure that cluster-critical control plane components are not
              impacted. Please turn on this field after doing due diligence.

            policy (Dict[str, Any]): DEPRECATED: the scheduler Policy API has been deprecated and will be
              removed in a future release. policy is a reference to a ConfigMap
              containing scheduler policy which has user specified predicates
              and priorities. If this ConfigMap is not available scheduler will
              default to use DefaultAlgorithmProvider. The namespace for this
              configmap is openshift-config.

            profile (str): profile sets which scheduling profile should be set in order to
              configure scheduling decisions for new pods.   Valid values are
              "LowNodeUtilization", "HighNodeUtilization", "NoScoring" Defaults
              to "LowNodeUtilization"

        """
        super().__init__(**kwargs)

        self.default_node_selector = default_node_selector
        self.masters_schedulable = masters_schedulable
        self.policy = policy
        self.profile = profile

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.default_node_selector:
                _spec["defaultNodeSelector"] = self.default_node_selector

            if self.masters_schedulable is not None:
                _spec["mastersSchedulable"] = self.masters_schedulable

            if self.policy:
                _spec["policy"] = self.policy

            if self.profile:
                _spec["profile"] = self.profile

    # End of generated code
