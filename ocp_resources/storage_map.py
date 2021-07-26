from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class StorageMap(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) StorageMap object.

    Args:
        source_provider_name (str): MTV Source Provider CR name.
        source_provider_namespace (str): MTV Source Provider CR namespace.
        destination_provider_name (str): MTV Destination Provider CR name.
        destination_provider_namespace (str): MTV Destination Provider CR namespace.
        mapping (dict): Storage Resources Mapping
            Example:
                [ { "destination" : { "storageClass": "nfs",
                                      "accessMode": " ReadWriteMany",
                                      "volumeMode": "Filesystem" },
                    "source" : { "id": "datastore-11" }},

                  { "destination" : { "storageClass": "hss",
                                      "accessMode": " ReadWriteMany",
                                      "volumeMode": "Block" },
                    "source" : { "name": "MyDatastore" }},

                ]

    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name,
        namespace,
        source_provider_name=None,
        source_provider_namespace=None,
        destination_provider_name=None,
        destination_provider_namespace=None,
        mapping=None,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.mapping = mapping
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace
        self.condition_message_ready = self.ConditionMessage.STORAGE_MAP_READY

    def to_dict(self):
        res = super().to_dict()
        res.update(self.map_to_dict)
        return res
