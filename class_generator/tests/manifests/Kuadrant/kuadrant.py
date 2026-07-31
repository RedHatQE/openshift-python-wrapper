# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Kuadrant(NamespacedResource):
    """
    Kuadrant configures installations of Kuadrant Service Protection components
    """

    api_group: str = NamespacedResource.ApiGroup.KUADRANT_IO

    def __init__(
        self,
        components: dict[str, Any] | None = None,
        mtls: dict[str, Any] | None = None,
        observability: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            components (dict[str, Any]): Components configures optional Kuadrant components

            mtls (dict[str, Any]): MTLS is an optional entry which when enabled is set to true, kuadrant-
              operator will add the configuration required to enable mTLS
              between an Istio provided gateway and the Kuadrant components.

            observability (dict[str, Any]): Observability configures telemetry and monitoring settings for
              Kuadrant components. When enabled, it configures logging, tracing,
              and other observability features for both the control plane and
              data plane components.

        """
        super().__init__(**kwargs)

        self.components = components
        self.mtls = mtls
        self.observability = observability

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.components is not None:
                _spec["components"] = self.components

            if self.mtls is not None:
                _spec["mtls"] = self.mtls

            if self.observability is not None:
                _spec["observability"] = self.observability

    # End of generated code
