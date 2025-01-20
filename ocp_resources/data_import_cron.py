# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from __future__ import annotations
from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource

from typing import Any


class DataImportCron(NamespacedResource):
    """
    DataImportCron defines a cron job for recurring polling/importing disk images as PVCs into a golden image namespace
    """

    api_group: str = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        garbage_collect: str | None = None,
        imports_to_keep: int | None = None,
        managed_data_source: str | None = None,
        retention_policy: str | None = None,
        schedule: str | None = None,
        template: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            garbage_collect (str): GarbageCollect specifies whether old PVCs should be cleaned up after a
              new PVC is imported. Options are currently "Outdated" and "Never",
              defaults to "Outdated".

            imports_to_keep (int): Number of import PVCs to keep when garbage collecting. Default is 3.

            managed_data_source (str): ManagedDataSource specifies the name of the corresponding DataSource
              this cron will manage. DataSource has to be in the same namespace.

            retention_policy (str): RetentionPolicy specifies whether the created DataVolumes and
              DataSources are retained when their DataImportCron is deleted.
              Default is RatainAll.

            schedule (str): Schedule specifies in cron format when and how often to look for new
              imports

            template (dict[str, Any]): Template specifies template for the DVs to be created

        """
        super().__init__(**kwargs)

        self.garbage_collect = garbage_collect
        self.imports_to_keep = imports_to_keep
        self.managed_data_source = managed_data_source
        self.retention_policy = retention_policy
        self.schedule = schedule
        self.template = template

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.managed_data_source is None:
                raise MissingRequiredArgumentError(argument="self.managed_data_source")

            if self.schedule is None:
                raise MissingRequiredArgumentError(argument="self.schedule")

            if self.template is None:
                raise MissingRequiredArgumentError(argument="self.template")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["managedDataSource"] = self.managed_data_source
            _spec["schedule"] = self.schedule
            _spec["template"] = self.template

            if self.garbage_collect is not None:
                _spec["garbageCollect"] = self.garbage_collect

            if self.imports_to_keep is not None:
                _spec["importsToKeep"] = self.imports_to_keep

            if self.retention_policy is not None:
                _spec["retentionPolicy"] = self.retention_policy

    # End of generated code
