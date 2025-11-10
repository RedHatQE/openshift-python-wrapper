# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import Resource


class GatewayClass(Resource):
    """
        GatewayClass describes a class of Gateways available to the user for creating
    Gateway resources.

    It is recommended that this resource be used as a template for Gateways. This
    means that a Gateway is based on the state of the GatewayClass at the time it
    was created and changes to the GatewayClass or associated parameters are not
    propagated down to existing Gateways. This recommendation is intended to
    limit the blast radius of changes to GatewayClass or associated parameters.
    If implementations choose to propagate GatewayClass changes to existing
    Gateways, that MUST be clearly documented by the implementation.

    Whenever one or more Gateways are using a GatewayClass, implementations SHOULD
    add the `gateway-exists-finalizer.gateway.networking.k8s.io` finalizer on the
    associated GatewayClass. This ensures that a GatewayClass associated with a
    Gateway is not deleted while in use.

    GatewayClass is a Cluster level resource.
    """

    api_group: str = Resource.ApiGroup.GATEWAY_NETWORKING_K8S_IO

    def __init__(
        self,
        controller_name: str | None = None,
        description: str | None = None,
        parameters_ref: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            controller_name (str): ControllerName is the name of the controller that is managing Gateways
              of this class. The value of this field MUST be a domain prefixed
              path.  Example: "example.net/gateway-controller".  This field is
              not mutable and cannot be empty.  Support: Core

            description (str): Description helps describe a GatewayClass with more details.

            parameters_ref (dict[str, Any]): ParametersRef is a reference to a resource that contains the
              configuration parameters corresponding to the GatewayClass. This
              is optional if the controller does not require any additional
              configuration.  ParametersRef can reference a standard Kubernetes
              resource, i.e. ConfigMap, or an implementation-specific custom
              resource. The resource can be cluster-scoped or namespace-scoped.
              If the referent cannot be found, refers to an unsupported kind, or
              when the data within that resource is malformed, the GatewayClass
              SHOULD be rejected with the "Accepted" status condition set to
              "False" and an "InvalidParameters" reason.  A Gateway for this
              GatewayClass may provide its own `parametersRef`. When both are
              specified, the merging behavior is implementation specific. It is
              generally recommended that GatewayClass provides defaults that can
              be overridden by a Gateway.  Support: Implementation-specific

        """
        super().__init__(**kwargs)

        self.controller_name = controller_name
        self.description = description
        self.parameters_ref = parameters_ref

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.controller_name is None:
                raise MissingRequiredArgumentError(argument="self.controller_name")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["controllerName"] = self.controller_name

            if self.description is not None:
                _spec["description"] = self.description

            if self.parameters_ref is not None:
                _spec["parametersRef"] = self.parameters_ref

    # End of generated code
