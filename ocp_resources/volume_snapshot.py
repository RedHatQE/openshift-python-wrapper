from ocp_resources.resource import NamespacedResource


class VolumeSnapshot(NamespacedResource):
    """
    VolumeSnapshot object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO


class VolumeSnapshotClass(NamespacedResource):
    """
    VolumeSnapshotClass object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO
