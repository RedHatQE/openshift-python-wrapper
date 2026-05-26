# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, Resource


class ClusterUserDefinedNetwork(Resource):
    """
    ClusterUserDefinedNetwork describe network request for a shared network across namespaces.
    """

    api_group: str = Resource.ApiGroup.K8S_OVN_ORG

    def __init__(
        self,
        namespace_selector: dict[str, Any] | None = None,
        network: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            namespace_selector (dict[str, Any]): NamespaceSelector Label selector for which namespace network should be
              available for.

            network (dict[str, Any]): Network is the user-defined-network spec

        """
        super().__init__(**kwargs)

        self.namespace_selector = namespace_selector
        self.network = network

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.namespace_selector is None:
                raise MissingRequiredArgumentError(argument="self.namespace_selector")

            if self.network is None:
                raise MissingRequiredArgumentError(argument="self.network")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["namespaceSelector"] = self.namespace_selector
            _spec["network"] = self.network

    # End of generated code
