from typing import Any

from ocp_resources.resource import NamespacedResource


class Provider(NamespacedResource):
    """
    Migration Toolkit For Virtualization (MTV) Provider object.
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        provider_type: str | None = None,
        url: str | None = None,
        secret_name: str | None = None,
        secret_namespace: str | None = None,
        vddk_init_image: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.provider_type = provider_type
        self.url = url
        self.secret_name = secret_name
        self.secret_namespace = secret_namespace
        self.vddk_init_image = vddk_init_image

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res.update({
                "spec": {
                    "type": self.provider_type,
                    "url": self.url,
                    "secret": {
                        "name": self.secret_name,
                        "namespace": self.secret_namespace,
                    },
                    "settings": {"vddkInitImage": self.vddk_init_image},
                }
            })
