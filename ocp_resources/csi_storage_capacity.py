from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class CSIStorageCapacity(NamespacedResource):
    """
    https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/csi-storage-capacity-v1/#CSIStorageCapacity
    """

    api_group = NamespacedResource.ApiGroup.STORAGE_K8S_IO

    def __init__(
        self,
        capacity=None,
        maximum_volume_size=None,
        node_topology=None,
        storage_class_name=None,
        **kwargs,
    ):
        """
        Args:
            capacity (str, optional): value reported by the csi driver
            maximum_volume_size (str, optional): maximum volume size reported by csi driver
            storage_class_name (str): storage class name
            node_topology (dict, optional): defines which node has access to the storage for which capacity
            was reported
                Example:
                    node_topology: {'matchLabels': {'topology.hostpath.csi/node': 'c01-dbn-413-4c48b-worker-0-pmtv8'}}
        """
        super().__init__(**kwargs)
        self.capacity = capacity
        self.node_topology = node_topology
        self.storage_class_name = storage_class_name
        self.maximum_volume_size = maximum_volume_size

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.storage_class_name:
                raise MissingRequiredArgumentError(argument="storage_class_name")
            self.res.update({
                "storageClassName": self.storage_class_name,
            })
            if self.maximum_volume_size:
                self.res["maximumVolumeSize"] = self.maximum_volume_size
            if self.node_topology:
                self.res["nodeTopology"] = self.node_topology
            if self.capacity:
                self.res["capacity"] = self.capacity
