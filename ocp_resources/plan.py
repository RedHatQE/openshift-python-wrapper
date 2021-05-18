from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class Plan(NamespacedResource, MTV):
    """
    Migration Tool for Virtualization (MTV) Plan Resource.

    Args:

        source_provider_name (str): mtv provider cr name.
        source_provider_namespace (str): mtv provider cr namespace.
        destination_provider_name (str): mtv destination cr name.
        destination_provider_namespace (str): mtv destination cr namespace.
        storage_map_name (str): mtv  storagemap cr name.
        storage_map_namespace (str): mtv storagemap cr namespace.
        network_map_name (str): mtv networkmap cr name.
        network_map_namespace (str): mtv networkmap cr namespace.
        virtual_machines_list (list): A List of dicts of vm ids and/or names.
        warm_migration (bool): Warm (true) or Cold (false) migration.
    """

    class StatusConditions:
        class CATEGORY:
            REQUIRED = "Required"

        class MESSAGE:
            PLAN_READY = "The migration plan is ready."

        class STATUS:
            TRUE = "True"

        class TYPE:
            READY = "Ready"

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name,
        namespace,
        source_provider_name=None,
        source_provider_namespace=None,
        destination_provider_name=None,
        destination_provider_namespace=None,
        storage_map_name=None,
        storage_map_namespace=None,
        network_map_name=None,
        network_map_namespace=None,
        virtual_machines_list=None,
        warm_migration=False,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
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

    def to_dict(self):
        res = super().to_dict()
        res.update(
            {
                "spec": {
                    "map": {
                        "storage": {
                            "name": self.storage_map_name,
                            "namespace": self.storage_map_namespace,
                        },
                        "network": {
                            "name": self.storage_map_name,
                            "namespace": self.storage_map_namespace,
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
            }
        )
        return res

    def wait_for_condition_ready(self):
        self.wait_for_resource_status(
            condition_message=Plan.StatusConditions.MESSAGE.PLAN_READY,
            condition_status=self.Condition.Status.TRUE,
            condition_type=self.Condition.READY,
        )
