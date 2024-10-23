# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class Authorino(NamespacedResource):
    """
    Authorino is the Schema for the authorinos API
    """

    api_group: str = NamespacedResource.ApiGroup.OPERATOR_AUTHORINO_KUADRANT_IO

    def __init__(
        self,
        auth_config_label_selectors: Optional[str] = "",
        cluster_wide: Optional[bool] = None,
        evaluator_cache_size: Optional[int] = None,
        healthz: Optional[Dict[str, Any]] = None,
        image: Optional[str] = "",
        image_pull_policy: Optional[str] = "",
        listener: Optional[Dict[str, Any]] = None,
        log_level: Optional[str] = "",
        log_mode: Optional[str] = "",
        metrics: Optional[Dict[str, Any]] = None,
        oidc_server: Optional[Dict[str, Any]] = None,
        replicas: Optional[int] = None,
        secret_label_selectors: Optional[str] = "",
        superseding_host_subsets: Optional[bool] = None,
        tracing: Optional[Dict[str, Any]] = None,
        volumes: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            auth_config_label_selectors (str): No field description from API; please add description

            cluster_wide (bool): No field description from API; please add description

            evaluator_cache_size (int): No field description from API; please add description

            healthz (Dict[str, Any]): No field description from API; please add description

            image (str): No field description from API; please add description

            image_pull_policy (str): PullPolicy describes a policy for if/when to pull a container image

            listener (Dict[str, Any]): No field description from API; please add description

            log_level (str): No field description from API; please add description

            log_mode (str): No field description from API; please add description

            metrics (Dict[str, Any]): No field description from API; please add description

            oidc_server (Dict[str, Any]): No field description from API; please add description

            replicas (int): No field description from API; please add description

            secret_label_selectors (str): No field description from API; please add description

            superseding_host_subsets (bool): No field description from API; please add description

            tracing (Dict[str, Any]): No field description from API; please add description

            volumes (Dict[str, Any]): No field description from API; please add description

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
            if not self.listener:
                raise MissingRequiredArgumentError(argument="self.listener")

            if not self.oidc_server:
                raise MissingRequiredArgumentError(argument="self.oidc_server")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["listener"] = self.listener
            _spec["oidcServer"] = self.oidc_server

            if self.auth_config_label_selectors:
                _spec["authConfigLabelSelectors"] = self.auth_config_label_selectors

            if self.cluster_wide is not None:
                _spec["clusterWide"] = self.cluster_wide

            if self.evaluator_cache_size:
                _spec["evaluatorCacheSize"] = self.evaluator_cache_size

            if self.healthz:
                _spec["healthz"] = self.healthz

            if self.image:
                _spec["image"] = self.image

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.log_level:
                _spec["logLevel"] = self.log_level

            if self.log_mode:
                _spec["logMode"] = self.log_mode

            if self.metrics:
                _spec["metrics"] = self.metrics

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.secret_label_selectors:
                _spec["secretLabelSelectors"] = self.secret_label_selectors

            if self.superseding_host_subsets is not None:
                _spec["supersedingHostSubsets"] = self.superseding_host_subsets

            if self.tracing:
                _spec["tracing"] = self.tracing

            if self.volumes:
                _spec["volumes"] = self.volumes

    # End of generated code
