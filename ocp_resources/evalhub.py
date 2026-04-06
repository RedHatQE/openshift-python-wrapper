# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class EvalHub(NamespacedResource):
    """
    EvalHub is the Schema for the evalhubs API
    """

    api_group: str = NamespacedResource.ApiGroup.TRUSTYAI_OPENDATAHUB_IO

    def __init__(
        self,
        collections: list[Any] | None = None,
        database: dict[str, Any] | None = None,
        env: list[Any] | None = None,
        otel: dict[str, Any] | None = None,
        providers: list[Any] | None = None,
        replicas: int | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            collections (list[Any]): Collections is the list of OOTB collection names to mount into the
              deployment. Each name must match a collection-name label on a
              ConfigMap in the operator namespace.

            database (dict[str, Any]): Database configuration for persistent storage. This field is required:
              the operator will not start the service without an explicit
              database configuration. Set type to "postgresql" with a secret
              reference, or "sqlite" for lightweight/development deployments.

            env (list[Any]): Environment variables for the eval-hub container

            otel (dict[str, Any]): OpenTelemetry configuration for observability. When set, the operator
              includes OTEL settings in the generated config. When omitted, the
              service uses its defaults (OTEL disabled).

            providers (list[Any]): Providers is the list of OOTB provider names to mount into the
              deployment. Each name must match a provider-name label on a
              ConfigMap in the operator namespace.

            replicas (int): Number of replicas for the eval-hub deployment

        """
        super().__init__(**kwargs)

        self.collections = collections
        self.database = database
        self.env = env
        self.otel = otel
        self.providers = providers
        self.replicas = replicas

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.collections is not None:
                _spec["collections"] = self.collections

            if self.database is not None:
                _spec["database"] = self.database

            if self.env is not None:
                _spec["env"] = self.env

            if self.otel is not None:
                _spec["otel"] = self.otel

            if self.providers is not None:
                _spec["providers"] = self.providers

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

    # End of generated code
