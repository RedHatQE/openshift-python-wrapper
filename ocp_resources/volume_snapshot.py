from ocp_resources.resource import NamespacedResource, Resource


class VolumeSnapshot(NamespacedResource):
    """
    VolumeSnapshot object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO


class VolumeSnapshotClass(Resource):
    """
    VolumeSnapshotClass object.
    """

    api_group = Resource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO
