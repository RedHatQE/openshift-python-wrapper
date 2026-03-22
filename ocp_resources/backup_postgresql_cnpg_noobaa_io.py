# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class Backup(NamespacedResource):
    """
    A Backup resource is a request for a PostgreSQL backup by the user.
    """

    api_group: str = NamespacedResource.ApiGroup.POSTGRESQL_CNPG_NOOBAA_IO

    def __init__(
        self,
        cluster: dict[str, Any] | None = None,
        method: str | None = None,
        online: bool | None = None,
        online_configuration: dict[str, Any] | None = None,
        plugin_configuration: dict[str, Any] | None = None,
        target: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            cluster (dict[str, Any]): The cluster to backup

            method (str): The backup method to be used, possible options are
              `barmanObjectStore`, `volumeSnapshot` or `plugin`. Defaults to:
              `barmanObjectStore`.

            online (bool): Whether the default type of backup with volume snapshots is online/hot
              (`true`, default) or offline/cold (`false`) Overrides the default
              setting specified in the cluster field
              '.spec.backup.volumeSnapshot.online'

            online_configuration (dict[str, Any]): Configuration parameters to control the online/hot backup with volume
              snapshots Overrides the default settings specified in the cluster
              '.backup.volumeSnapshot.onlineConfiguration' stanza

            plugin_configuration (dict[str, Any]): Configuration parameters passed to the plugin managing this backup

            target (str): The policy to decide which instance should perform this backup. If
              empty, it defaults to `cluster.spec.backup.target`. Available
              options are empty string, `primary` and `prefer-standby`.
              `primary` to have backups run always on primary instances,
              `prefer-standby` to have backups run preferably on the most
              updated standby, if available.

        """
        super().__init__(**kwargs)

        self.cluster = cluster
        self.method = method
        self.online = online
        self.online_configuration = online_configuration
        self.plugin_configuration = plugin_configuration
        self.target = target

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.cluster is None:
                raise MissingRequiredArgumentError(argument="self.cluster")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["cluster"] = self.cluster

            if self.method is not None:
                _spec["method"] = self.method

            if self.online is not None:
                _spec["online"] = self.online

            if self.online_configuration is not None:
                _spec["onlineConfiguration"] = self.online_configuration

            if self.plugin_configuration is not None:
                _spec["pluginConfiguration"] = self.plugin_configuration

            if self.target is not None:
                _spec["target"] = self.target

    # End of generated code
