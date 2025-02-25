from typing import Any, Dict
from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class CatalogSource(NamespacedResource):
    """
    https://olm.operatorframework.io/docs/concepts/crds/catalogsource/
    """

    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        source_type: str = "",
        image: str = "",
        display_name: str = "",
        publisher: str = "",
        update_strategy_registry_poll_interval: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            source_type (str): Name of the source type.
            image (str): Image index for the catalog.
            display_name (str): Display name for the catalog in the web console and CLI.
            publisher (str): Name of the publisher.
            update_strategy_registry_poll_interval (str, optional): Time interval between checks of the latest
                catalog_source version.
        """
        super().__init__(**kwargs)
        self.source_type = source_type
        self.image = image
        self.display_name = display_name
        self.publisher = publisher
        self.update_strategy_registry_poll_interval = update_strategy_registry_poll_interval

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not all([self.source_type, self.image, self.display_name, self.publisher]):
                raise MissingRequiredArgumentError(argument="'source_type', 'image', 'display_name' and 'publisher'")

            self.res["spec"] = {
                "sourceType": self.source_type,
                "image": self.image,
                "displayName": self.display_name,
                "publisher": self.publisher,
            }
            _spec: Dict[str, Any] = self.res["spec"]

            if self.update_strategy_registry_poll_interval:
                _spec["updateStrategy"] = {"registryPoll": {"interval": self.update_strategy_registry_poll_interval}}
