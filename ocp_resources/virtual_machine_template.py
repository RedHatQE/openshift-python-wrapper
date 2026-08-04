# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class VirtualMachineTemplate(NamespacedResource):
    """
    VirtualMachineTemplate is the Schema for the virtualmachinetemplates API
    """

    api_group: str = NamespacedResource.ApiGroup.TEMPLATE_KUBEVIRT_IO

    def __init__(
        self,
        message: str | None = None,
        parameters: list[Any] | None = None,
        virtual_machine: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            message (str): Message is an optional instructional message for this template. This
              field should inform the user how to utilize the newly created
              VirtualMachine.

            parameters (list[Any]): Parameters is an optional list of Parameters used during processing of
              the template.

            virtual_machine (dict[str, Any]): VirtualMachine is the template VirtualMachine to include in this
              template. If a namespace value is hardcoded, it will be removed
              during processing of the template. If the namespace value however
              contains a ${PARAMETER_REFERENCE}, the resolved value after
              parameter substitution will be respected and the VirtualMachine
              will be created in that namespace.

        """
        super().__init__(**kwargs)

        self.message = message
        self.parameters = parameters
        self.virtual_machine = virtual_machine

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.virtual_machine is None:
                raise MissingRequiredArgumentError(argument="self.virtual_machine")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["virtualMachine"] = self.virtual_machine

            if self.message is not None:
                _spec["message"] = self.message

            if self.parameters is not None:
                _spec["parameters"] = self.parameters

    # End of generated code

    def process(
        self,
        parameters: dict[str, str] | None = None,
        client: Any = None,
    ) -> Any:
        """
        Process the VirtualMachineTemplate using the KubeVirt subresources API.

        Sends a POST request to the process subresource endpoint, substituting the
        provided parameter values into the template and returning the result.

        Args:
            parameters (dict[str, str] | None): Key-value pairs of template parameters
                to substitute, e.g. ``{"NAME": "my-vm", "INSTANCETYPE": "u1.large"}``.
                Defaults to an empty dict (no substitutions).
            client: Optional Kubernetes API client. Defaults to ``self.client``.

        Returns:
            Any: The raw API server response object.

        """
        _client = client or self.client
        _subresources_api = f"subresources.{self.api_version}"
        body: dict[str, Any] = {
            "apiVersion": _subresources_api,
            "kind": "ProcessOptions",
            "parameters": parameters or {},
        }
        response = _client.request(
            "POST",
            f"/apis/{_subresources_api}/namespaces/{self.namespace}/virtualmachinetemplates/{self.name}/process",
            body,
        )
        return response
