from ocp_resources.resource import MissingRequiredArgumentError, Resource


class NodeHealthCheck(Resource):
    """
    NodeHealthCheck object.
    Reference : https://github.com/medik8s/node-healthcheck-operator
    """

    api_group = Resource.ApiGroup.REMEDIATION_MEDIK8S_IO

    def __init__(
        self,
        selector_match_expressions=None,
        selector_match_labels=None,
        min_unhealthy=None,
        unhealthy_conditions=None,
        escalating_remediation=None,
        remediation_template=None,
        **kwargs,
    ):
        """
        Create NodeHealthCheck object.

        Args:
            selector_match_expressions (dict, Optional if `selector_match_labels` exist): Belongs to selector object.
                This helps in matching nodes.
            selector_match_labels (dict, Optional if `selector_match_expressions` exist): Belongs to selector object.
                This is a map of {key,value} pairs.
            min_unhealthy (int, Optional): Remediation is allowed if at least "MinHealthy" nodes selected by "selector"
            unhealthy_conditions (list, Optional): UnhealthyConditions contains a list of the conditions that determine
                whether a node is considered unhealthy.
            remediation_template (dict, mandatory if `escalating_remediation` is not provided) : remediation template
                provided by an infrastructure provider.
            escalating_remediation (list, mandatory if `remediation_template` is not provided): EscalatingRemediations
                contain a list of ordered remediation templates with a timeout.
                example: [{'remediationTemplate': {'apiVersion': 'self-node-remediation.medik8s.io/v1alpha1', 'kind':
                'SelfNodeRemediationTemplate', 'namespace': 'openshift-operators',
                'name': 'self-node-remediation-resource-deletion-template'}, 'order': 1, 'timeout': '70s'}]
        """
        super().__init__(
            **kwargs,
        )
        self.selector_match_expressions = selector_match_expressions
        self.selector_match_labels = selector_match_labels
        self.min_unhealthy = min_unhealthy
        self.unhealthy_conditions = unhealthy_conditions
        self.escalating_remediation = escalating_remediation
        self.remediation_template = remediation_template

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not (self.selector_match_expressions or self.selector_match_labels):
                raise MissingRequiredArgumentError(argument="'selector_match_expressions' or 'selector_match_labels'")

            if self.escalating_remediation and self.remediation_template:
                raise ValueError("remediation_template and escalating_remediation  usage is mutual exclusive")

            spec = self.res.setdefault("spec", {})

            if self.escalating_remediation:
                spec["escalatingRemediations"] = self.escalating_remediation

            if self.remediation_template:
                spec["remediationTemplate"] = self.remediation_template

            if self.min_unhealthy:
                spec["minHealthy"] = self.min_unhealthy

            if self.unhealthy_conditions:
                spec["unhealthyConditions"] = self.unhealthy_conditions

            spec.setdefault("selector", {})

            if self.selector_match_expressions:
                spec["selector"]["matchExpressions"] = self.selector_match_expressions

            if self.selector_match_labels:
                spec["selector"]["matchLabels"] = self.selector_match_labels
