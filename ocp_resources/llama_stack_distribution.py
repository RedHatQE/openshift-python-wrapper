# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class LlamaStackDistribution(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.LLAMASTACK_IO

    def __init__(
        self,
        replicas: int | None = None,
        network: dict[str, Any] | None = None,
        server: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            replicas (int): No field description from API

            network (dict[str, Any]): Network defines network access controls for the LlamaStack service

            server (dict[str, Any]): ServerSpec defines the desired state of llama server.

        """
        super().__init__(**kwargs)

        self.replicas = replicas
        self.network = network
        self.server = server

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.server is None:
                raise MissingRequiredArgumentError(argument="self.server")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.network is not None:
                _spec["network"] = self.network
            _spec["server"] = self.server

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

    # End of generated code
