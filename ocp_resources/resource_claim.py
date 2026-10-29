# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class ResourceClaim(NamespacedResource):
    """
    ResourceClaim describes a request for access to resources in the cluster, for use by workloads. For example, if a workload needs an accelerator device with specific properties, this is how that request is expressed. The status stanza tracks whether this claim has been satisfied and what specific resources have been allocated.
    """

    api_group: str = NamespacedResource.ApiGroup.RESOURCE_K8S_IO

    def __init__(
        self,
        devices: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            devices (dict[str, Any]): DeviceClaim defines how to request devices with a ResourceClaim.

        """
        super().__init__(**kwargs)

        self.devices = devices

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.devices is not None:
                _spec["devices"] = self.devices

    # End of generated code
