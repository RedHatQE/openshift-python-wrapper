# -*- coding: utf-8 -*-

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


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

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            if not self.backup_name:
                raise MissingRequiredArgumentError(argument="backup_name")

            if not self.yaml_file:
                self.res.update({
                    "spec": {
                        "backupName": self.backup_name,
                    }
                })
                if self.included_namespaces:
                    self.res["spec"]["includedNamespaces"] = self.included_namespaces
