# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class ModelRegistry(Resource):
    """
    ModelRegistry is the Schema for the modelregistries API
    """

    api_group: str = Resource.ApiGroup.COMPONENTS_PLATFORM_OPENDATAHUB_IO

    def __init__(
        self,
        dev_flags: dict[str, Any] | None = None,
        registries_namespace: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            dev_flags (dict[str, Any]): Add developer fields

            registries_namespace (str): Namespace for model registries to be installed, configurable only once
              when model registry is enabled, defaults to "rhoai-model-
              registries"

        """
        super().__init__(**kwargs)

        self.dev_flags = dev_flags
        self.registries_namespace = registries_namespace

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.dev_flags is not None:
                _spec["devFlags"] = self.dev_flags

            if self.registries_namespace is not None:
                _spec["registriesNamespace"] = self.registries_namespace

    # End of generated code
