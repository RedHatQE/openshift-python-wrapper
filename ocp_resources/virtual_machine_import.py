# -*- coding: utf-8 -*-


from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler
from ocp_resources.virtual_machine import VirtualMachine


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
        if mapping.target_access_modes:
            mapping_dict["accessMode"] = mapping.target_access_modes
        if mapping.target_volume_mode:
            mapping_dict["volumeMode"] = mapping.target_volume_mode
        mappings_list.append(mapping_dict)
    return mappings_list


class VirtualMachineImport(NamespacedResource):
    """
    Virtual Machine Import object, inherited from NamespacedResource.
    """

    api_group = NamespacedResource.ApiGroup.V2V_KUBEVIRT_IO

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
        SECRET_NOT_FOUND = "SecretNotFound"  # pragma: allowlist secret
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
        name=None,
        namespace=None,
        provider_credentials_secret_name=None,
        provider_type=None,
        provider_credentials_secret_namespace=None,
        client=None,
        teardown=True,
        vm_id=None,
        vm_name=None,
        cluster_id=None,
        cluster_name=None,
        target_vm_name=None,
        start_vm=False,
        provider_mappings=None,
        resource_mapping_name=None,
        resource_mapping_namespace=None,
        warm=False,
        finalize_date=None,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
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
        self.provider_mappings = provider_mappings
        self.resource_mapping_name = resource_mapping_name
        self.resource_mapping_namespace = resource_mapping_namespace
        self.provider_type = provider_type
        self.warm = warm
        self.finalize_date = finalize_date

    @property
    def vm(self):
        return VirtualMachine(
            name=self.target_vm_name,
            namespace=self.namespace,
            client=self.client,
            privileged_client=self.privileged_client or self.client,
        )

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

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

        if self.warm:
            spec["warm"] = self.warm
        if self.finalize_date:
            spec["finalizeDate"] = self.finalize_date.strftime(
                format="%Y-%m-%dT%H:%M:%SZ"
            )

        provider_source = spec.setdefault("source", {}).setdefault(
            self.provider_type, {}
        )
        vm = provider_source.setdefault("vm", {})
        if self.vm_id:
            vm["id"] = self.vm_id
        if self.vm_name:
            vm["name"] = self.vm_name

        if self.cluster_id:
            vm.setdefault("cluster", {})["id"] = self.cluster_id
        if self.cluster_name:
            vm.setdefault("cluster", {})["name"] = self.cluster_name

        if self.provider_mappings:
            if self.provider_mappings.disk_mappings:
                mappings = _map_mappings(mappings=self.provider_mappings.disk_mappings)
                provider_source.setdefault("mappings", {}).setdefault(
                    "diskMappings", mappings
                )

            if self.provider_mappings.network_mappings:
                mappings = _map_mappings(
                    mappings=self.provider_mappings.network_mappings
                )
                provider_source.setdefault("mappings", {}).setdefault(
                    "networkMappings", mappings
                )

            if self.provider_mappings.storage_mappings:
                mappings = _map_mappings(
                    mappings=self.provider_mappings.storage_mappings
                )
                provider_source.setdefault("mappings", {}).setdefault(
                    "storageMappings", mappings
                )

        return res

    def wait(
        self,
        timeout=600,
        cond_reason=SucceededConditionReason.VIRTUAL_MACHINE_READY,
        cond_status=Condition.Status.TRUE,
        cond_type=Condition.SUCCEEDED,
    ):
        self.logger.info(
            f"Wait for {self.kind} {self.name} {cond_reason} condition to be {cond_status}"
        )
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.api.get,
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
                                self.logger.info(msg)
                                return
        except TimeoutExpiredError:
            raise TimeoutExpiredError(
                f"Last condition of {self.kind} {self.name} {last_condition.type} was "
                f"{last_condition.status} ({last_condition.reason}: {last_condition.message})"
            )


class ResourceMapping(NamespacedResource):
    """
    ResourceMapping object.
    """

    api_group = NamespacedResource.ApiGroup.V2V_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        mapping=None,
        client=None,
        teardown=True,
        yaml_file=None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            **kwargs,
        )
        self.mapping = mapping

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        for provider, mapping in self.mapping.items():
            res_provider_section = res.setdefault("spec", {}).setdefault(provider, {})
            if mapping.network_mappings is not None:
                res_provider_section.setdefault(
                    "networkMappings",
                    _map_mappings(mappings=mapping.network_mappings),
                )
            if mapping.storage_mappings is not None:
                res_provider_section.setdefault(
                    "storageMappings",
                    _map_mappings(mappings=mapping.storage_mappings),
                )

        return res
