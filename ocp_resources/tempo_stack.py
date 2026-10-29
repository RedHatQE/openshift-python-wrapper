# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class TempoStack(NamespacedResource):
    """
    TempoStack manages a Tempo deployment in microservices mode.
    """

    api_group: str = NamespacedResource.ApiGroup.TEMPO_GRAFANA_COM

    def __init__(
        self,
        extra_config: dict[str, Any] | None = None,
        hash_ring: dict[str, Any] | None = None,
        images: dict[str, Any] | None = None,
        limits: dict[str, Any] | None = None,
        management_state: str | None = None,
        observability: dict[str, Any] | None = None,
        replication_factor: int | None = None,
        resources: dict[str, Any] | None = None,
        retention: dict[str, Any] | None = None,
        search: dict[str, Any] | None = None,
        service_account: str | None = None,
        storage: dict[str, Any] | None = None,
        storage_class_name: str | None = None,
        storage_size: Any | None = None,
        template: dict[str, Any] | None = None,
        tenants: dict[str, Any] | None = None,
        timeout: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            extra_config (dict[str, Any]): ExtraConfigSpec defines extra configurations for tempo that will be
              merged with the operator generated, configurations defined here
              has precedence and could override generated config.

            hash_ring (dict[str, Any]): HashRing defines the spec for the distributed hash ring configuration.

            images (dict[str, Any]): Images defines the image for each container.

            limits (dict[str, Any]): LimitSpec is used to limit ingestion and querying rates.

            management_state (str): ManagementState defines if the CR should be managed by the operator or
              not. Default is managed.

            observability (dict[str, Any]): ObservabilitySpec defines how telemetry data gets handled.

            replication_factor (int): The replication factor is a configuration setting that determines how
              many ingesters need to acknowledge the data from the distributors
              before accepting a span.

            resources (dict[str, Any]): Resources defines resources configuration.

            retention (dict[str, Any]): Retention period defined by dataset. User can specify how long data
              should be stored.

            search (dict[str, Any]): SearchSpec control the configuration for the search capabilities.

            service_account (str): ServiceAccount defines the service account to use for all tempo
              components.

            storage (dict[str, Any]): Storage defines the spec for the object storage endpoint to store
              traces. User is required to create secret and supply it.

            storage_class_name (str): StorageClassName for PVCs used by ingester. Defaults to nil (default
              storage class in the cluster).

            storage_size (Any): StorageSize for PVCs used by ingester. Defaults to 10Gi.

            template (dict[str, Any]): Template defines requirements for a set of tempo components.

            tenants (dict[str, Any]): Tenants defines the per-tenant authentication and authorization spec.

            timeout (str): Timeout configures the same timeout on all components starting at
              ingress down to the ingestor/querier. Timeout configuration on a
              specific component has a higher precedence. Defaults to 30
              seconds.

        """
        super().__init__(**kwargs)

        self.extra_config = extra_config
        self.hash_ring = hash_ring
        self.images = images
        self.limits = limits
        self.management_state = management_state
        self.observability = observability
        self.replication_factor = replication_factor
        self.resources = resources
        self.retention = retention
        self.search = search
        self.service_account = service_account
        self.storage = storage
        self.storage_class_name = storage_class_name
        self.storage_size = storage_size
        self.template = template
        self.tenants = tenants
        self.timeout = timeout

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.management_state is None:
                raise MissingRequiredArgumentError(argument="self.management_state")

            if self.storage is None:
                raise MissingRequiredArgumentError(argument="self.storage")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["managementState"] = self.management_state
            _spec["storage"] = self.storage

            if self.extra_config is not None:
                _spec["extraConfig"] = self.extra_config

            if self.hash_ring is not None:
                _spec["hashRing"] = self.hash_ring

            if self.images is not None:
                _spec["images"] = self.images

            if self.limits is not None:
                _spec["limits"] = self.limits

            if self.observability is not None:
                _spec["observability"] = self.observability

            if self.replication_factor is not None:
                _spec["replicationFactor"] = self.replication_factor

            if self.resources is not None:
                _spec["resources"] = self.resources

            if self.retention is not None:
                _spec["retention"] = self.retention

            if self.search is not None:
                _spec["search"] = self.search

            if self.service_account is not None:
                _spec["serviceAccount"] = self.service_account

            if self.storage_class_name is not None:
                _spec["storageClassName"] = self.storage_class_name

            if self.storage_size is not None:
                _spec["storageSize"] = self.storage_size

            if self.template is not None:
                _spec["template"] = self.template

            if self.tenants is not None:
                _spec["tenants"] = self.tenants

            if self.timeout is not None:
                _spec["timeout"] = self.timeout

    # End of generated code
