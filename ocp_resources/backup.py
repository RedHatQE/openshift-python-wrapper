# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any, List

from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):
    """
    Backup in 'velero' official API:
        https://velero.io/docs/main/api-types/backup/
    """

    api_group = NamespacedResource.ApiGroup.VELERO_IO

    def __init__(
        self,
        included_namespaces: List[str] | None = None,
        excluded_resources: List[str] | None = None,
        snapshot_move_data: bool = False,
        storage_location: str = "",
        **kwargs: Any,
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

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            spec_dict = self.res["spec"]

            if self.included_namespaces:
                spec_dict["includedNamespaces"] = self.included_namespaces

            if self.excluded_resources:
                spec_dict["excludedResources"] = self.excluded_resources

            if self.snapshot_move_data:
                spec_dict["snapshotMoveData"] = self.snapshot_move_data

            if self.storage_location:
                spec_dict["storageLocation"] = self.storage_location
