# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):
    """
    Backup object.
    """

    api_group = NamespacedResource.ApiGroup.VELERO_IO

    def __init__(self, included_namespaces=None, excluded_resources=None, **kwargs):
        """
        Args:
            included_namespaces (list): Namespaces to include in the backup (optional).
                If unspecified, all namespaces are included.
            excluded_resources (list): Resources to exclude from the backup (optional).
                Resources may be shortcuts (e.g. 'po' for 'pods') or fully-qualified.
        """
        if not included_namespaces:
            raise ValueError("included_namespaces can't be None")

        super().__init__(**kwargs)
        self.included_namespaces = included_namespaces
        self.excluded_resources = excluded_resources

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "includedNamespaces": self.included_namespaces,
                    }
                }
            )

            if self.excluded_resources:
                self.res["spec"]["excludedResources"] = self.excluded_resources
