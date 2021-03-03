import logging

from ocp_resources.resource import NamespacedResource


LOGGER = logging.getLogger(__name__)


class CatalogSource(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        name,
        namespace,
        client=None,
        source_type=None,
        image=None,
        display_name=None,
        publisher=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.source_type = source_type
        self.image = image
        self.display_name = display_name
        self.publisher = publisher

    def to_dict(self):
        res = super().to_dict()
        res.update(
            {
                "spec": {
                    "sourceType": self.source_type,
                    "image": self.image,
                    "displayName": self.display_name,
                    "publisher": self.publisher,
                }
            }
        )

        return res
