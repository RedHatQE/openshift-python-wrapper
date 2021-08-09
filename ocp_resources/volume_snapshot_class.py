from ocp_resources.resource import Resource


class VolumeSnapshotClass(Resource):
    """
    VolumeSnapshotClass object.
    """

    api_group = Resource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO
