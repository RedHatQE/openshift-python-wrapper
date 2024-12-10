# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class ModelRegistry(NamespacedResource):
    """
    ModelRegistry is the Schema for the modelregistries API
    """

    api_group: str = NamespacedResource.ApiGroup.MODELREGISTRY_OPENDATAHUB_IO

    def __init__(
        self,
        downgrade_db_schema_version: Optional[int] = None,
        enable_database_upgrade: Optional[bool] = None,
        grpc: Optional[Dict[str, Any]] = None,
        istio: Optional[Dict[str, Any]] = None,
        mysql: Optional[Dict[str, Any]] = None,
        postgres: Optional[Dict[str, Any]] = None,
        rest: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            downgrade_db_schema_version (int): Database downgrade schema version value. If set the database schema
              version is downgraded to the set value during initialization
              (Optional Parameter)

            enable_database_upgrade (bool): Flag specifying database upgrade option. If set to true, it enables
              database migration during initialization (Optional parameter)

            grpc (Dict[str, Any]): Configuration for gRPC endpoint

            istio (Dict[str, Any]): Istio servicemesh configuration options

            mysql (Dict[str, Any]): MySQL configuration options

            postgres (Dict[str, Any]): PostgreSQL configuration options

            rest (Dict[str, Any]): Configuration for REST endpoint

        """
        super().__init__(**kwargs)

        self.downgrade_db_schema_version = downgrade_db_schema_version
        self.enable_database_upgrade = enable_database_upgrade
        self.grpc = grpc
        self.istio = istio
        self.mysql = mysql
        self.postgres = postgres
        self.rest = rest

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.grpc is None:
                raise MissingRequiredArgumentError(argument="self.grpc")

            if self.rest is None:
                raise MissingRequiredArgumentError(argument="self.rest")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["grpc"] = self.grpc
            _spec["rest"] = self.rest

            if self.downgrade_db_schema_version:
                _spec["downgrade_db_schema_version"] = self.downgrade_db_schema_version

            if self.enable_database_upgrade is not None:
                _spec["enable_database_upgrade"] = self.enable_database_upgrade

            if self.istio:
                _spec["istio"] = self.istio

            if self.mysql:
                _spec["mysql"] = self.mysql

            if self.postgres:
                _spec["postgres"] = self.postgres

    # End of generated code
