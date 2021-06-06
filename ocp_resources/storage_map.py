from ocp_resources.mtv import MTV
from ocp_resources.network_map import NetworkMap
from ocp_resources.resource import NamespacedResource


# TODO delete irrelevant imports


class StorageMap(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) storagemap wrapper.
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(self, name, namespace, map=None, provider=None):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.map = map
        self.provider = provider

    def to_dict(self):
        res = super().to_dict()
        res.update({"spec": {"map": self.map, "provider": self.provider}})

        return res

    def wait_for_condition_ready(self):
        self.wait_for_resource_status(
            condition_status=NamespacedResource.Condition.Status.TRUE,
            condition_type=NamespacedResource.Condition.READY,
        )
