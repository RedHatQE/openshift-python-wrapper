from ocp_resources.resource import Resource


class VolumeSnapshotContent(Resource):
    """
    VolumeSnapshotContent object. API reference:
    https://docs.openshift.com/container-platform/4.11/rest_api/storage_apis/volumesnapshotcontent-snapshot-storage-k8s-io-v1.html
    """

    api_group = Resource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO
