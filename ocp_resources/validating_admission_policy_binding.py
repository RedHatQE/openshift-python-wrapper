# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class ValidatingAdmissionPolicyBinding(Resource):
    """
        ValidatingAdmissionPolicyBinding binds the ValidatingAdmissionPolicy with paramerized resources. ValidatingAdmissionPolicyBinding and parameter CRDs together define how cluster administrators configure policies for clusters.

    For a given admission request, each binding will cause its policy to be evaluated N times, where N is 1 for policies/bindings that don't use params, otherwise N is the number of parameters selected by the binding.

    The CEL expressions of a policy must have a computed CEL cost below the maximum CEL budget. Each evaluation of the policy is given an independent CEL cost budget. Adding/removing policies, bindings, or params can not affect whether a given (policy, binding, param) combination is within its own CEL budget.
    """

    api_group: str = Resource.ApiGroup.ADMISSIONREGISTRATION_K8S_IO

    def __init__(
        self,
        match_resources: dict[str, Any] | None = None,
        param_ref: dict[str, Any] | None = None,
        policy_name: str | None = None,
        validation_actions: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            match_resources (dict[str, Any]): MatchResources decides whether to run the admission control policy on
              an object based on whether it meets the match criteria. The
              exclude rules take precedence over include rules (if a resource
              matches both, it is excluded)

            param_ref (dict[str, Any]): ParamRef describes how to locate the params to be used as input to
              expressions of rules applied by a policy binding.

            policy_name (str): PolicyName references a ValidatingAdmissionPolicy name which the
              ValidatingAdmissionPolicyBinding binds to. If the referenced
              resource does not exist, this binding is considered invalid and
              will be ignored Required.

            validation_actions (list[Any]): validationActions declares how Validations of the referenced
              ValidatingAdmissionPolicy are enforced. If a validation evaluates
              to false it is always enforced according to these actions.
              Failures defined by the ValidatingAdmissionPolicy's FailurePolicy
              are enforced according to these actions only if the FailurePolicy
              is set to Fail, otherwise the failures are ignored. This includes
              compilation errors, runtime errors and misconfigurations of the
              policy.  validationActions is declared as a set of action values.
              Order does not matter. validationActions may not contain
              duplicates of the same action.  The supported actions values are:
              "Deny" specifies that a validation failure results in a denied
              request.  "Warn" specifies that a validation failure is reported
              to the request client in HTTP Warning headers, with a warning code
              of 299. Warnings can be sent both for allowed or denied admission
              responses.  "Audit" specifies that a validation failure is
              included in the published audit event for the request. The audit
              event will contain a
              `validation.policy.admission.k8s.io/validation_failure` audit
              annotation with a value containing the details of the validation
              failures, formatted as a JSON list of objects, each with the
              following fields: - message: The validation failure message string
              - policy: The resource name of the ValidatingAdmissionPolicy -
              binding: The resource name of the ValidatingAdmissionPolicyBinding
              - expressionIndex: The index of the failed validations in the
              ValidatingAdmissionPolicy - validationActions: The enforcement
              actions enacted for the validation failure Example audit
              annotation:
              `"validation.policy.admission.k8s.io/validation_failure":
              "[{\"message\": \"Invalid value\", {\"policy\":
              \"policy.example.com\", {\"binding\":
              \"policybinding.example.com\", {\"expressionIndex\": \"1\",
              {\"validationActions\": [\"Audit\"]}]"`  Clients should expect to
              handle additional values by ignoring any values not recognized.
              "Deny" and "Warn" may not be used together since this combination
              needlessly duplicates the validation failure both in the API
              response body and the HTTP warning headers.  Required.

        """
        super().__init__(**kwargs)

        self.match_resources = match_resources
        self.param_ref = param_ref
        self.policy_name = policy_name
        self.validation_actions = validation_actions

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.match_resources is not None:
                _spec["matchResources"] = self.match_resources

            if self.param_ref is not None:
                _spec["paramRef"] = self.param_ref

            if self.policy_name is not None:
                _spec["policyName"] = self.policy_name

            if self.validation_actions is not None:
                _spec["validationActions"] = self.validation_actions

    # End of generated code
