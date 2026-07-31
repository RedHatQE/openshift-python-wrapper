# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class InferencePool(NamespacedResource):
    """
    InferencePool is the Schema for the InferencePools API.

    """

    api_group: str = NamespacedResource.ApiGroup.INFERENCE_NETWORKING_K8S_IO

    def __init__(
        self,
        app_protocol: str | None = None,
        endpoint_picker_ref: dict[str, Any] | None = None,
        selector: dict[str, Any] | None = None,
        target_ports: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            app_protocol (str): AppProtocol describes the application protocol for all the target
              ports.  If unspecified, the protocol defaults to HTTP/1.1.
              Supported values include: * "http": HTTP/1.1. This is the default.
              * "kubernetes.io/h2c": HTTP/2 over cleartext.

            endpoint_picker_ref (dict[str, Any]): EndpointPickerRef is a reference to the Endpoint Picker extension and
              its associated configuration.

            selector (dict[str, Any]): Selector determines which Pods are members of this inference pool. It
              matches Pods by their labels only within the same namespace;
              cross-namespace selection is not supported.  The structure of this
              LabelSelector is intentionally simple to be compatible with
              Kubernetes Service selectors, as some implementations may
              translate this configuration into a Service resource.

            target_ports (list[Any]): TargetPorts defines a list of ports that are exposed by this
              InferencePool. Every port will be treated as a distinctive
              endpoint by EPP, addressable as a 'podIP:portNumber' combination.

        """
        super().__init__(**kwargs)

        self.app_protocol = app_protocol
        self.endpoint_picker_ref = endpoint_picker_ref
        self.selector = selector
        self.target_ports = target_ports

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.endpoint_picker_ref is None:
                raise MissingRequiredArgumentError(argument="self.endpoint_picker_ref")

            if self.selector is None:
                raise MissingRequiredArgumentError(argument="self.selector")

            if self.target_ports is None:
                raise MissingRequiredArgumentError(argument="self.target_ports")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["endpointPickerRef"] = self.endpoint_picker_ref
            _spec["selector"] = self.selector
            _spec["targetPorts"] = self.target_ports

            if self.app_protocol is not None:
                _spec["appProtocol"] = self.app_protocol

    # End of generated code
