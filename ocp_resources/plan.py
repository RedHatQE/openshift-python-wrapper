from typing import Any

from ocp_resources.resource import NamespacedResource


class Plan(NamespacedResource):
    """
    Migration Tool for Virtualization (MTV) Plan Resource.

    Args:
        source_provider_name (str): MTV Source Provider CR name.
        source_provider_namespace (str): MTV Source Provider CR namespace.
        destination_provider_name (str): MTV Destination Provider CR name.
        destination_provider_namespace (str): MTV Destination Provider CR namespace.
        storage_map_name (str): MTV StorageMap CR name.
        storage_map_namespace (str): MTV StorageMap CR namespace.
        network_map_name (str): MTV NetworkMap CR name.
        network_map_namespace (str): MTV NetworkMap CR CR namespace.
        virtual_machines_list (list): A List of dicts, each contain
                                      the Name Or Id of the source Virtual Machines to migrate.
                                      Example: [ { "id": "vm-id-x" }, { "name": "vm-name-x" } ]
        warm_migration (bool, default: False): Warm (True) or Cold (False) migration.
        type (str, optional): Migration type. Valid values: "cold", "warm", "live", "conversion".
        pvc_name_template_use_generate_name (bool, optional): Whether to use generateName for PVC name templates.
        pvc_name_template (str, optional): Template for generating PVC names.
        volume_name_template (str, optional): Template for generating volume interface names in the target VM.
        network_name_template (str, optional): Template for generating network interface names in the target VM.
        skip_guest_conversion (bool, optional): Whether to skip guest conversion.
        target_power_state (str, optional): Specifies the desired power state of the target VM after migration.
                                          - "on": Target VM will be powered on after migration
                                          - "off": Target VM will be powered off after migration
                                          - "auto" or None (default): Target VM will match the source VM's power state
        use_compatibility_mode (bool, optional): Whether to use compatibility mode.
        migrate_shared_disks (bool, optional): Whether to migrate shared disks.
        preserve_static_ips (bool, optional): Whether to preserve static IPs during migration.
        target_node_selector (dict, optional): Node selector for the target VM. Specifies which node labels
                                             should be used for NodeSelector parameter of VMI resource.
        target_labels (dict, optional): Labels to be applied to the target VM. Specifies which labels
                                      should be added to the target VM resource.
        target_affinity (dict, optional): Affinity rules for the target VM. Specifies which affinity
                                        rules should be applied to the target VM resource.
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        source_provider_name: str | None = None,
        source_provider_namespace: str | None = None,
        destination_provider_name: str | None = None,
        destination_provider_namespace: str | None = None,
        storage_map_name: str | None = None,
        storage_map_namespace: str | None = None,
        network_map_name: str | None = None,
        network_map_namespace: str | None = None,
        virtual_machines_list: list[Any] | None = None,
        target_namespace: str | None = None,
        warm_migration: bool = False,
        pre_hook_name: str | None = None,
        pre_hook_namespace: str | None = None,
        after_hook_name: str | None = None,
        after_hook_namespace: str | None = None,
        type: str | None = None,
        pvc_name_template_use_generate_name: bool | None = None,
        pvc_name_template: str | None = None,
        volume_name_template: str | None = None,
        network_name_template: str | None = None,
        skip_guest_conversion: bool | None = None,
        target_power_state: str | None = None,
        use_compatibility_mode: bool | None = None,
        migrate_shared_disks: bool | None = None,
        preserve_static_ips: bool | None = None,
        target_node_selector: dict[str, str] | None = None,
        target_labels: dict[str, str] | None = None,
        target_affinity: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace
        self.storage_map_name = storage_map_name
        self.storage_map_namespace = storage_map_namespace
        self.network_map_name = network_map_name
        self.network_map_namespace = network_map_namespace
        self.virtual_machines_list = virtual_machines_list
        self.warm_migration = warm_migration
        self.pre_hook_name = pre_hook_name
        self.pre_hook_namespace = pre_hook_namespace
        self.after_hook_name = after_hook_name
        self.after_hook_namespace = after_hook_namespace
        self.target_namespace = target_namespace or self.namespace
        self.hooks_array = []
        self.type = type
        self.pvc_name_template_use_generate_name = pvc_name_template_use_generate_name
        self.pvc_name_template = pvc_name_template
        self.volume_name_template = volume_name_template
        self.network_name_template = network_name_template
        self.skip_guest_conversion = skip_guest_conversion
        self.target_power_state = target_power_state
        self.use_compatibility_mode = use_compatibility_mode
        self.migrate_shared_disks = migrate_shared_disks
        self.preserve_static_ips = preserve_static_ips
        self.target_node_selector = target_node_selector
        self.target_labels = target_labels
        self.target_affinity = target_affinity

        if self.pre_hook_name and self.pre_hook_namespace:
            self.hooks_array.append(
                self._generate_hook_spec(
                    hook_name=self.pre_hook_name,
                    hook_namespace=self.pre_hook_namespace,
                    hook_type="PreHook",
                )
            )

        if self.after_hook_name and self.after_hook_namespace:
            self.hooks_array.append(
                self._generate_hook_spec(
                    hook_name=self.after_hook_name,
                    hook_namespace=self.after_hook_namespace,
                    hook_type="AfterHook",
                )
            )

        if self.hooks_array and self.virtual_machines_list:
            for vm in self.virtual_machines_list:
                vm["hooks"] = self.hooks_array

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res.update({
                "spec": {
                    "warm": self.warm_migration,
                    "targetNamespace": self.target_namespace,
                    "map": {
                        "storage": {
                            "name": self.storage_map_name,
                            "namespace": self.storage_map_namespace,
                        },
                        "network": {
                            "name": self.network_map_name,
                            "namespace": self.network_map_namespace,
                        },
                    },
                    "vms": self.virtual_machines_list,
                    "provider": {
                        "source": {
                            "name": self.source_provider_name,
                            "namespace": self.source_provider_namespace,
                        },
                        "destination": {
                            "name": self.destination_provider_name,
                            "namespace": self.destination_provider_namespace,
                        },
                    },
                }
            })

            # Add optional fields if they are set
            spec = self.res["spec"]

            if self.type is not None:
                spec["type"] = self.type

            if self.pvc_name_template_use_generate_name is not None:
                spec["pvcNameTemplateUseGenerateName"] = self.pvc_name_template_use_generate_name

            if self.pvc_name_template is not None:
                spec["pvcNameTemplate"] = self.pvc_name_template

            if self.volume_name_template is not None:
                spec["volumeNameTemplate"] = self.volume_name_template

            if self.network_name_template is not None:
                spec["networkNameTemplate"] = self.network_name_template

            if self.skip_guest_conversion is not None:
                spec["skipGuestConversion"] = self.skip_guest_conversion

            if self.target_power_state is not None:
                spec["targetPowerState"] = self.target_power_state

            if self.use_compatibility_mode is not None:
                spec["useCompatibilityMode"] = self.use_compatibility_mode

            if self.migrate_shared_disks is not None:
                spec["migrateSharedDisks"] = self.migrate_shared_disks

            if self.preserve_static_ips is not None:
                spec["preserveStaticIPs"] = self.preserve_static_ips

            if self.target_node_selector is not None:
                spec["targetNodeSelector"] = self.target_node_selector

            if self.target_labels is not None:
                spec["targetLabels"] = self.target_labels

            if self.target_affinity is not None:
                spec["targetAffinity"] = self.target_affinity

    def _generate_hook_spec(self, hook_name: str, hook_namespace: str, hook_type: str) -> dict[str, Any]:
        return {
            "hook": {
                "name": hook_name,
                "namespace": hook_namespace,
            },
            "step": hook_type,
        }
