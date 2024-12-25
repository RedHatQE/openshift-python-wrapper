from __future__ import annotations
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
        **kwargs,
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

    def _generate_hook_spec(self, hook_name: str, hook_namespace: str, hook_type: str) -> dict[str, Any]:
        return {
            "hook": {
                "name": hook_name,
                "namespace": hook_namespace,
            },
            "step": hook_type,
        }
