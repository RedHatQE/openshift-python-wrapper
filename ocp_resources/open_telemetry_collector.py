# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class OpenTelemetryCollector(NamespacedResource):
    """
    OpenTelemetryCollector is the Schema for the opentelemetrycollectors API
    """

    api_group: str = NamespacedResource.ApiGroup.OPENTELEMETRY_IO

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        management_state: str | None = None,
        mode: str | None = None,
        replicas: int | None = None,
        resources: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            config (dict[str, Any]): Required. Collector pipeline configuration.

            management_state (str): Required. Usually "Managed".

            mode (str): Deployment mode ("deployment", "daemonset", "sidecar").

            replicas (int): Number of collector replicas (when mode=deployment).

            resources (dict[str, Any]): Resource requests/limits.
        """
        super().__init__(**kwargs)

        self.config = config
        self.management_state = management_state
        self.mode = mode
        self.replicas = replicas
        self.resources = resources

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.config is None:
                raise MissingRequiredArgumentError(argument="self.config")

            if self.management_state is None:
                raise MissingRequiredArgumentError(argument="self.management_state")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["config"] = self.config
            _spec["managementState"] = self.management_state

            if self.mode is not None:
                _spec["mode"] = self.mode

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.resources is not None:
                _spec["resources"] = self.resources

    # End of generated code
