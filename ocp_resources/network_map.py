from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class NetworkMap(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) NetworkMap object.

    Args:
        source_provider_name (str): MTV Source Provider CR name.
        source_provider_namespace (str): MTV Source Provider CR namespace.
        destination_provider_name (str): MTV Destination Provider CR name.
        destination_provider_namespace (str): MTV Destination Provider CR namespace.
        mapping (dict): Storage Resources Mapping
            Exaple:
                [ { "destination" : { "type": "pod",
                    "source" : { "id": "network-13" }},

                  { "destination" : { "name": "nad_cr_name",
                                      "namespace": "nad_cr_namespace",
                                      "type": "multus"},
                    "source" : { "name": "VM Netowrk" }},

                ]
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        mapping=None,
        source_provider_name=None,
        source_provider_namespace=None,
        destination_provider_name=None,
        destination_provider_namespace=None,
        client=None,
        teardown=True,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.mapping = mapping
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace
        self.condition_message_ready = self.ConditionMessage.NETWORK_MAP_READY

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res.update(self.map_to_dict)
        return res
