# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class Snapshot(NamespacedResource):
    """
    Snapshot is the Schema for the snapshots API
    """

    api_group: str = NamespacedResource.ApiGroup.APPSTUDIO_REDHAT_COM

    def __init__(
        self,
        application: str | None = None,
        artifacts: dict[str, Any] | None = None,
        components: list[Any] | None = None,
        display_description: str | None = None,
        display_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            application (str): Application is a reference to the name of an Application resource
              within the same namespace, which defines the target application
              for the Snapshot (when used with a Binding).

            artifacts (dict[str, Any]): Artifacts is a placeholder section for 'artifact links' we want to
              maintain to other AppStudio resources. See Environment API doc for
              details.

            components (list[Any]): Components field contains the sets of components to deploy as part of
              this snapshot.

            display_description (str): DisplayDescription is a user-visible, user definable description for
              the resource (and is not used for any functional behaviour)

            display_name (str): DisplayName is a user-visible, user-definable name for the resource
              (and is not used for any functional behaviour)

        """
        super().__init__(**kwargs)

        self.application = application
        self.artifacts = artifacts
        self.components = components
        self.display_description = display_description
        self.display_name = display_name

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.application is None:
                raise MissingRequiredArgumentError(argument="self.application")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["application"] = self.application

            if self.artifacts is not None:
                _spec["artifacts"] = self.artifacts

            if self.components is not None:
                _spec["components"] = self.components

            if self.display_description is not None:
                _spec["displayDescription"] = self.display_description

            if self.display_name is not None:
                _spec["displayName"] = self.display_name

    # End of generated code
