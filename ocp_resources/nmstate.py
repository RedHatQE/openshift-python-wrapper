# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import Resource


class NMState(Resource):
    """
    NMState is the Schema for the nmstates API
    """

    api_group: str = Resource.ApiGroup.NMSTATE_IO

    def __init__(
        self,
        affinity: Optional[Dict[str, Any]] = None,
        infra_affinity: Optional[Dict[str, Any]] = None,
        infra_node_selector: Optional[Dict[str, Any]] = None,
        infra_tolerations: Optional[List[Any]] = None,
        node_selector: Optional[Dict[str, Any]] = None,
        self_sign_configuration: Optional[Dict[str, Any]] = None,
        tolerations: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            affinity(Dict[Any, Any]): Affinity is an optional affinity selector that will be added to handler
              DaemonSet manifest.

              FIELDS:
                nodeAffinity	<Object>
                  Describes node affinity scheduling rules for the pod.

                podAffinity	<Object>
                  Describes pod affinity scheduling rules (e.g. co-locate this pod in the same
                  node, zone, etc. as some other pod(s)).

                podAntiAffinity	<Object>
                  Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in
                  the same node, zone, etc. as some other pod(s)).

            infra_affinity(Dict[Any, Any]): Affinity is an optional affinity selector that will be added to webhook &
              certmanager Deployment manifests.

              FIELDS:
                nodeAffinity	<Object>
                  Describes node affinity scheduling rules for the pod.

                podAffinity	<Object>
                  Describes pod affinity scheduling rules (e.g. co-locate this pod in the same
                  node, zone, etc. as some other pod(s)).

                podAntiAffinity	<Object>
                  Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in
                  the same node, zone, etc. as some other pod(s)).

            infra_node_selector(Dict[Any, Any]): InfraNodeSelector is an optional selector that will be added to webhook &
              certmanager Deployment manifests
              If InfraNodeSelector is specified, the webhook and certmanager will run only
              on nodes that have each of the indicated
              key-value pairs as labels applied to the node.

            infra_tolerations(List[Any]): InfraTolerations is an optional list of tolerations to be added to webhook &
              certmanager Deployment manifests
              If InfraTolerations is specified, the webhook and certmanager will be able
              to be scheduled on nodes with corresponding taints
              The pod this Toleration is attached to tolerates any taint that matches
              the triple <key,value,effect> using the matching operator <operator>.

              FIELDS:
                effect	<string>
                  Effect indicates the taint effect to match. Empty means match all taint
                  effects.
                  When specified, allowed values are NoSchedule, PreferNoSchedule and
                  NoExecute.

                key	<string>
                  Key is the taint key that the toleration applies to. Empty means match all
                  taint keys.
                  If the key is empty, operator must be Exists; this combination means to
                  match all values and all keys.

                operator	<string>
                  Operator represents a key's relationship to the value.
                  Valid operators are Exists and Equal. Defaults to Equal.
                  Exists is equivalent to wildcard for value, so that a pod can
                  tolerate all taints of a particular category.

                tolerationSeconds	<integer>
                  TolerationSeconds represents the period of time the toleration (which must
                  be
                  of effect NoExecute, otherwise this field is ignored) tolerates the taint.
                  By default,
                  it is not set, which means tolerate the taint forever (do not evict). Zero
                  and
                  negative values will be treated as 0 (evict immediately) by the system.

                value	<string>
                  Value is the taint value the toleration matches to.
                  If the operator is Exists, the value should be empty, otherwise just a
                  regular string.

            node_selector(Dict[Any, Any]): NodeSelector is an optional selector that will be added to handler DaemonSet
              manifest
              for both workers and control-plane
              (https://github.com/nmstate/kubernetes-nmstate/blob/main/deploy/handler/operator.yaml).
              If NodeSelector is specified, the handler will run only on nodes that have
              each of the indicated key-value pairs
              as labels applied to the node.

            self_sign_configuration(Dict[Any, Any]): SelfSignConfiguration defines self signed certificate configuration

              FIELDS:
                caOverlapInterval	<string>
                  CAOverlapInterval defines the duration where expired CA certificate
                  can overlap with new one, in order to allow fluent CA rotation transitioning

                caRotateInterval	<string>
                  CARotateInterval defines duration for CA expiration

                certOverlapInterval	<string>
                  CertOverlapInterval defines the duration where expired service certificate
                  can overlap with new one, in order to allow fluent service rotation
                  transitioning

                certRotateInterval	<string>
                  CertRotateInterval defines duration for of service certificate expiration

            tolerations(List[Any]): Tolerations is an optional list of tolerations to be added to handler
              DaemonSet manifest
              If Tolerations is specified, the handler daemonset will be also scheduled on
              nodes with corresponding taints
              The pod this Toleration is attached to tolerates any taint that matches
              the triple <key,value,effect> using the matching operator <operator>.

              FIELDS:
                effect	<string>
                  Effect indicates the taint effect to match. Empty means match all taint
                  effects.
                  When specified, allowed values are NoSchedule, PreferNoSchedule and
                  NoExecute.

                key	<string>
                  Key is the taint key that the toleration applies to. Empty means match all
                  taint keys.
                  If the key is empty, operator must be Exists; this combination means to
                  match all values and all keys.

                operator	<string>
                  Operator represents a key's relationship to the value.
                  Valid operators are Exists and Equal. Defaults to Equal.
                  Exists is equivalent to wildcard for value, so that a pod can
                  tolerate all taints of a particular category.

                tolerationSeconds	<integer>
                  TolerationSeconds represents the period of time the toleration (which must
                  be
                  of effect NoExecute, otherwise this field is ignored) tolerates the taint.
                  By default,
                  it is not set, which means tolerate the taint forever (do not evict). Zero
                  and
                  negative values will be treated as 0 (evict immediately) by the system.

                value	<string>
                  Value is the taint value the toleration matches to.
                  If the operator is Exists, the value should be empty, otherwise just a
                  regular string.

        """
        super().__init__(**kwargs)

        self.affinity = affinity
        self.infra_affinity = infra_affinity
        self.infra_node_selector = infra_node_selector
        self.infra_tolerations = infra_tolerations
        self.node_selector = node_selector
        self.self_sign_configuration = self_sign_configuration
        self.tolerations = tolerations

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.affinity:
                _spec["affinity"] = self.affinity

            if self.infra_affinity:
                _spec["infraAffinity"] = self.infra_affinity

            if self.infra_node_selector:
                _spec["infraNodeSelector"] = self.infra_node_selector

            if self.infra_tolerations:
                _spec["infraTolerations"] = self.infra_tolerations

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.self_sign_configuration:
                _spec["selfSignConfiguration"] = self.self_sign_configuration

            if self.tolerations:
                _spec["tolerations"] = self.tolerations
