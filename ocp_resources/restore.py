# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class Restore(NamespacedResource):
    """
    Restore object.
    """

    api_group = NamespacedResource.ApiGroup.VELERO_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        included_namespaces=None,
        backup_name=None,
        client=None,
        teardown=False,
        privileged_client=None,
        yaml_file=None,
        **kwargs,
    ):
        if not backup_name:
            raise ValueError("backup_name can't be None")

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
        self.backup_name = backup_name

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res
        res.update(
            {
                "spec": {
                    "backupName": self.backup_name,
                }
            }
        )
        if self.included_namespaces:
            res["spec"]["includedNamespaces"] = self.included_namespaces
        return res
