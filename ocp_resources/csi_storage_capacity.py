from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class CSIStorageCapacity(NamespacedResource):
    """
    CSIStorageCapacity object. API reference:
    https://docs.openshift.com/container-platform/4.12/rest_api/storage_apis/storage-apis-index.html#csistoragecapacity-storage-k8s-iov1
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
            name (str): Name of the endpoints resource
            namespace (str): Namespace of endpoints resource
            client: (DynamicClient): DynamicClient for api calls
            capacity (str): value reported by the csi driver
            maximum_volume_size (str): maximum volume size reported by csi driver
            storage_class_name (str): storage class name
            node_topology (object): defines which node has access to the storage for which capacity was reported
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
            self.res.update(
                {
                    "maximumVolumeSize": self.maximum_volume_size,
                    "nodeTopology": self.node_topology,
                    "storageClassName": self.storage_class_name,
                    "capacity": self.capacity,
                }
            )
