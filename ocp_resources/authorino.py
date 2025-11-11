# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class Authorino(NamespacedResource):
    """
    Authorino is the Schema for the authorinos API
    """

    api_group: str = NamespacedResource.ApiGroup.OPERATOR_AUTHORINO_KUADRANT_IO

    def __init__(
        self,
        auth_config_label_selectors: str | None = None,
        cluster_wide: bool | None = None,
        evaluator_cache_size: int | None = None,
        healthz: dict[str, Any] | None = None,
        image: str | None = None,
        image_pull_policy: str | None = None,
        listener: dict[str, Any] | None = None,
        log_level: str | None = None,
        log_mode: str | None = None,
        metrics: dict[str, Any] | None = None,
        oidc_server: dict[str, Any] | None = None,
        replicas: int | None = None,
        secret_label_selectors: str | None = None,
        superseding_host_subsets: bool | None = None,
        tracing: dict[str, Any] | None = None,
        volumes: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            auth_config_label_selectors (str): No field description from API

            cluster_wide (bool): No field description from API

            evaluator_cache_size (int): No field description from API

            healthz (dict[str, Any]): No field description from API

            image (str): No field description from API

            image_pull_policy (str): PullPolicy describes a policy for if/when to pull a container image

            listener (dict[str, Any]): No field description from API

            log_level (str): No field description from API

            log_mode (str): No field description from API

            metrics (dict[str, Any]): No field description from API

            oidc_server (dict[str, Any]): No field description from API

            replicas (int): No field description from API

            secret_label_selectors (str): No field description from API

            superseding_host_subsets (bool): No field description from API

            tracing (dict[str, Any]): No field description from API

            volumes (dict[str, Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.auth_config_label_selectors = auth_config_label_selectors
        self.cluster_wide = cluster_wide
        self.evaluator_cache_size = evaluator_cache_size
        self.healthz = healthz
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.listener = listener
        self.log_level = log_level
        self.log_mode = log_mode
        self.metrics = metrics
        self.oidc_server = oidc_server
        self.replicas = replicas
        self.secret_label_selectors = secret_label_selectors
        self.superseding_host_subsets = superseding_host_subsets
        self.tracing = tracing
        self.volumes = volumes

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.listener is None:
                raise MissingRequiredArgumentError(argument="self.listener")

            if self.oidc_server is None:
                raise MissingRequiredArgumentError(argument="self.oidc_server")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["listener"] = self.listener
            _spec["oidcServer"] = self.oidc_server

            if self.auth_config_label_selectors is not None:
                _spec["authConfigLabelSelectors"] = self.auth_config_label_selectors

            if self.cluster_wide is not None:
                _spec["clusterWide"] = self.cluster_wide

            if self.evaluator_cache_size is not None:
                _spec["evaluatorCacheSize"] = self.evaluator_cache_size

            if self.healthz is not None:
                _spec["healthz"] = self.healthz

            if self.image is not None:
                _spec["image"] = self.image

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.log_level is not None:
                _spec["logLevel"] = self.log_level

            if self.log_mode is not None:
                _spec["logMode"] = self.log_mode

            if self.metrics is not None:
                _spec["metrics"] = self.metrics

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.secret_label_selectors is not None:
                _spec["secretLabelSelectors"] = self.secret_label_selectors

            if self.superseding_host_subsets is not None:
                _spec["supersedingHostSubsets"] = self.superseding_host_subsets

            if self.tracing is not None:
                _spec["tracing"] = self.tracing

            if self.volumes is not None:
                _spec["volumes"] = self.volumes

    # End of generated code
