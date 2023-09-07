# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):
    """
    Backup in 'velero' official API:
        https://velero.io/docs/v0.7.1/api-types/backup/
    """

    api_group = NamespacedResource.ApiGroup.VELERO_IO

    def __init__(self, included_namespaces=None, excluded_resources=None, **kwargs):
        """
        Args:
            included_namespaces (list, optional): Namespaces to include in the backup.
                If unspecified, all namespaces are included.
            excluded_resources (list, optional): Resources to exclude from the backup.
                Resources may be shortcuts (e.g. 'po' for 'pods') or fully-qualified.
        """
        super().__init__(**kwargs)
        self.included_namespaces = included_namespaces
        self.excluded_resources = excluded_resources

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            spec_dict = {}
            if self.included_namespaces:
                spec_dict.update({"includedNamespaces": self.included_namespaces})
            if self.excluded_resources:
                spec_dict.update({"excludedResources": self.excluded_resources})
            if spec_dict:
                self.res.update({"spec": spec_dict})
