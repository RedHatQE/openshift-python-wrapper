# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class VirtualMachineTemplateRequest(NamespacedResource):
    """
    VirtualMachineTemplateRequest is the Schema for the virtualmachinetemplaterequests API
    """

    api_group: str = NamespacedResource.ApiGroup.TEMPLATE_KUBEVIRT_IO

    def __init__(
        self,
        template_name: str | None = None,
        virtual_machine_ref: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            template_name (str): TemplateName holds the optional name for the new
              VirtualMachineTemplate. If not specified the template will have
              the same name as the VirtualMachineTemplateRequest.

            virtual_machine_ref (dict[str, Any]): VirtualMachineReference holds a reference to a
              VirtualMachine.kubevirt.io

        """
        super().__init__(**kwargs)

        self.template_name = template_name
        self.virtual_machine_ref = virtual_machine_ref

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.virtual_machine_ref is None:
                raise MissingRequiredArgumentError(argument="self.virtual_machine_ref")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["virtualMachineRef"] = self.virtual_machine_ref

            if self.template_name is not None:
                _spec["templateName"] = self.template_name

    # End of generated code
