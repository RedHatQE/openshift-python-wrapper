# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource, MissingRequiredArgumentError


class VolumeSnapshotClass(Resource):
    """
    VolumeSnapshotClass specifies parameters that a underlying storage system uses when creating a volume snapshot. A specific VolumeSnapshotClass is used by specifying its name in a VolumeSnapshot object. VolumeSnapshotClasses are non-namespaced
    """

    api_group: str = Resource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO

    def __init__(
        self,
        deletion_policy: Optional[str] = "",
        driver: Optional[str] = "",
        parameters: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            deletion_policy (str): deletionPolicy determines whether a VolumeSnapshotContent created
              through the VolumeSnapshotClass should be deleted when its bound
              VolumeSnapshot is deleted. Supported values are "Retain" and
              "Delete". "Retain" means that the VolumeSnapshotContent and its
              physical snapshot on underlying storage system are kept. "Delete"
              means that the VolumeSnapshotContent and its physical snapshot on
              underlying storage system are deleted. Required.

            driver (str): driver is the name of the storage driver that handles this
              VolumeSnapshotClass. Required.

            parameters (Dict[str, Any]): parameters is a key-value map with storage driver specific parameters
              for creating snapshots. These values are opaque to Kubernetes.

        """
        super().__init__(**kwargs)

        self.deletion_policy = deletion_policy
        self.driver = driver
        self.parameters = parameters

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.deletion_policy:
                raise MissingRequiredArgumentError(argument="self.deletion_policy")

            if not self.driver:
                raise MissingRequiredArgumentError(argument="self.driver")

            self.res["deletionPolicy"] = self.deletion_policy
            self.res["driver"] = self.driver

            if self.parameters:
                self.res["parameters"] = self.parameters

    # End of generated code
