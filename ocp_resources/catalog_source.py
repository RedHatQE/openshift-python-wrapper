from ocp_resources.resource import NamespacedResource


class CatalogSource(NamespacedResource):
    """
    CatalogSource 'OLM' API official docs:
        https://olm.operatorframework.io/docs/concepts/crds/catalogsource/
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
            source_type (str): Role name.
            image (DynamicClient): DynamicClient to use.
            display_name (list): list of dicts of rules. In the dict:
                permissions_to_resources (list): List of string with resource/s to which you want to add permissions to.
                Verbs (list): Determine the action/s (permissions) applicable on a specific resource.
                    Available verbs per resource can be seen with the command 'oc api-resources --sort-by name -o wide'
            publisher (bool, default: True): Indicates if this resource would need to be deleted.
            update_strategy_registry_poll_interval (yaml, default: None): yaml file for the resource.
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
