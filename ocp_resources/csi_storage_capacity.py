from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class CSIStorageCapacity(NamespacedResource):
    """
    CSIStorageCapacity object. API reference:
    https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/csi-storage-capacity-v1/#CSIStorageCapacity
    """

    api_group = NamespacedResource.ApiGroup.STORAGE_K8S_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        capacity=None,
        maximum_volume_size=None,
        node_topology=None,
        storage_class_name=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the CSIStorageCapacity resource
            namespace (str): Namespace of CSIStorageCapacity resource
            client: (DynamicClient): DynamicClient for api calls
            capacity (str, optional): value reported by the csi driver
            maximum_volume_size (str, optional): maximum volume size reported by csi driver
            storage_class_name (str): storage class name
            node_topology (dict, optional): defines which node has access to the storage for which capacity
            was reported
                Example:
                    node_topology: {'matchLabels': {'topology.hostpath.csi/node': 'c01-dbn-413-4c48b-worker-0-pmtv8'}}
            teardown (bool): Indicates if the resource should be torn down at the end
            privileged_client (DynamicClient): Privileged client for api calls
            yaml_file (str): yaml file for the resource.
            delete_timeout (int): timeout associated with delete action
        """
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
        self.capacity = capacity
        self.node_topology = node_topology
        self.storage_class_name = storage_class_name
        self.maximum_volume_size = maximum_volume_size

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if not self.storage_class_name:
                raise ValueError(
                    "yaml_file or parameter 'storage_class_name' is required."
                )
            self.res.update(
                {
                    "storageClassName": self.storage_class_name,
                }
            )
            if self.maximum_volume_size:
                self.res["maximumVolumeSize"] = self.maximum_volume_size
            if self.node_topology:
                self.res["nodeTopology"] = self.node_topology
            if self.capacity:
                self.res["capacity"] = self.capacity
