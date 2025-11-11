# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class VirtualMachineInstancePreset(NamespacedResource):
    """
        Deprecated for removal in v2, please use VirtualMachineInstanceType and VirtualMachinePreference instead.

    VirtualMachineInstancePreset defines a VMI spec.domain to be applied to all VMIs that match the provided label selector
    More info: https://kubevirt.io/user-guide/virtual_machines/presets/#overrides
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        domain: dict[str, Any] | None = None,
        selector: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            domain (dict[str, Any]): Domain is the same object type as contained in
              VirtualMachineInstanceSpec

            selector (dict[str, Any]): Selector is a label query over a set of VMIs. Required.

        """
        super().__init__(**kwargs)

        self.domain = domain
        self.selector = selector

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.selector is None:
                raise MissingRequiredArgumentError(argument="self.selector")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["selector"] = self.selector

            if self.domain is not None:
                _spec["domain"] = self.domain

    # End of generated code
