from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


def _to_list_of_vm_dicts(vms):
    """
    Converts list on attribute bases vms (vm.name; vm.id) to list of dict
    """
    _vms = []
    for vm in vms:
        _vm = {}
        if vm.vm_id:
            _vm["id"] = vm.vm_id
        if vm.vm_name:
            _vm["name"] = vm.vm_name
        _vms.append(_vm)
    return _vms


class Plan(NamespacedResource, MTV):
    """
    MTV Plan Resource
    Args:
        vms (:
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
        vms=None,
        warm_migration=False,
        teardown=True,
    ):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace
        self.storage_map_name = storage_map_name
        self.storage_map_namespace = storage_map_namespace
        self.network_map_name = network_map_name
        self.network_map_namespace = network_map_namespace
        self.vms = vms
        self.warm_migration = warm_migration

    def to_dict(self):
        res = super()._base_body()
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
                    "vms": _to_list_of_vm_dicts(self.vms),
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
