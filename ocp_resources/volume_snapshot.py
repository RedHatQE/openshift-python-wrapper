# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class VolumeSnapshot(NamespacedResource):
    """
    VolumeSnapshot is a user's request for either creating a point-in-time snapshot of a persistent volume, or binding to a pre-existing snapshot.
    """

    api_group: str = NamespacedResource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO

    def __init__(
        self,
        source: Optional[Dict[str, Any]] = None,
        volume_snapshot_class_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            source (Dict[str, Any]): source specifies where a snapshot will be created from. This field is
              immutable after creation. Required.

            volume_snapshot_class_name (str): VolumeSnapshotClassName is the name of the VolumeSnapshotClass
              requested by the VolumeSnapshot. VolumeSnapshotClassName may be
              left nil to indicate that the default SnapshotClass should be
              used. A given cluster may have multiple default Volume
              SnapshotClasses: one default per CSI Driver. If a VolumeSnapshot
              does not specify a SnapshotClass, VolumeSnapshotSource will be
              checked to figure out what the associated CSI Driver is, and the
              default VolumeSnapshotClass associated with that CSI Driver will
              be used. If more than one VolumeSnapshotClass exist for a given
              CSI Driver and more than one have been marked as default,
              CreateSnapshot will fail and generate an event. Empty string is
              not allowed for this field.

        """
        super().__init__(**kwargs)

        self.source = source
        self.volume_snapshot_class_name = volume_snapshot_class_name

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.source:
                raise MissingRequiredArgumentError(argument="self.source")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["source"] = self.source

            if self.volume_snapshot_class_name is not None:
                _spec["volumeSnapshotClassName"] = self.volume_snapshot_class_name

    # End of generated code
