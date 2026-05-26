# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Jaeger(NamespacedResource):
    """
    Jaeger is the Schema for the jaegers.jaegertracing.io API
    """

    api_group: str = NamespacedResource.ApiGroup.JAEGERTRACING_IO

    def __init__(
        self,
        strategy: str | None = None,
        ingress: dict[str, Any] | None = None,
        collector: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            strategy (str): Jaeger deployment strategy ("allInOne" or "production").
            ingress (dict[str, Any]): Optional ingress settings for Jaeger UI.
            collector (dict[str, Any]): Optional collector configuration.
        """
        super().__init__(**kwargs)
        self.strategy = strategy
        self.ingress = ingress
        self.collector = collector

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]
            if self.strategy is not None:
                _spec["strategy"] = self.strategy
            if self.ingress is not None:
                _spec["ingress"] = self.ingress
            if self.collector is not None:
                _spec["collector"] = self.collector

    # End of generated code
