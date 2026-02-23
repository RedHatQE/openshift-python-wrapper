# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource

from typing import Any
from ocp_resources.resource import NamespacedResource
from ocp_resources.exceptions import MissingRequiredArgumentError

class LlamaStackDistribution(NamespacedResource):
    """
    
    """

    api_group: str = NamespacedResource.ApiGroup.LLAMASTACK_IO

    def __init__(
        self,
        network: dict[str, Any] | None = None,
        replicas: int | None = None,
        server: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            network (dict[str, Any]): Network defines network access controls for the LlamaStack service

            replicas (int): No field description from API

            server (dict[str, Any]): ServerSpec defines the desired state of llama server.

        """
        super().__init__(**kwargs)

        self.network = network
        self.replicas = replicas
        self.server = server

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.server is None:
                raise MissingRequiredArgumentError(argument="self.server")


            self.res["spec"] = {}
            _spec = self.res["spec"]


            _spec["server"] = self.server


            if self.network is not None:
                _spec["network"] = self.network

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

    # End of generated code
