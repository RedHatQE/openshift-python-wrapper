# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from warnings import warn

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource

warn(
    "model_registry.py module will be removed in the next release, "
    "please import `ModelRegistry` from model_registry_modelregistry_opendatahub_io.py "
    "or model_registry_components_platform_opendatahub_io.py instead",
    DeprecationWarning,
    stacklevel=2,
)


class ModelRegistry(NamespacedResource):
    """
    ModelRegistry is the Schema for the modelregistries API
    """

    api_group: str = NamespacedResource.ApiGroup.MODELREGISTRY_OPENDATAHUB_IO

    def __init__(
        self,
        downgrade_db_schema_version: int | None = None,
        enable_database_upgrade: bool | None = None,
        grpc: dict[str, Any] | None = None,
        istio: dict[str, Any] | None = None,
        mysql: dict[str, Any] | None = None,
        postgres: dict[str, Any] | None = None,
        rest: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            downgrade_db_schema_version (int): Database downgrade schema version value. If set the database schema
              version is downgraded to the set value during initialization
              (Optional Parameter)

            enable_database_upgrade (bool): Flag specifying database upgrade option. If set to true, it enables
              database migration during initialization (Optional parameter)

            grpc (dict[str, Any]): Configuration for gRPC endpoint

            istio (dict[str, Any]): Istio servicemesh configuration options

            mysql (dict[str, Any]): MySQL configuration options

            postgres (dict[str, Any]): PostgreSQL configuration options

            rest (dict[str, Any]): Configuration for REST endpoint

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
