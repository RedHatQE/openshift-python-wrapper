# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class PodMetrics(NamespacedResource):
    """
    PodMetrics sets resource usage metrics of a pod.
    """

    api_group: str = NamespacedResource.ApiGroup.METRICS_K8S_IO

    def __init__(
        self,
        containers: list[Any] | None = None,
        timestamp: str | None = None,
        window: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            containers (list[Any]): Metrics for all containers are collected within the same time window.

            timestamp (str): Time is a wrapper around time.Time which supports correct marshaling
              to YAML and JSON.  Wrappers are provided for many of the factory
              methods that the time package offers.

            window (str): Duration is a wrapper around time.Duration which supports correct
              marshaling to YAML and JSON. In particular, it marshals into
              strings, which can be used as map keys in json.

        """
        super().__init__(**kwargs)

        self.containers = containers
        self.timestamp = timestamp
        self.window = window

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.containers is None:
                raise MissingRequiredArgumentError(argument="self.containers")

            if self.timestamp is None:
                raise MissingRequiredArgumentError(argument="self.timestamp")

            if self.window is None:
                raise MissingRequiredArgumentError(argument="self.window")

            self.res["containers"] = self.containers
            self.res["timestamp"] = self.timestamp
            self.res["window"] = self.window

    # End of generated code
