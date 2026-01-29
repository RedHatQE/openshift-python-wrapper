# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class ValidatingAdmissionPolicy(Resource):
    """
    ValidatingAdmissionPolicy describes the definition of an admission validation policy that accepts or rejects an object without changing it.
    """

    api_group: str = Resource.ApiGroup.ADMISSIONREGISTRATION_K8S_IO

    def __init__(
        self,
        audit_annotations: list[Any] | None = None,
        failure_policy: str | None = None,
        match_conditions: list[Any] | None = None,
        match_constraints: dict[str, Any] | None = None,
        param_kind: dict[str, Any] | None = None,
        validations: list[Any] | None = None,
        variables: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            audit_annotations (list[Any]): auditAnnotations contains CEL expressions which are used to produce
              audit annotations for the audit event of the API request.
              validations and auditAnnotations may not both be empty; a least
              one of validations or auditAnnotations is required.

            failure_policy (str): failurePolicy defines how to handle failures for the admission policy.
              Failures can occur from CEL expression parse errors, type check
              errors, runtime errors and invalid or mis-configured policy
              definitions or bindings.  A policy is invalid if spec.paramKind
              refers to a non-existent Kind. A binding is invalid if
              spec.paramRef.name refers to a non-existent resource.
              failurePolicy does not define how validations that evaluate to
              false are handled.  When failurePolicy is set to Fail,
              ValidatingAdmissionPolicyBinding validationActions define how
              failures are enforced.  Allowed values are Ignore or Fail.
              Defaults to Fail.  Possible enum values:  - `"Fail"` means that an
              error calling the webhook causes the admission to fail.  -
              `"Ignore"` means that an error calling the webhook is ignored.

            match_conditions (list[Any]): MatchConditions is a list of conditions that must be met for a request
              to be validated. Match conditions filter requests that have
              already been matched by the rules, namespaceSelector, and
              objectSelector. An empty list of matchConditions matches all
              requests. There are a maximum of 64 match conditions allowed.  If
              a parameter object is provided, it can be accessed via the
              `params` handle in the same manner as validation expressions.  The
              exact matching logic is (in order):   1. If ANY matchCondition
              evaluates to FALSE, the policy is skipped.   2. If ALL
              matchConditions evaluate to TRUE, the policy is evaluated.   3. If
              any matchCondition evaluates to an error (but none are FALSE):
              - If failurePolicy=Fail, reject the request      - If
              failurePolicy=Ignore, the policy is skipped

            match_constraints (dict[str, Any]): MatchResources decides whether to run the admission control policy on
              an object based on whether it meets the match criteria. The
              exclude rules take precedence over include rules (if a resource
              matches both, it is excluded)

            param_kind (dict[str, Any]): ParamKind is a tuple of Group Kind and Version.

            validations (list[Any]): Validations contain CEL expressions which is used to apply the
              validation. Validations and AuditAnnotations may not both be
              empty; a minimum of one Validations or AuditAnnotations is
              required.

            variables (list[Any]): Variables contain definitions of variables that can be used in
              composition of other expressions. Each variable is defined as a
              named CEL expression. The variables defined here will be available
              under `variables` in other expressions of the policy except
              MatchConditions because MatchConditions are evaluated before the
              rest of the policy.  The expression of a variable can refer to
              other variables defined earlier in the list but not those after.
              Thus, Variables must be sorted by the order of first appearance
              and acyclic.

        """
        super().__init__(**kwargs)

        self.audit_annotations = audit_annotations
        self.failure_policy = failure_policy
        self.match_conditions = match_conditions
        self.match_constraints = match_constraints
        self.param_kind = param_kind
        self.validations = validations
        self.variables = variables

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.audit_annotations is not None:
                _spec["auditAnnotations"] = self.audit_annotations

            if self.failure_policy is not None:
                _spec["failurePolicy"] = self.failure_policy

            if self.match_conditions is not None:
                _spec["matchConditions"] = self.match_conditions

            if self.match_constraints is not None:
                _spec["matchConstraints"] = self.match_constraints

            if self.param_kind is not None:
                _spec["paramKind"] = self.param_kind

            if self.validations is not None:
                _spec["validations"] = self.validations

            if self.variables is not None:
                _spec["variables"] = self.variables

    # End of generated code
