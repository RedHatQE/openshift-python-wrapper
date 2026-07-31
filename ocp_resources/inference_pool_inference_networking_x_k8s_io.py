# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class InferencePool(NamespacedResource):
    """
    InferencePool is the Schema for the InferencePools API.
    """

    api_group: str = NamespacedResource.ApiGroup.INFERENCE_NETWORKING_X_K8S_IO

    def __init__(
        self,
        extension_ref: dict[str, Any] | None = None,
        selector: dict[str, Any] | None = None,
        target_port_number: int | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            extension_ref (dict[str, Any]): Extension configures an endpoint picker as an extension service.

            selector (dict[str, Any]): Selector defines a map of labels to watch model server Pods that
              should be included in the InferencePool. In some cases,
              implementations may translate this field to a Service selector, so
              this matches the simple map used for Service selectors instead of
              the full Kubernetes LabelSelector type. If specified, it will be
              applied to match the model server pods in the same namespace as
              the InferencePool. Cross namesoace selector is not supported.

            target_port_number (int): TargetPortNumber defines the port number to access the selected model
              server Pods. The number must be in the range 1 to 65535.

        """
        super().__init__(**kwargs)

        self.extension_ref = extension_ref
        self.selector = selector
        self.target_port_number = target_port_number

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.extension_ref is None:
                raise MissingRequiredArgumentError(argument="self.extension_ref")

            if self.selector is None:
                raise MissingRequiredArgumentError(argument="self.selector")

            if self.target_port_number is None:
                raise MissingRequiredArgumentError(argument="self.target_port_number")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["extensionRef"] = self.extension_ref
            _spec["selector"] = self.selector
            _spec["targetPortNumber"] = self.target_port_number

    # End of generated code
