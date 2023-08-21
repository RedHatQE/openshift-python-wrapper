from ocp_resources.resource import NamespacedResource


class CatalogSource(NamespacedResource):
    """
    CatalogSource 'OLM' API official docs:
        https://olm.operatorframework.io/docs/concepts/crds/catalogsource/
    CatalogSource in Openshift docs:
        https://docs.openshift.com/container-platform/4.9/rest_api/operatorhub_apis/catalogsource-operators-coreos-com-v1alpha1.html
    """

    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        source_type=None,
        image=None,
        display_name=None,
        publisher=None,
        update_strategy_registry_poll_interval=None,
        **kwargs,
    ):
        """
        Args:
            source_type (str): Name of the source type, could be one of the following:
                grpc with an image reference: OLM pulls the image and runs the pod,
                    which is expected to serve a compliant API.
                grpc with an address field: OLM attempts to contact
                    the gRPC API at the given address. This should not be used in most cases.
                configmap: OLM parses config map data and runs a pod that can serve the gRPC API over it.
            image (str): Index image for the catalog.
            display_name (str): Display name for the catalog in the web console and CLI.
            publisher (str): Name of the publisher.
            update_strategy_registry_poll_interval (str): Time interval between checks of the latest
                catalog_source version. The catalog operator polls to see if a new version of the catalog source
                is available.
        """
        super().__init__(**kwargs)
        self.source_type = source_type
        self.image = image
        self.display_name = display_name
        self.publisher = publisher
        self.update_strategy_registry_poll_interval = (
            update_strategy_registry_poll_interval
        )

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "sourceType": self.source_type,
                        "image": self.image,
                        "displayName": self.display_name,
                        "publisher": self.publisher,
                    }
                }
            )
            if self.update_strategy_registry_poll_interval:
                self.res["spec"].update(
                    {
                        "updateStrategy": {
                            "registryPoll": {
                                "interval": self.update_strategy_registry_poll_interval,
                            },
                        },
                    }
                )
