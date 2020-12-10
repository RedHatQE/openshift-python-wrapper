from .resource import NamespacedResource


class VolumeSnapshot(NamespacedResource):
    """
    VolumeSnapshot object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO

    def __init__(
        self,
        name,
        namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )


class VolumeSnapshotClass(NamespacedResource):
    """
    VolumeSnapshotClass object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_STORAGE_K8S_IO

    def __init__(
        self,
        name,
        namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
