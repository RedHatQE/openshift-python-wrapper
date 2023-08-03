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
            #TODO
            included_namespaces (..): NamespacedResource dict/list to include in backup.
            excluded_resources (..): Update backup spec with excludedResources.
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
