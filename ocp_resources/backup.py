# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):
    """
    Backup object.
    """

    api_group = NamespacedResource.ApiGroup.VELERO_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        included_namespaces=None,
        client=None,
        teardown=False,
        privileged_client=None,
        yaml_file=None,
        excluded_resources=None,
        **kwargs,
    ):
        if not included_namespaces:
            raise ValueError("included_namespaces can't be None")

        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            **kwargs,
        )
        self.included_namespaces = included_namespaces
        self.excluded_resources = excluded_resources

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res
        res.update(
            {
                "spec": {
                    "includedNamespaces": self.included_namespaces,
                }
            }
        )

        if self.excluded_resources:
            res["spec"]["excludedResources"] = self.excluded_resources
        return res
