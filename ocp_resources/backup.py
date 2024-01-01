# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):
    """
    Backup in 'velero' official API:
        https://velero.io/docs/main/api-types/backup/
    """

    api_group = NamespacedResource.ApiGroup.VELERO_IO

    def __init__(
        self,
        included_namespaces=None,
        excluded_resources=None,
        snapshot_move_data=False,
        storage_location=None,
        **kwargs,
    ):
        """
        Args:
            included_namespaces (list, optional): Namespaces to include in the backup.
                If unspecified, all namespaces are included.
            excluded_resources (list, optional): Resources to exclude from the backup.
                Resources may be shortcuts (e.g. 'po' for 'pods') or fully-qualified.
            snapshot_move_data (bool, optional): If set to true, deploys the volume snapshot mover
                controller and a modified CSI Data Mover plugin.
            storage_location (string, optional): Define the location for the DataMover.
        """
        super().__init__(**kwargs)
        self.included_namespaces = included_namespaces
        self.excluded_resources = excluded_resources
        self.snapshot_move_data = snapshot_move_data
        self.storage_location = storage_location

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            spec_dict = {}
            if self.included_namespaces:
                spec_dict.update({"includedNamespaces": self.included_namespaces})
            if self.excluded_resources:
                spec_dict.update({"excludedResources": self.excluded_resources})
            if self.snapshot_move_data:
                spec_dict.update({"snapshotMoveData": self.snapshot_move_data})
            if self.storage_location:
                spec_dict.update({"storageLocation": self.storage_location})
            if spec_dict:
                self.res.update({"spec": spec_dict})
