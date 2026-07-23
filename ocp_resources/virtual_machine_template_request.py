# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


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
        template_labels: dict[str, Any] | None = None,
        template_name: str | None = None,
        ttl_seconds_after_finished: int | None = None,
        virtual_machine_ref: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            template_labels (dict[str, Any]): TemplateLabels holds optional labels to apply to the created
              VirtualMachineTemplate. Labels with the "template.kubevirt.io/"
              prefix are reserved for system use and are not allowed.

            template_name (str): TemplateName holds the optional name for the new
              VirtualMachineTemplate. If not specified the template will have
              the same name as the VirtualMachineTemplateRequest.

            ttl_seconds_after_finished (int): TTLSecondsAfterFinished limits the lifetime of a
              VirtualMachineTemplateRequest that has finished execution. Failed
              VirtualMachineTemplateRequests are never cleaned up by the TTL
              controller, so they remain available for debugging. If this field
              is unset, the VirtualMachineTemplateRequest is not automatically
              deleted and must be removed manually or through the owner
              reference cleanup described below. If this field is set to zero,
              the VirtualMachineTemplateRequest becomes eligible to be deleted
              immediately after it finishes.

            virtual_machine_ref (dict[str, Any]): VirtualMachineReference holds a reference to a
              VirtualMachine.kubevirt.io

        """
        super().__init__(**kwargs)

        self.template_labels = template_labels
        self.template_name = template_name
        self.ttl_seconds_after_finished = ttl_seconds_after_finished
        self.virtual_machine_ref = virtual_machine_ref

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.virtual_machine_ref is None:
                raise MissingRequiredArgumentError(argument="self.virtual_machine_ref")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["virtualMachineRef"] = self.virtual_machine_ref

            if self.template_labels is not None:
                _spec["templateLabels"] = self.template_labels

            if self.template_name is not None:
                _spec["templateName"] = self.template_name

            if self.ttl_seconds_after_finished is not None:
                _spec["ttlSecondsAfterFinished"] = self.ttl_seconds_after_finished

    # End of generated code
