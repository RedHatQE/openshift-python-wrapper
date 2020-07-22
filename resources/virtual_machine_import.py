# -*- coding: utf-8 -*-


import logging

from urllib3.exceptions import ProtocolError

from .resource import NamespacedResource
from .utils import TimeoutExpiredError, TimeoutSampler
from .virtual_machine import VirtualMachine


LOGGER = logging.getLogger(__name__)


def _map_mappings(mappings):
    mappings_list = []
    for mapping in mappings:
        mapping_dict = {"target": {"name": mapping.target_name}}
        if mapping.target_namespace:
            mapping_dict["target"]["namespace"] = mapping.target_namespace
        if mapping.target_type:
            mapping_dict["type"] = mapping.target_type
        if mapping.source_id:
            mapping_dict.setdefault("source", {})["id"] = mapping.source_id
        if mapping.source_name:
            mapping_dict.setdefault("source", {})["name"] = mapping.source_name
        mappings_list.append(mapping_dict)
    return mappings_list


class VirtualMachineImport(NamespacedResource):
    """
    Virtual Machine Import object, inherited from NamespacedResource.
    """

    api_group = "v2v.kubevirt.io"

    class Condition(NamespacedResource.Condition):
        SUCCEEDED = "Succeeded"
        VALID = "Valid"
        MAPPING_RULES_VERIFIED = "MappingRulesVerified"
        PROCESSING = "Processing"

    class ValidConditionReason:
        """
        Valid condition reason object
        """

        VALIDATION_COMPLETED = "ValidationCompleted"
        SECRET_NOT_FOUND = "SecretNotFound"
        RESOURCE_MAPPING_NOT_FOUND = "ResourceMappingNotFound"
        UNINITIALIZED_PROVIDER = "UninitializedProvider"
        SOURCE_VM_NOT_FOUND = "SourceVMNotFound"
        INCOMPLETE_MAPPING_RULES = "IncompleteMappingRules"

    class MappingRulesConditionReason:
        """
        Mapping rules verified condition reason object
        """

        MAPPING_COMPLETED = "MappingRulesVerificationCompleted"
        MAPPING_FAILED = "MappingRulesVerificationFailed"
        MAPPING_REPORTED_WARNINGS = "MappingRulesVerificationReportedWarnings"

    class ProcessingConditionReason:
        """
        Processing condition reason object
        """

        CREATING_TARGET_VM = "CreatingTargetVM"
        COPYING_DISKS = "CopyingDisks"
        COMPLETED = "ProcessingCompleted"
        FAILED = "ProcessingFailed"

    class SucceededConditionReason:
        """
        Succeeced cond reason object
        """

        VALIDATION_FAILED = "ValidationFailed"
        VM_CREATION_FAILED = "VMCreationFailed"
        DATAVOLUME_CREATION_FAILED = "DataVolumeCreationFailed"
        VIRTUAL_MACHINE_READY = "VirtualMachineReady"
        VIRTUAL_MACHINE_RUNNING = "VirtualMachineRunning"
        VMTEMPLATE_MATCHING_FAILED = "VMTemplateMatchingFailed"

    def __init__(
        self,
        name,
        namespace,
        provider_credentials_secret_name,
        provider_credentials_secret_namespace=None,
        client=None,
        teardown=True,
        vm_id=None,
        vm_name=None,
        cluster_id=None,
        cluster_name=None,
        target_vm_name=None,
        start_vm=False,
        ovirt_mappings=None,
        resource_mapping_name=None,
        resource_mapping_namespace=None,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.vm_id = vm_id
        self.vm_name = vm_name
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.target_vm_name = target_vm_name
        self.start_vm = start_vm
        self.provider_credentials_secret_name = provider_credentials_secret_name
        self.provider_credentials_secret_namespace = (
            provider_credentials_secret_namespace
        )
        self.ovirt_mappings = ovirt_mappings
        self.resource_mapping_name = resource_mapping_name
        self.resource_mapping_namespace = resource_mapping_namespace

    @property
    def vm(self):
        return VirtualMachine(name=self.target_vm_name, namespace=self.namespace)

    def to_dict(self):
        res = super().to_dict()
        spec = res.setdefault("spec", {})

        secret = spec.setdefault("providerCredentialsSecret", {})
        secret["name"] = self.provider_credentials_secret_name

        if self.provider_credentials_secret_namespace:
            secret["namespace"] = self.provider_credentials_secret_namespace

        if self.resource_mapping_name:
            spec.setdefault("resourceMapping", {})["name"] = self.resource_mapping_name
        if self.resource_mapping_namespace:
            spec.setdefault("resourceMapping", {})[
                "namespace"
            ] = self.resource_mapping_namespace

        if self.target_vm_name:
            spec["targetVmName"] = self.target_vm_name

        if self.start_vm is not None:
            spec["startVm"] = self.start_vm

        ovirt = spec.setdefault("source", {}).setdefault("ovirt", {})

        vm = ovirt.setdefault("vm", {})
        if self.vm_id:
            vm["id"] = self.vm_id
        if self.vm_name:
            vm["name"] = self.vm_name

        if self.cluster_id:
            vm.setdefault("cluster", {})["id"] = self.cluster_id
        if self.cluster_name:
            vm.setdefault("cluster", {})["name"] = self.cluster_name

        if self.ovirt_mappings:
            if self.ovirt_mappings.disk_mappings:
                mappings = _map_mappings(mappings=self.ovirt_mappings.disk_mappings)
                ovirt.setdefault("mappings", {}).setdefault("diskMappings", mappings)

            if self.ovirt_mappings.network_mappings:
                mappings = _map_mappings(mappings=self.ovirt_mappings.network_mappings)
                ovirt.setdefault("mappings", {}).setdefault("networkMappings", mappings)

            if self.ovirt_mappings.storage_mappings:
                mappings = _map_mappings(mappings=self.ovirt_mappings.storage_mappings)
                ovirt.setdefault("mappings", {}).setdefault("storageMappings", mappings)

        return res

    def wait(
        self,
        timeout=600,
        cond_reason=SucceededConditionReason.VIRTUAL_MACHINE_READY,
        cond_status=Condition.Status.TRUE,
        cond_type=Condition.SUCCEEDED,
    ):
        LOGGER.info(
            f"Wait for {self.kind} {self.name} {cond_reason} condition to be {cond_status}"
        )
        samples = TimeoutSampler(
            timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        last_condition = None
        try:
            for sample in samples:
                if sample.items:
                    sample_status = sample.items[0].status
                    if sample_status:
                        current_conditions = sample_status.conditions
                        for cond in current_conditions:
                            last_condition = cond
                            if (
                                cond.type == cond_type
                                and cond.status == cond_status
                                and cond.reason == cond_reason
                            ):
                                msg = (
                                    f"Status of {self.kind} {self.name} {cond.type} is "
                                    f"{cond.status} ({cond.reason}: {cond.message})"
                                )
                                LOGGER.info(msg)
                                return
        except TimeoutExpiredError:
            msg = (
                f"Last condition of {self.kind} {self.name} {last_condition.type} was "
                f"{last_condition.status} ({last_condition.reason}: {last_condition.message})"
            )
            LOGGER.error(msg)
            raise


class OvirtMappings:
    def __init__(
        self, disk_mappings=None, network_mappings=None, storage_mappings=None
    ):
        self.disk_mappings = disk_mappings
        self.network_mappings = network_mappings
        self.storage_mappings = storage_mappings


class ResourceMappingItem:
    def __init__(
        self,
        target_name,
        target_namespace=None,
        target_type=None,
        source_name=None,
        source_id=None,
    ):
        self.target_name = target_name
        self.target_namespace = target_namespace
        self.source_name = source_name
        self.source_id = source_id
        self.target_type = target_type
