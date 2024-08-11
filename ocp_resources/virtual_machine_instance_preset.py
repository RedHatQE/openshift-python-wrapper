# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class VirtualMachineInstancePreset(NamespacedResource):
    """
    Deprecated for removal in v2, please use VirtualMachineInstanceType and
    VirtualMachinePreference instead.
     VirtualMachineInstancePreset defines a VMI spec.domain to be applied to all
    VMIs that match the provided label selector More info:
    https://kubevirt.io/user-guide/virtual_machines/presets/#overrides
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        domain: Optional[Dict[str, Any]] = None,
        selector: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            domain(Dict[Any, Any]): Domain is the same object type as contained in VirtualMachineInstanceSpec

              FIELDS:
                chassis	<Object>
                  Chassis specifies the chassis info passed to the domain.

                clock	<Object>
                  Clock sets the clock and timers of the vmi.

                cpu	<Object>
                  CPU allow specified the detailed CPU topology inside the vmi.

                devices	<Object> -required-
                  Devices allows adding disks, network interfaces, and others

                features	<Object>
                  Features like acpi, apic, hyperv, smm.

                firmware	<Object>
                  Firmware.

                ioThreadsPolicy	<string>
                  Controls whether or not disks will share IOThreads. Omitting IOThreadsPolicy
                  disables use of IOThreads. One of: shared, auto

                launchSecurity	<Object>
                  Launch Security setting of the vmi.

                machine	<Object>
                  Machine type.

                memory	<Object>
                  Memory allow specifying the VMI memory features.

                resources	<Object>
                  Resources describes the Compute Resources required by this vmi.

            selector(Dict[Any, Any]): Selector is a label query over a set of VMIs. Required.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

        """
        super().__init__(**kwargs)

        self.domain = domain
        self.selector = selector

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            if not all([
                self.selector,
            ]):
                raise MissingRequiredArgumentError(argument="selector")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            self.res["selector"] = self.selector

            if self.domain:
                _spec["domain"] = self.domain
