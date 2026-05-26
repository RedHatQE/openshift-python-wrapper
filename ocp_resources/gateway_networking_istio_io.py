# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Gateway(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.NETWORKING_ISTIO_IO

    def __init__(
        self,
        selector: dict[str, Any] | None = None,
        servers: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            selector (dict[str, Any]): No field description from API

            servers (list[Any]): A list of server specifications.

        """
        super().__init__(**kwargs)

        self.selector = selector
        self.servers = servers

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.selector is not None:
                _spec["selector"] = self.selector

            if self.servers is not None:
                _spec["servers"] = self.servers

    # End of generated code
