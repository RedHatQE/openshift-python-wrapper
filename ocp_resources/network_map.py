from ocp_resources.utils.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class NetworkMap(NamespacedResource):
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
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.mapping = mapping
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace

    @property
    def map_to_dict(self):
        return {
            "spec": {
                "map": self.mapping,
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

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res.update(self.map_to_dict)
