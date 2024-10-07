from ocp_resources.resource import MissingRequiredArgumentError, Resource


class MultiClusterObservability(Resource):
    """
    https://github.com/stolostron/multicluster-observability-operator/blob/main/docs/MultiClusterObservability-CRD.md
    """

    api_group = Resource.ApiGroup.OBSERVABILITY_OPEN_CLUSTER_MANAGEMENT_IO

    def __init__(
        self,
        observability_addon_spec=None,
        metric_object_storage=None,
        enable_downsampling=True,
        image_pull_policy=None,
        image_pull_secret=None,
        **kwargs,
    ):
        """
        Args:
            observability_addon_spec (dict): Global settings for all managed clusters which have observability
                add-on installed. If not provided, an empty dict is provided.
            metric_object_storage (dict): Reference to Preconfigured Storage to be used by Observability.
                The storage secret must be created.
                https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.3/html/observability/observing-environments-intro#enabling-observability
                Example: {"name": "thanos-object-storage, "key": "thanos.yaml"}
            enable_downsampling (bool, optional): Enable or disable the downsampling.
            image_pull_policy (str, optional): Pull policy of the MultiClusterObservability images.
            image_pull_secret (str, optional): Pull secret of the MultiCluster Observability images.
        """

        super().__init__(**kwargs)
        self.observability_addon_spec = observability_addon_spec or {}
        self.metric_object_storage = metric_object_storage
        self.enable_downsampling = enable_downsampling
        self.image_pull_policy = image_pull_policy
        self.image_pull_secret = image_pull_secret

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.metric_object_storage:
                raise MissingRequiredArgumentError(argument="metric_object_storage")
            spec_dict = {"observabilityAddonSpec": self.observability_addon_spec}
            spec_dict.setdefault("storageConfig", {})["metricObjectStorage"] = self.metric_object_storage

            if self.enable_downsampling:
                spec_dict["enableDownsampling"] = self.enable_downsampling
            if self.image_pull_policy:
                spec_dict["imagePullPolicy"] = self.image_pull_policy
            if self.image_pull_secret:
                spec_dict["imagePullSecret"] = self.image_pull_secret

            self.res.update({"spec": spec_dict})
