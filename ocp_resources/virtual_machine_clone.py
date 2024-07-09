# API reference: https://kubevirt.io/user-guide/operations/clone_api/

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource
from ocp_resources.virtual_machine import VirtualMachine


class VirtualMachineClone(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.CLONE_KUBEVIRT_IO

    def __init__(
        self,
        source_name=None,
        source_kind=None,
        target_name=None,
        label_filters=None,
        annotation_filters=None,
        new_mac_addresses=None,
        new_smbios_serial=None,
        **kwargs,
    ):
        """
        Create VirtualMachineClone object.

        Args:
            source_name (str): the clone's source name
            source_kind (str, optional): the clone's source type, default - VirtualMachine.kind
            target_name (str, optional): the clone's target name, default - randomly generated name
            label_filters (list, optional): List of label filters, e.g. ["*", "!someKey/*"]
            annotation_filters (list, optional): List of annotation filters, e.g. ["firstKey/*", "secondKey/*"]
            new_mac_addresses (dict, optional): Dict of new MAC addresses, {interface_name: mac_address}
            new_smbios_serial (str, optional): the clone's new smbios serial
        """
        super().__init__(**kwargs)
        self.source_name = source_name
        self.source_kind = source_kind
        self.target_name = target_name
        self.label_filters = label_filters
        self.annotation_filters = annotation_filters
        self.new_mac_addresses = new_mac_addresses
        self.new_smbios_serial = new_smbios_serial

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.source_name:
                raise MissingRequiredArgumentError(argument="source_name")
            spec = self.res.setdefault("spec", {})

            source = spec.setdefault("source", {})
            source["apiGroup"] = NamespacedResource.ApiGroup.KUBEVIRT_IO
            source["kind"] = self.source_kind if self.source_kind else VirtualMachine.kind
            source["name"] = self.source_name

            if self.target_name:
                target = spec.setdefault("target", {})
                target["apiGroup"] = NamespacedResource.ApiGroup.KUBEVIRT_IO
                target["kind"] = VirtualMachine.kind
                target["name"] = self.target_name

            if self.label_filters:
                spec["labelFilters"] = self.label_filters
            if self.annotation_filters:
                spec["annotationFilters"] = self.annotation_filters
            if self.new_mac_addresses:
                spec["newMacAddresses"] = self.new_mac_addresses
            if self.new_smbios_serial:
                spec["newSMBiosSerial"] = self.new_smbios_serial
