# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class Prometheus(NamespacedResource):
    """
    Prometheus defines a Prometheus deployment.
    """

    api_group: str = NamespacedResource.ApiGroup.MONITORING_COREOS_COM

    def __init__(
        self,
        additional_alert_manager_configs: Optional[Dict[str, Any]] = None,
        additional_alert_relabel_configs: Optional[Dict[str, Any]] = None,
        additional_args: Optional[List[Any]] = None,
        additional_scrape_configs: Optional[Dict[str, Any]] = None,
        affinity: Optional[Dict[str, Any]] = None,
        alerting: Optional[Dict[str, Any]] = None,
        allow_overlapping_blocks: Optional[bool] = None,
        apiserver_config: Optional[Dict[str, Any]] = None,
        arbitrary_fs_access_through_sms: Optional[Dict[str, Any]] = None,
        automount_service_account_token: Optional[bool] = None,
        base_image: Optional[str] = "",
        body_size_limit: Optional[str] = "",
        config_maps: Optional[List[Any]] = None,
        containers: Optional[List[Any]] = None,
        disable_compaction: Optional[bool] = None,
        enable_admin_api: Optional[bool] = None,
        enable_features: Optional[List[Any]] = None,
        enable_remote_write_receiver: Optional[bool] = None,
        enforced_body_size_limit: Optional[str] = "",
        enforced_keep_dropped_targets: Optional[int] = None,
        enforced_label_limit: Optional[int] = None,
        enforced_label_name_length_limit: Optional[int] = None,
        enforced_label_value_length_limit: Optional[int] = None,
        enforced_namespace_label: Optional[str] = "",
        enforced_sample_limit: Optional[int] = None,
        enforced_target_limit: Optional[int] = None,
        evaluation_interval: Optional[str] = "",
        excluded_from_enforcement: Optional[List[Any]] = None,
        exemplars: Optional[Dict[str, Any]] = None,
        external_labels: Optional[Dict[str, Any]] = None,
        external_url: Optional[str] = "",
        host_aliases: Optional[List[Any]] = None,
        host_network: Optional[bool] = None,
        ignore_namespace_selectors: Optional[bool] = None,
        image: Optional[str] = "",
        image_pull_policy: Optional[str] = "",
        image_pull_secrets: Optional[List[Any]] = None,
        init_containers: Optional[List[Any]] = None,
        keep_dropped_targets: Optional[int] = None,
        label_limit: Optional[int] = None,
        label_name_length_limit: Optional[int] = None,
        label_value_length_limit: Optional[int] = None,
        listen_local: Optional[bool] = None,
        log_format: Optional[str] = "",
        log_level: Optional[str] = "",
        maximum_startup_duration_seconds: Optional[int] = None,
        min_ready_seconds: Optional[int] = None,
        node_selector: Optional[Dict[str, Any]] = None,
        override_honor_labels: Optional[bool] = None,
        override_honor_timestamps: Optional[bool] = None,
        paused: Optional[bool] = None,
        persistent_volume_claim_retention_policy: Optional[Dict[str, Any]] = None,
        pod_metadata: Optional[Dict[str, Any]] = None,
        pod_monitor_namespace_selector: Optional[Dict[str, Any]] = None,
        pod_monitor_selector: Optional[Dict[str, Any]] = None,
        pod_target_labels: Optional[List[Any]] = None,
        port_name: Optional[str] = "",
        priority_class_name: Optional[str] = "",
        probe_namespace_selector: Optional[Dict[str, Any]] = None,
        probe_selector: Optional[Dict[str, Any]] = None,
        prometheus_external_label_name: Optional[str] = "",
        prometheus_rules_excluded_from_enforce: Optional[List[Any]] = None,
        query: Optional[Dict[str, Any]] = None,
        query_log_file: Optional[str] = "",
        reload_strategy: Optional[str] = "",
        remote_read: Optional[List[Any]] = None,
        remote_write: Optional[List[Any]] = None,
        replica_external_label_name: Optional[str] = "",
        replicas: Optional[int] = None,
        resources: Optional[Dict[str, Any]] = None,
        retention: Optional[str] = "",
        retention_size: Optional[str] = "",
        route_prefix: Optional[str] = "",
        rule_namespace_selector: Optional[Dict[str, Any]] = None,
        rule_selector: Optional[Dict[str, Any]] = None,
        rules: Optional[Dict[str, Any]] = None,
        sample_limit: Optional[int] = None,
        scrape_classes: Optional[List[Any]] = None,
        scrape_config_namespace_selector: Optional[Dict[str, Any]] = None,
        scrape_config_selector: Optional[Dict[str, Any]] = None,
        scrape_interval: Optional[str] = "",
        scrape_protocols: Optional[List[Any]] = None,
        scrape_timeout: Optional[str] = "",
        secrets: Optional[List[Any]] = None,
        security_context: Optional[Dict[str, Any]] = None,
        service_account_name: Optional[str] = "",
        service_monitor_namespace_selector: Optional[Dict[str, Any]] = None,
        service_monitor_selector: Optional[Dict[str, Any]] = None,
        sha: Optional[str] = "",
        shards: Optional[int] = None,
        storage: Optional[Dict[str, Any]] = None,
        tag: Optional[str] = "",
        target_limit: Optional[int] = None,
        thanos: Optional[Dict[str, Any]] = None,
        tolerations: Optional[List[Any]] = None,
        topology_spread_constraints: Optional[List[Any]] = None,
        tracing_config: Optional[Dict[str, Any]] = None,
        tsdb: Optional[Dict[str, Any]] = None,
        version: Optional[str] = "",
        volume_mounts: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        wal_compression: Optional[bool] = None,
        web: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            additional_alert_manager_configs (Dict[str, Any]): AdditionalAlertManagerConfigs specifies a key of a Secret containing
              additional Prometheus Alertmanager configurations. The
              Alertmanager configurations are appended to the configuration
              generated by the Prometheus Operator. They must be formatted
              according to the official Prometheus documentation:   https://prom
              etheus.io/docs/prometheus/latest/configuration/configuration/#aler
              tmanager_config   The user is responsible for making sure that the
              configurations are valid   Note that using this feature may expose
              the possibility to break upgrades of Prometheus. It is advised to
              review Prometheus release notes to ensure that no incompatible
              AlertManager configs are going to break Prometheus after the
              upgrade.

            additional_alert_relabel_configs (Dict[str, Any]): AdditionalAlertRelabelConfigs specifies a key of a Secret containing
              additional Prometheus alert relabel configurations. The alert
              relabel configurations are appended to the configuration generated
              by the Prometheus Operator. They must be formatted according to
              the official Prometheus documentation:   https://prometheus.io/doc
              s/prometheus/latest/configuration/configuration/#alert_relabel_con
              figs   The user is responsible for making sure that the
              configurations are valid   Note that using this feature may expose
              the possibility to break upgrades of Prometheus. It is advised to
              review Prometheus release notes to ensure that no incompatible
              alert relabel configs are going to break Prometheus after the
              upgrade.

            additional_args (List[Any]): AdditionalArgs allows setting additional arguments for the
              'prometheus' container.   It is intended for e.g. activating
              hidden flags which are not supported by the dedicated
              configuration options yet. The arguments are passed as-is to the
              Prometheus container which may cause issues if they are invalid or
              not supported by the given Prometheus version.   In case of an
              argument conflict (e.g. an argument which is already set by the
              operator itself) or when providing an invalid argument, the
              reconciliation will fail and an error will be logged.

            additional_scrape_configs (Dict[str, Any]): AdditionalScrapeConfigs allows specifying a key of a Secret containing
              additional Prometheus scrape configurations. Scrape configurations
              specified are appended to the configurations generated by the
              Prometheus Operator. Job configurations specified must have the
              form as specified in the official Prometheus documentation: https:
              //prometheus.io/docs/prometheus/latest/configuration/configuration
              /#scrape_config. As scrape configs are appended, the user is
              responsible to make sure it is valid. Note that using this feature
              may expose the possibility to break upgrades of Prometheus. It is
              advised to review Prometheus release notes to ensure that no
              incompatible scrape configs are going to break Prometheus after
              the upgrade.

            affinity (Dict[str, Any]): Defines the Pods' affinity scheduling rules if specified.

            alerting (Dict[str, Any]): Defines the settings related to Alertmanager.

            allow_overlapping_blocks (bool): AllowOverlappingBlocks enables vertical compaction and vertical query
              merge in Prometheus.   Deprecated: this flag has no effect for
              Prometheus >= 2.39.0 where overlapping blocks are enabled by
              default.

            apiserver_config (Dict[str, Any]): APIServerConfig allows specifying a host and auth methods to access
              the Kuberntees API server. If null, Prometheus is assumed to run
              inside of the cluster: it will discover the API servers
              automatically and use the Pod's CA certificate and bearer token
              file at /var/run/secrets/kubernetes.io/serviceaccount/.

            arbitrary_fs_access_through_sms (Dict[str, Any]): When true, ServiceMonitor, PodMonitor and Probe object are forbidden
              to reference arbitrary files on the file system of the
              'prometheus' container. When a ServiceMonitor's endpoint specifies
              a `bearerTokenFile` value (e.g.
              '/var/run/secrets/kubernetes.io/serviceaccount/token'), a
              malicious target can get access to the Prometheus service
              account's token in the Prometheus' scrape request. Setting
              `spec.arbitraryFSAccessThroughSM` to 'true' would prevent the
              attack. Users should instead provide the credentials using the
              `spec.bearerTokenSecret` field.

            automount_service_account_token (bool): AutomountServiceAccountToken indicates whether a service account token
              should be automatically mounted in the pod. If the field isn't
              set, the operator mounts the service account token by default.
              **Warning:** be aware that by default, Prometheus requires the
              service account token for Kubernetes service discovery. It is
              possible to use strategic merge patch to project the service
              account token into the 'prometheus' container.

            base_image (str): Deprecated: use 'spec.image' instead.

            body_size_limit (str): BodySizeLimit defines per-scrape on response body size. Only valid in
              Prometheus versions 2.45.0 and newer.   Note that the global limit
              only applies to scrape objects that don't specify an explicit
              limit value. If you want to enforce a maximum limit for all scrape
              objects, refer to enforcedBodySizeLimit.

            config_maps (List[Any]): ConfigMaps is a list of ConfigMaps in the same namespace as the
              Prometheus object, which shall be mounted into the Prometheus
              Pods. Each ConfigMap is added to the StatefulSet definition as a
              volume named `configmap-<configmap-name>`. The ConfigMaps are
              mounted into /etc/prometheus/configmaps/<configmap-name> in the
              'prometheus' container.

            containers (List[Any]): Containers allows injecting additional containers or modifying
              operator generated containers. This can be used to allow adding an
              authentication proxy to the Pods or to change the behavior of an
              operator generated container. Containers described here modify an
              operator generated container if they share the same name and
              modifications are done via a strategic merge patch.   The names of
              containers managed by the operator are: * `prometheus` * `config-
              reloader` * `thanos-sidecar`   Overriding containers is entirely
              outside the scope of what the maintainers will support and by
              doing so, you accept that this behaviour may break at any time
              without notice.

            disable_compaction (bool): When true, the Prometheus compaction is disabled.

            enable_admin_api (bool): Enables access to the Prometheus web admin API.   WARNING: Enabling
              the admin APIs enables mutating endpoints, to delete data,
              shutdown Prometheus, and more. Enabling this should be done with
              care and the user is advised to add additional authentication
              authorization via a proxy to ensure only clients authorized to
              perform these actions can do so.   For more information:
              https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-
              admin-apis

            enable_features (List[Any]): Enable access to Prometheus feature flags. By default, no features are
              enabled.   Enabling features which are disabled by default is
              entirely outside the scope of what the maintainers will support
              and by doing so, you accept that this behaviour may break at any
              time without notice.   For more information see
              https://prometheus.io/docs/prometheus/latest/feature_flags/

            enable_remote_write_receiver (bool): Enable Prometheus to be used as a receiver for the Prometheus remote
              write protocol.   WARNING: This is not considered an efficient way
              of ingesting samples. Use it with caution for specific low-volume
              use cases. It is not suitable for replacing the ingestion via
              scraping and turning Prometheus into a push-based metrics
              collection system. For more information see
              https://prometheus.io/docs/prometheus/latest/querying/api/#remote-
              write-receiver   It requires Prometheus >= v2.33.0.

            enforced_body_size_limit (str): When defined, enforcedBodySizeLimit specifies a global limit on the
              size of uncompressed response body that will be accepted by
              Prometheus. Targets responding with a body larger than this many
              bytes will cause the scrape to fail.   It requires Prometheus >=
              v2.28.0.   When both `enforcedBodySizeLimit` and `bodySizeLimit`
              are defined and greater than zero, the following rules apply: *
              Scrape objects without a defined bodySizeLimit value will inherit
              the global bodySizeLimit value (Prometheus >= 2.45.0) or the
              enforcedBodySizeLimit value (Prometheus < v2.45.0).   If
              Prometheus version is >= 2.45.0 and the `enforcedBodySizeLimit` is
              greater than the `bodySizeLimit`, the `bodySizeLimit` will be set
              to `enforcedBodySizeLimit`. * Scrape objects with a bodySizeLimit
              value less than or equal to enforcedBodySizeLimit keep their
              specific value. * Scrape objects with a bodySizeLimit value
              greater than enforcedBodySizeLimit are set to
              enforcedBodySizeLimit.

            enforced_keep_dropped_targets (int): When defined, enforcedKeepDroppedTargets specifies a global limit on
              the number of targets dropped by relabeling that will be kept in
              memory. The value overrides any `spec.keepDroppedTargets` set by
              ServiceMonitor, PodMonitor, Probe objects unless
              `spec.keepDroppedTargets` is greater than zero and less than
              `spec.enforcedKeepDroppedTargets`.   It requires Prometheus >=
              v2.47.0.   When both `enforcedKeepDroppedTargets` and
              `keepDroppedTargets` are defined and greater than zero, the
              following rules apply: * Scrape objects without a defined
              keepDroppedTargets value will inherit the global
              keepDroppedTargets value (Prometheus >= 2.45.0) or the
              enforcedKeepDroppedTargets value (Prometheus < v2.45.0).   If
              Prometheus version is >= 2.45.0 and the
              `enforcedKeepDroppedTargets` is greater than the
              `keepDroppedTargets`, the `keepDroppedTargets` will be set to
              `enforcedKeepDroppedTargets`. * Scrape objects with a
              keepDroppedTargets value less than or equal to
              enforcedKeepDroppedTargets keep their specific value. * Scrape
              objects with a keepDroppedTargets value greater than
              enforcedKeepDroppedTargets are set to enforcedKeepDroppedTargets.

            enforced_label_limit (int): When defined, enforcedLabelLimit specifies a global limit on the
              number of labels per sample. The value overrides any
              `spec.labelLimit` set by ServiceMonitor, PodMonitor, Probe objects
              unless `spec.labelLimit` is greater than zero and less than
              `spec.enforcedLabelLimit`.   It requires Prometheus >= v2.27.0.
              When both `enforcedLabelLimit` and `labelLimit` are defined and
              greater than zero, the following rules apply: * Scrape objects
              without a defined labelLimit value will inherit the global
              labelLimit value (Prometheus >= 2.45.0) or the enforcedLabelLimit
              value (Prometheus < v2.45.0).   If Prometheus version is >= 2.45.0
              and the `enforcedLabelLimit` is greater than the `labelLimit`, the
              `labelLimit` will be set to `enforcedLabelLimit`. * Scrape objects
              with a labelLimit value less than or equal to enforcedLabelLimit
              keep their specific value. * Scrape objects with a labelLimit
              value greater than enforcedLabelLimit are set to
              enforcedLabelLimit.

            enforced_label_name_length_limit (int): When defined, enforcedLabelNameLengthLimit specifies a global limit on
              the length of labels name per sample. The value overrides any
              `spec.labelNameLengthLimit` set by ServiceMonitor, PodMonitor,
              Probe objects unless `spec.labelNameLengthLimit` is greater than
              zero and less than `spec.enforcedLabelNameLengthLimit`.   It
              requires Prometheus >= v2.27.0.   When both
              `enforcedLabelNameLengthLimit` and `labelNameLengthLimit` are
              defined and greater than zero, the following rules apply: * Scrape
              objects without a defined labelNameLengthLimit value will inherit
              the global labelNameLengthLimit value (Prometheus >= 2.45.0) or
              the enforcedLabelNameLengthLimit value (Prometheus < v2.45.0).
              If Prometheus version is >= 2.45.0 and the
              `enforcedLabelNameLengthLimit` is greater than the
              `labelNameLengthLimit`, the `labelNameLengthLimit` will be set to
              `enforcedLabelNameLengthLimit`. * Scrape objects with a
              labelNameLengthLimit value less than or equal to
              enforcedLabelNameLengthLimit keep their specific value. * Scrape
              objects with a labelNameLengthLimit value greater than
              enforcedLabelNameLengthLimit are set to
              enforcedLabelNameLengthLimit.

            enforced_label_value_length_limit (int): When not null, enforcedLabelValueLengthLimit defines a global limit on
              the length of labels value per sample. The value overrides any
              `spec.labelValueLengthLimit` set by ServiceMonitor, PodMonitor,
              Probe objects unless `spec.labelValueLengthLimit` is greater than
              zero and less than `spec.enforcedLabelValueLengthLimit`.   It
              requires Prometheus >= v2.27.0.   When both
              `enforcedLabelValueLengthLimit` and `labelValueLengthLimit` are
              defined and greater than zero, the following rules apply: * Scrape
              objects without a defined labelValueLengthLimit value will inherit
              the global labelValueLengthLimit value (Prometheus >= 2.45.0) or
              the enforcedLabelValueLengthLimit value (Prometheus < v2.45.0).
              If Prometheus version is >= 2.45.0 and the
              `enforcedLabelValueLengthLimit` is greater than the
              `labelValueLengthLimit`, the `labelValueLengthLimit` will be set
              to `enforcedLabelValueLengthLimit`. * Scrape objects with a
              labelValueLengthLimit value less than or equal to
              enforcedLabelValueLengthLimit keep their specific value. * Scrape
              objects with a labelValueLengthLimit value greater than
              enforcedLabelValueLengthLimit are set to
              enforcedLabelValueLengthLimit.

            enforced_namespace_label (str): When not empty, a label will be added to:   1. All metrics scraped
              from `ServiceMonitor`, `PodMonitor`, `Probe` and `ScrapeConfig`
              objects. 2. All metrics generated from recording rules defined in
              `PrometheusRule` objects. 3. All alerts generated from alerting
              rules defined in `PrometheusRule` objects. 4. All vector selectors
              of PromQL expressions defined in `PrometheusRule` objects.   The
              label will not added for objects referenced in
              `spec.excludedFromEnforcement`.   The label's name is this field's
              value. The label's value is the namespace of the `ServiceMonitor`,
              `PodMonitor`, `Probe`, `PrometheusRule` or `ScrapeConfig` object.

            enforced_sample_limit (int): When defined, enforcedSampleLimit specifies a global limit on the
              number of scraped samples that will be accepted. This overrides
              any `spec.sampleLimit` set by ServiceMonitor, PodMonitor, Probe
              objects unless `spec.sampleLimit` is greater than zero and less
              than `spec.enforcedSampleLimit`.   It is meant to be used by
              admins to keep the overall number of samples/series under a
              desired limit.   When both `enforcedSampleLimit` and `sampleLimit`
              are defined and greater than zero, the following rules apply: *
              Scrape objects without a defined sampleLimit value will inherit
              the global sampleLimit value (Prometheus >= 2.45.0) or the
              enforcedSampleLimit value (Prometheus < v2.45.0).   If Prometheus
              version is >= 2.45.0 and the `enforcedSampleLimit` is greater than
              the `sampleLimit`, the `sampleLimit` will be set to
              `enforcedSampleLimit`. * Scrape objects with a sampleLimit value
              less than or equal to enforcedSampleLimit keep their specific
              value. * Scrape objects with a sampleLimit value greater than
              enforcedSampleLimit are set to enforcedSampleLimit.

            enforced_target_limit (int): When defined, enforcedTargetLimit specifies a global limit on the
              number of scraped targets. The value overrides any
              `spec.targetLimit` set by ServiceMonitor, PodMonitor, Probe
              objects unless `spec.targetLimit` is greater than zero and less
              than `spec.enforcedTargetLimit`.   It is meant to be used by
              admins to to keep the overall number of targets under a desired
              limit.   When both `enforcedTargetLimit` and `targetLimit` are
              defined and greater than zero, the following rules apply: * Scrape
              objects without a defined targetLimit value will inherit the
              global targetLimit value (Prometheus >= 2.45.0) or the
              enforcedTargetLimit value (Prometheus < v2.45.0).   If Prometheus
              version is >= 2.45.0 and the `enforcedTargetLimit` is greater than
              the `targetLimit`, the `targetLimit` will be set to
              `enforcedTargetLimit`. * Scrape objects with a targetLimit value
              less than or equal to enforcedTargetLimit keep their specific
              value. * Scrape objects with a targetLimit value greater than
              enforcedTargetLimit are set to enforcedTargetLimit.

            evaluation_interval (str): Interval between rule evaluations. Default: "30s"

            excluded_from_enforcement (List[Any]): List of references to PodMonitor, ServiceMonitor, Probe and
              PrometheusRule objects to be excluded from enforcing a namespace
              label of origin.   It is only applicable if
              `spec.enforcedNamespaceLabel` set to true.

            exemplars (Dict[str, Any]): Exemplars related settings that are runtime reloadable. It requires to
              enable the `exemplar-storage` feature flag to be effective.

            external_labels (Dict[str, Any]): The labels to add to any time series or alerts when communicating with
              external systems (federation, remote storage, Alertmanager).
              Labels defined by `spec.replicaExternalLabelName` and
              `spec.prometheusExternalLabelName` take precedence over this list.

            external_url (str): The external URL under which the Prometheus service is externally
              available. This is necessary to generate correct URLs (for
              instance if Prometheus is accessible behind an Ingress resource).

            host_aliases (List[Any]): Optional list of hosts and IPs that will be injected into the Pod's
              hosts file if specified.

            host_network (bool): Use the host's network namespace if true.   Make sure to understand
              the security implications if you want to enable it
              (https://kubernetes.io/docs/concepts/configuration/overview/).
              When hostNetwork is enabled, this will set the DNS policy to
              `ClusterFirstWithHostNet` automatically.

            ignore_namespace_selectors (bool): When true, `spec.namespaceSelector` from all PodMonitor,
              ServiceMonitor and Probe objects will be ignored. They will only
              discover targets within the namespace of the PodMonitor,
              ServiceMonitor and Probe object.

            image (str): Container image name for Prometheus. If specified, it takes precedence
              over the `spec.baseImage`, `spec.tag` and `spec.sha` fields.
              Specifying `spec.version` is still necessary to ensure the
              Prometheus Operator knows which version of Prometheus is being
              configured.   If neither `spec.image` nor `spec.baseImage` are
              defined, the operator will use the latest upstream version of
              Prometheus available at the time when the operator was released.

            image_pull_policy (str): Image pull policy for the 'prometheus', 'init-config-reloader' and
              'config-reloader' containers. See
              https://kubernetes.io/docs/concepts/containers/images/#image-pull-
              policy for more details.

            image_pull_secrets (List[Any]): An optional list of references to Secrets in the same namespace to use
              for pulling images from registries. See
              http://kubernetes.io/docs/user-guide/images#specifying-
              imagepullsecrets-on-a-pod

            init_containers (List[Any]): InitContainers allows injecting initContainers to the Pod definition.
              Those can be used to e.g.  fetch secrets for injection into the
              Prometheus configuration from external sources. Any errors during
              the execution of an initContainer will lead to a restart of the
              Pod. More info:
              https://kubernetes.io/docs/concepts/workloads/pods/init-
              containers/ InitContainers described here modify an operator
              generated init containers if they share the same name and
              modifications are done via a strategic merge patch.   The names of
              init container name managed by the operator are: * `init-config-
              reloader`.   Overriding init containers is entirely outside the
              scope of what the maintainers will support and by doing so, you
              accept that this behaviour may break at any time without notice.

            keep_dropped_targets (int): Per-scrape limit on the number of targets dropped by relabeling that
              will be kept in memory. 0 means no limit.   It requires Prometheus
              >= v2.47.0.   Note that the global limit only applies to scrape
              objects that don't specify an explicit limit value. If you want to
              enforce a maximum limit for all scrape objects, refer to
              enforcedKeepDroppedTargets.

            label_limit (int): Per-scrape limit on number of labels that will be accepted for a
              sample. Only valid in Prometheus versions 2.45.0 and newer.   Note
              that the global limit only applies to scrape objects that don't
              specify an explicit limit value. If you want to enforce a maximum
              limit for all scrape objects, refer to enforcedLabelLimit.

            label_name_length_limit (int): Per-scrape limit on length of labels name that will be accepted for a
              sample. Only valid in Prometheus versions 2.45.0 and newer.   Note
              that the global limit only applies to scrape objects that don't
              specify an explicit limit value. If you want to enforce a maximum
              limit for all scrape objects, refer to
              enforcedLabelNameLengthLimit.

            label_value_length_limit (int): Per-scrape limit on length of labels value that will be accepted for a
              sample. Only valid in Prometheus versions 2.45.0 and newer.   Note
              that the global limit only applies to scrape objects that don't
              specify an explicit limit value. If you want to enforce a maximum
              limit for all scrape objects, refer to
              enforcedLabelValueLengthLimit.

            listen_local (bool): When true, the Prometheus server listens on the loopback address
              instead of the Pod IP's address.

            log_format (str): Log format for Log level for Prometheus and the config-reloader
              sidecar.

            log_level (str): Log level for Prometheus and the config-reloader sidecar.

            maximum_startup_duration_seconds (int): Defines the maximum time that the `prometheus` container's startup
              probe will wait before being considered failed. The startup probe
              will return success after the WAL replay is complete. If set, the
              value should be greater than 60 (seconds). Otherwise it will be
              equal to 600 seconds (15 minutes).

            min_ready_seconds (int): Minimum number of seconds for which a newly created Pod should be
              ready without any of its container crashing for it to be
              considered available. Defaults to 0 (pod will be considered
              available as soon as it is ready)   This is an alpha field from
              kubernetes 1.22 until 1.24 which requires enabling the
              StatefulSetMinReadySeconds feature gate.

            node_selector (Dict[str, Any]): Defines on which Nodes the Pods are scheduled.

            override_honor_labels (bool): When true, Prometheus resolves label conflicts by renaming the labels
              in the scraped data  to “exported_” for all targets created from
              ServiceMonitor, PodMonitor and ScrapeConfig objects. Otherwise the
              HonorLabels field of the service or pod monitor applies. In
              practice,`overrideHonorLaels:true` enforces `honorLabels:false`
              for all ServiceMonitor, PodMonitor and ScrapeConfig objects.

            override_honor_timestamps (bool): When true, Prometheus ignores the timestamps for all the targets
              created from service and pod monitors. Otherwise the
              HonorTimestamps field of the service or pod monitor applies.

            paused (bool): When a Prometheus deployment is paused, no actions except for deletion
              will be performed on the underlying objects.

            persistent_volume_claim_retention_policy (Dict[str, Any]): The field controls if and how PVCs are deleted during the lifecycle of
              a StatefulSet. The default behavior is all PVCs are retained. This
              is an alpha field from kubernetes 1.23 until 1.26 and a beta field
              from 1.26. It requires enabling the StatefulSetAutoDeletePVC
              feature gate.

            pod_metadata (Dict[str, Any]): PodMetadata configures labels and annotations which are propagated to
              the Prometheus pods.   The following items are reserved and cannot
              be overridden: * "prometheus" label, set to the name of the
              Prometheus object. * "app.kubernetes.io/instance" label, set to
              the name of the Prometheus object. * "app.kubernetes.io/managed-
              by" label, set to "prometheus-operator". *
              "app.kubernetes.io/name" label, set to "prometheus". *
              "app.kubernetes.io/version" label, set to the Prometheus version.
              * "operator.prometheus.io/name" label, set to the name of the
              Prometheus object. * "operator.prometheus.io/shard" label, set to
              the shard number of the Prometheus object. *
              "kubectl.kubernetes.io/default-container" annotation, set to
              "prometheus".

            pod_monitor_namespace_selector (Dict[str, Any]): Namespaces to match for PodMonitors discovery. An empty label selector
              matches all namespaces. A null label selector (default value)
              matches the current namespace only.

            pod_monitor_selector (Dict[str, Any]): PodMonitors to be selected for target discovery. An empty label
              selector matches all objects. A null label selector matches no
              objects.   If `spec.serviceMonitorSelector`,
              `spec.podMonitorSelector`, `spec.probeSelector` and
              `spec.scrapeConfigSelector` are null, the Prometheus configuration
              is unmanaged. The Prometheus operator will ensure that the
              Prometheus configuration's Secret exists, but it is the
              responsibility of the user to provide the raw gzipped Prometheus
              configuration under the `prometheus.yaml.gz` key. This behavior is
              *deprecated* and will be removed in the next major version of the
              custom resource definition. It is recommended to use
              `spec.additionalScrapeConfigs` instead.

            pod_target_labels (List[Any]): PodTargetLabels are appended to the `spec.podTargetLabels` field of
              all PodMonitor and ServiceMonitor objects.

            port_name (str): Port name used for the pods and governing service. Default: "web"

            priority_class_name (str): Priority class assigned to the Pods.

            probe_namespace_selector (Dict[str, Any]): Namespaces to match for Probe discovery. An empty label selector
              matches all namespaces. A null label selector matches the current
              namespace only.

            probe_selector (Dict[str, Any]): Probes to be selected for target discovery. An empty label selector
              matches all objects. A null label selector matches no objects.
              If `spec.serviceMonitorSelector`, `spec.podMonitorSelector`,
              `spec.probeSelector` and `spec.scrapeConfigSelector` are null, the
              Prometheus configuration is unmanaged. The Prometheus operator
              will ensure that the Prometheus configuration's Secret exists, but
              it is the responsibility of the user to provide the raw gzipped
              Prometheus configuration under the `prometheus.yaml.gz` key. This
              behavior is *deprecated* and will be removed in the next major
              version of the custom resource definition. It is recommended to
              use `spec.additionalScrapeConfigs` instead.

            prometheus_external_label_name (str): Name of Prometheus external label used to denote the Prometheus
              instance name. The external label will _not_ be added when the
              field is set to the empty string (`""`).   Default: "prometheus"

            prometheus_rules_excluded_from_enforce (List[Any]): Defines the list of PrometheusRule objects to which the namespace
              label enforcement doesn't apply. This is only relevant when
              `spec.enforcedNamespaceLabel` is set to true. Deprecated: use
              `spec.excludedFromEnforcement` instead.

            query (Dict[str, Any]): QuerySpec defines the configuration of the Promethus query service.

            query_log_file (str): queryLogFile specifies where the file to which PromQL queries are
              logged.   If the filename has an empty path, e.g. 'query.log', The
              Prometheus Pods will mount the file into an emptyDir volume at
              `/var/log/prometheus`. If a full path is provided, e.g.
              '/var/log/prometheus/query.log', you must mount a volume in the
              specified directory and it must be writable. This is because the
              prometheus container runs with a read-only root filesystem for
              security reasons. Alternatively, the location can be set to a
              standard I/O stream, e.g. `/dev/stdout`, to log query information
              to the default Prometheus log stream.

            reload_strategy (str): Defines the strategy used to reload the Prometheus configuration. If
              not specified, the configuration is reloaded using the /-/reload
              HTTP endpoint.

            remote_read (List[Any]): Defines the list of remote read configurations.

            remote_write (List[Any]): Defines the list of remote write configurations.

            replica_external_label_name (str): Name of Prometheus external label used to denote the replica name. The
              external label will _not_ be added when the field is set to the
              empty string (`""`).   Default: "prometheus_replica"

            replicas (int): Number of replicas of each shard to deploy for a Prometheus
              deployment. `spec.replicas` multiplied by `spec.shards` is the
              total number of Pods created.   Default: 1

            resources (Dict[str, Any]): Defines the resources requests and limits of the 'prometheus'
              container.

            retention (str): How long to retain the Prometheus data.   Default: "24h" if
              `spec.retention` and `spec.retentionSize` are empty.

            retention_size (str): Maximum number of bytes used by the Prometheus data.

            route_prefix (str): The route prefix Prometheus registers HTTP handlers for.   This is
              useful when using `spec.externalURL`, and a proxy is rewriting
              HTTP routes of a request, and the actual ExternalURL is still
              true, but the server serves requests under a different route
              prefix. For example for use with `kubectl proxy`.

            rule_namespace_selector (Dict[str, Any]): Namespaces to match for PrometheusRule discovery. An empty label
              selector matches all namespaces. A null label selector matches the
              current namespace only.

            rule_selector (Dict[str, Any]): PrometheusRule objects to be selected for rule evaluation. An empty
              label selector matches all objects. A null label selector matches
              no objects.

            rules (Dict[str, Any]): Defines the configuration of the Prometheus rules' engine.

            sample_limit (int): SampleLimit defines per-scrape limit on number of scraped samples that
              will be accepted. Only valid in Prometheus versions 2.45.0 and
              newer.   Note that the global limit only applies to scrape objects
              that don't specify an explicit limit value. If you want to enforce
              a maximum limit for all scrape objects, refer to
              enforcedSampleLimit.

            scrape_classes (List[Any]): List of scrape classes to expose to scraping objects such as
              PodMonitors, ServiceMonitors, Probes and ScrapeConfigs.   This is
              an *experimental feature*, it may change in any upcoming release
              in a breaking way.

            scrape_config_namespace_selector (Dict[str, Any]): Namespaces to match for ScrapeConfig discovery. An empty label
              selector matches all namespaces. A null label selector matches the
              current namespace only.   Note that the ScrapeConfig custom
              resource definition is currently at Alpha level.

            scrape_config_selector (Dict[str, Any]): ScrapeConfigs to be selected for target discovery. An empty label
              selector matches all objects. A null label selector matches no
              objects.   If `spec.serviceMonitorSelector`,
              `spec.podMonitorSelector`, `spec.probeSelector` and
              `spec.scrapeConfigSelector` are null, the Prometheus configuration
              is unmanaged. The Prometheus operator will ensure that the
              Prometheus configuration's Secret exists, but it is the
              responsibility of the user to provide the raw gzipped Prometheus
              configuration under the `prometheus.yaml.gz` key. This behavior is
              *deprecated* and will be removed in the next major version of the
              custom resource definition. It is recommended to use
              `spec.additionalScrapeConfigs` instead.   Note that the
              ScrapeConfig custom resource definition is currently at Alpha
              level.

            scrape_interval (str): Interval between consecutive scrapes.   Default: "30s"

            scrape_protocols (List[Any]): The protocols to negotiate during a scrape. It tells clients the
              protocols supported by Prometheus in order of preference (from
              most to least preferred).   If unset, Prometheus uses its default
              value.   It requires Prometheus >= v2.49.0.

            scrape_timeout (str): Number of seconds to wait until a scrape request times out.

            secrets (List[Any]): Secrets is a list of Secrets in the same namespace as the Prometheus
              object, which shall be mounted into the Prometheus Pods. Each
              Secret is added to the StatefulSet definition as a volume named
              `secret-<secret-name>`. The Secrets are mounted into
              /etc/prometheus/secrets/<secret-name> in the 'prometheus'
              container.

            security_context (Dict[str, Any]): SecurityContext holds pod-level security attributes and common
              container settings. This defaults to the default
              PodSecurityContext.

            service_account_name (str): ServiceAccountName is the name of the ServiceAccount to use to run the
              Prometheus Pods.

            service_monitor_namespace_selector (Dict[str, Any]): Namespaces to match for ServicedMonitors discovery. An empty label
              selector matches all namespaces. A null label selector (default
              value) matches the current namespace only.

            service_monitor_selector (Dict[str, Any]): ServiceMonitors to be selected for target discovery. An empty label
              selector matches all objects. A null label selector matches no
              objects.   If `spec.serviceMonitorSelector`,
              `spec.podMonitorSelector`, `spec.probeSelector` and
              `spec.scrapeConfigSelector` are null, the Prometheus configuration
              is unmanaged. The Prometheus operator will ensure that the
              Prometheus configuration's Secret exists, but it is the
              responsibility of the user to provide the raw gzipped Prometheus
              configuration under the `prometheus.yaml.gz` key. This behavior is
              *deprecated* and will be removed in the next major version of the
              custom resource definition. It is recommended to use
              `spec.additionalScrapeConfigs` instead.

            sha (str): Deprecated: use 'spec.image' instead. The image's digest can be
              specified as part of the image name.

            shards (int): Number of shards to distribute targets onto. `spec.replicas`
              multiplied by `spec.shards` is the total number of Pods created.
              Note that scaling down shards will not reshard data onto remaining
              instances, it must be manually moved. Increasing shards will not
              reshard data either but it will continue to be available from the
              same instances. To query globally, use Thanos sidecar and Thanos
              querier or remote write data to a central location.   Sharding is
              performed on the content of the `__address__` target meta-label
              for PodMonitors and ServiceMonitors and `__param_target__` for
              Probes.   Default: 1

            storage (Dict[str, Any]): Storage defines the storage used by Prometheus.

            tag (str): Deprecated: use 'spec.image' instead. The image's tag can be specified
              as part of the image name.

            target_limit (int): TargetLimit defines a limit on the number of scraped targets that will
              be accepted. Only valid in Prometheus versions 2.45.0 and newer.
              Note that the global limit only applies to scrape objects that
              don't specify an explicit limit value. If you want to enforce a
              maximum limit for all scrape objects, refer to
              enforcedTargetLimit.

            thanos (Dict[str, Any]): Defines the configuration of the optional Thanos sidecar.

            tolerations (List[Any]): Defines the Pods' tolerations if specified.

            topology_spread_constraints (List[Any]): Defines the pod's topology spread constraints if specified.

            tracing_config (Dict[str, Any]): TracingConfig configures tracing in Prometheus.   This is an
              *experimental feature*, it may change in any upcoming release in a
              breaking way.

            tsdb (Dict[str, Any]): Defines the runtime reloadable configuration of the timeseries
              database (TSDB).

            version (str): Version of Prometheus being deployed. The operator uses this
              information to generate the Prometheus StatefulSet + configuration
              files.   If not specified, the operator assumes the latest
              upstream version of Prometheus available at the time when the
              version of the operator was released.

            volume_mounts (List[Any]): VolumeMounts allows the configuration of additional VolumeMounts.
              VolumeMounts will be appended to other VolumeMounts in the
              'prometheus' container, that are generated as a result of
              StorageSpec objects.

            volumes (List[Any]): Volumes allows the configuration of additional volumes on the output
              StatefulSet definition. Volumes specified will be appended to
              other volumes that are generated as a result of StorageSpec
              objects.

            wal_compression (bool): Configures compression of the write-ahead log (WAL) using Snappy.
              WAL compression is enabled by default for Prometheus >= 2.20.0
              Requires Prometheus v2.11.0 and above.

            web (Dict[str, Any]): Defines the configuration of the Prometheus web server.

        """
        super().__init__(**kwargs)

        self.additional_alert_manager_configs = additional_alert_manager_configs
        self.additional_alert_relabel_configs = additional_alert_relabel_configs
        self.additional_args = additional_args
        self.additional_scrape_configs = additional_scrape_configs
        self.affinity = affinity
        self.alerting = alerting
        self.allow_overlapping_blocks = allow_overlapping_blocks
        self.apiserver_config = apiserver_config
        self.arbitrary_fs_access_through_sms = arbitrary_fs_access_through_sms
        self.automount_service_account_token = automount_service_account_token
        self.base_image = base_image
        self.body_size_limit = body_size_limit
        self.config_maps = config_maps
        self.containers = containers
        self.disable_compaction = disable_compaction
        self.enable_admin_api = enable_admin_api
        self.enable_features = enable_features
        self.enable_remote_write_receiver = enable_remote_write_receiver
        self.enforced_body_size_limit = enforced_body_size_limit
        self.enforced_keep_dropped_targets = enforced_keep_dropped_targets
        self.enforced_label_limit = enforced_label_limit
        self.enforced_label_name_length_limit = enforced_label_name_length_limit
        self.enforced_label_value_length_limit = enforced_label_value_length_limit
        self.enforced_namespace_label = enforced_namespace_label
        self.enforced_sample_limit = enforced_sample_limit
        self.enforced_target_limit = enforced_target_limit
        self.evaluation_interval = evaluation_interval
        self.excluded_from_enforcement = excluded_from_enforcement
        self.exemplars = exemplars
        self.external_labels = external_labels
        self.external_url = external_url
        self.host_aliases = host_aliases
        self.host_network = host_network
        self.ignore_namespace_selectors = ignore_namespace_selectors
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.init_containers = init_containers
        self.keep_dropped_targets = keep_dropped_targets
        self.label_limit = label_limit
        self.label_name_length_limit = label_name_length_limit
        self.label_value_length_limit = label_value_length_limit
        self.listen_local = listen_local
        self.log_format = log_format
        self.log_level = log_level
        self.maximum_startup_duration_seconds = maximum_startup_duration_seconds
        self.min_ready_seconds = min_ready_seconds
        self.node_selector = node_selector
        self.override_honor_labels = override_honor_labels
        self.override_honor_timestamps = override_honor_timestamps
        self.paused = paused
        self.persistent_volume_claim_retention_policy = persistent_volume_claim_retention_policy
        self.pod_metadata = pod_metadata
        self.pod_monitor_namespace_selector = pod_monitor_namespace_selector
        self.pod_monitor_selector = pod_monitor_selector
        self.pod_target_labels = pod_target_labels
        self.port_name = port_name
        self.priority_class_name = priority_class_name
        self.probe_namespace_selector = probe_namespace_selector
        self.probe_selector = probe_selector
        self.prometheus_external_label_name = prometheus_external_label_name
        self.prometheus_rules_excluded_from_enforce = prometheus_rules_excluded_from_enforce
        self.query = query
        self.query_log_file = query_log_file
        self.reload_strategy = reload_strategy
        self.remote_read = remote_read
        self.remote_write = remote_write
        self.replica_external_label_name = replica_external_label_name
        self.replicas = replicas
        self.resources = resources
        self.retention = retention
        self.retention_size = retention_size
        self.route_prefix = route_prefix
        self.rule_namespace_selector = rule_namespace_selector
        self.rule_selector = rule_selector
        self.rules = rules
        self.sample_limit = sample_limit
        self.scrape_classes = scrape_classes
        self.scrape_config_namespace_selector = scrape_config_namespace_selector
        self.scrape_config_selector = scrape_config_selector
        self.scrape_interval = scrape_interval
        self.scrape_protocols = scrape_protocols
        self.scrape_timeout = scrape_timeout
        self.secrets = secrets
        self.security_context = security_context
        self.service_account_name = service_account_name
        self.service_monitor_namespace_selector = service_monitor_namespace_selector
        self.service_monitor_selector = service_monitor_selector
        self.sha = sha
        self.shards = shards
        self.storage = storage
        self.tag = tag
        self.target_limit = target_limit
        self.thanos = thanos
        self.tolerations = tolerations
        self.topology_spread_constraints = topology_spread_constraints
        self.tracing_config = tracing_config
        self.tsdb = tsdb
        self.version = version
        self.volume_mounts = volume_mounts
        self.volumes = volumes
        self.wal_compression = wal_compression
        self.web = web

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.additional_alert_manager_configs:
                _spec["additionalAlertManagerConfigs"] = self.additional_alert_manager_configs

            if self.additional_alert_relabel_configs:
                _spec["additionalAlertRelabelConfigs"] = self.additional_alert_relabel_configs

            if self.additional_args:
                _spec["additionalArgs"] = self.additional_args

            if self.additional_scrape_configs:
                _spec["additionalScrapeConfigs"] = self.additional_scrape_configs

            if self.affinity:
                _spec["affinity"] = self.affinity

            if self.alerting:
                _spec["alerting"] = self.alerting

            if self.allow_overlapping_blocks is not None:
                _spec["allowOverlappingBlocks"] = self.allow_overlapping_blocks

            if self.apiserver_config:
                _spec["apiserverConfig"] = self.apiserver_config

            if self.arbitrary_fs_access_through_sms:
                _spec["arbitraryFSAccessThroughSMs"] = self.arbitrary_fs_access_through_sms

            if self.automount_service_account_token is not None:
                _spec["automountServiceAccountToken"] = self.automount_service_account_token

            if self.base_image:
                _spec["baseImage"] = self.base_image

            if self.body_size_limit:
                _spec["bodySizeLimit"] = self.body_size_limit

            if self.config_maps:
                _spec["configMaps"] = self.config_maps

            if self.containers:
                _spec["containers"] = self.containers

            if self.disable_compaction is not None:
                _spec["disableCompaction"] = self.disable_compaction

            if self.enable_admin_api is not None:
                _spec["enableAdminAPI"] = self.enable_admin_api

            if self.enable_features:
                _spec["enableFeatures"] = self.enable_features

            if self.enable_remote_write_receiver is not None:
                _spec["enableRemoteWriteReceiver"] = self.enable_remote_write_receiver

            if self.enforced_body_size_limit:
                _spec["enforcedBodySizeLimit"] = self.enforced_body_size_limit

            if self.enforced_keep_dropped_targets:
                _spec["enforcedKeepDroppedTargets"] = self.enforced_keep_dropped_targets

            if self.enforced_label_limit:
                _spec["enforcedLabelLimit"] = self.enforced_label_limit

            if self.enforced_label_name_length_limit:
                _spec["enforcedLabelNameLengthLimit"] = self.enforced_label_name_length_limit

            if self.enforced_label_value_length_limit:
                _spec["enforcedLabelValueLengthLimit"] = self.enforced_label_value_length_limit

            if self.enforced_namespace_label:
                _spec["enforcedNamespaceLabel"] = self.enforced_namespace_label

            if self.enforced_sample_limit:
                _spec["enforcedSampleLimit"] = self.enforced_sample_limit

            if self.enforced_target_limit:
                _spec["enforcedTargetLimit"] = self.enforced_target_limit

            if self.evaluation_interval:
                _spec["evaluationInterval"] = self.evaluation_interval

            if self.excluded_from_enforcement:
                _spec["excludedFromEnforcement"] = self.excluded_from_enforcement

            if self.exemplars:
                _spec["exemplars"] = self.exemplars

            if self.external_labels:
                _spec["externalLabels"] = self.external_labels

            if self.external_url:
                _spec["externalUrl"] = self.external_url

            if self.host_aliases:
                _spec["hostAliases"] = self.host_aliases

            if self.host_network is not None:
                _spec["hostNetwork"] = self.host_network

            if self.ignore_namespace_selectors is not None:
                _spec["ignoreNamespaceSelectors"] = self.ignore_namespace_selectors

            if self.image:
                _spec["image"] = self.image

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.image_pull_secrets:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.init_containers:
                _spec["initContainers"] = self.init_containers

            if self.keep_dropped_targets:
                _spec["keepDroppedTargets"] = self.keep_dropped_targets

            if self.label_limit:
                _spec["labelLimit"] = self.label_limit

            if self.label_name_length_limit:
                _spec["labelNameLengthLimit"] = self.label_name_length_limit

            if self.label_value_length_limit:
                _spec["labelValueLengthLimit"] = self.label_value_length_limit

            if self.listen_local is not None:
                _spec["listenLocal"] = self.listen_local

            if self.log_format:
                _spec["logFormat"] = self.log_format

            if self.log_level:
                _spec["logLevel"] = self.log_level

            if self.maximum_startup_duration_seconds:
                _spec["maximumStartupDurationSeconds"] = self.maximum_startup_duration_seconds

            if self.min_ready_seconds:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.override_honor_labels is not None:
                _spec["overrideHonorLabels"] = self.override_honor_labels

            if self.override_honor_timestamps is not None:
                _spec["overrideHonorTimestamps"] = self.override_honor_timestamps

            if self.paused is not None:
                _spec["paused"] = self.paused

            if self.persistent_volume_claim_retention_policy:
                _spec["persistentVolumeClaimRetentionPolicy"] = self.persistent_volume_claim_retention_policy

            if self.pod_metadata:
                _spec["podMetadata"] = self.pod_metadata

            if self.pod_monitor_namespace_selector:
                _spec["podMonitorNamespaceSelector"] = self.pod_monitor_namespace_selector

            if self.pod_monitor_selector:
                _spec["podMonitorSelector"] = self.pod_monitor_selector

            if self.pod_target_labels:
                _spec["podTargetLabels"] = self.pod_target_labels

            if self.port_name:
                _spec["portName"] = self.port_name

            if self.priority_class_name:
                _spec["priorityClassName"] = self.priority_class_name

            if self.probe_namespace_selector:
                _spec["probeNamespaceSelector"] = self.probe_namespace_selector

            if self.probe_selector:
                _spec["probeSelector"] = self.probe_selector

            if self.prometheus_external_label_name:
                _spec["prometheusExternalLabelName"] = self.prometheus_external_label_name

            if self.prometheus_rules_excluded_from_enforce:
                _spec["prometheusRulesExcludedFromEnforce"] = self.prometheus_rules_excluded_from_enforce

            if self.query:
                _spec["query"] = self.query

            if self.query_log_file:
                _spec["queryLogFile"] = self.query_log_file

            if self.reload_strategy:
                _spec["reloadStrategy"] = self.reload_strategy

            if self.remote_read:
                _spec["remoteRead"] = self.remote_read

            if self.remote_write:
                _spec["remoteWrite"] = self.remote_write

            if self.replica_external_label_name:
                _spec["replicaExternalLabelName"] = self.replica_external_label_name

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.resources:
                _spec["resources"] = self.resources

            if self.retention:
                _spec["retention"] = self.retention

            if self.retention_size:
                _spec["retentionSize"] = self.retention_size

            if self.route_prefix:
                _spec["routePrefix"] = self.route_prefix

            if self.rule_namespace_selector:
                _spec["ruleNamespaceSelector"] = self.rule_namespace_selector

            if self.rule_selector:
                _spec["ruleSelector"] = self.rule_selector

            if self.rules:
                _spec["rules"] = self.rules

            if self.sample_limit:
                _spec["sampleLimit"] = self.sample_limit

            if self.scrape_classes:
                _spec["scrapeClasses"] = self.scrape_classes

            if self.scrape_config_namespace_selector:
                _spec["scrapeConfigNamespaceSelector"] = self.scrape_config_namespace_selector

            if self.scrape_config_selector:
                _spec["scrapeConfigSelector"] = self.scrape_config_selector

            if self.scrape_interval:
                _spec["scrapeInterval"] = self.scrape_interval

            if self.scrape_protocols:
                _spec["scrapeProtocols"] = self.scrape_protocols

            if self.scrape_timeout:
                _spec["scrapeTimeout"] = self.scrape_timeout

            if self.secrets:
                _spec["secrets"] = self.secrets

            if self.security_context:
                _spec["securityContext"] = self.security_context

            if self.service_account_name:
                _spec["serviceAccountName"] = self.service_account_name

            if self.service_monitor_namespace_selector:
                _spec["serviceMonitorNamespaceSelector"] = self.service_monitor_namespace_selector

            if self.service_monitor_selector:
                _spec["serviceMonitorSelector"] = self.service_monitor_selector

            if self.sha:
                _spec["sha"] = self.sha

            if self.shards:
                _spec["shards"] = self.shards

            if self.storage:
                _spec["storage"] = self.storage

            if self.tag:
                _spec["tag"] = self.tag

            if self.target_limit:
                _spec["targetLimit"] = self.target_limit

            if self.thanos:
                _spec["thanos"] = self.thanos

            if self.tolerations:
                _spec["tolerations"] = self.tolerations

            if self.topology_spread_constraints:
                _spec["topologySpreadConstraints"] = self.topology_spread_constraints

            if self.tracing_config:
                _spec["tracingConfig"] = self.tracing_config

            if self.tsdb:
                _spec["tsdb"] = self.tsdb

            if self.version:
                _spec["version"] = self.version

            if self.volume_mounts:
                _spec["volumeMounts"] = self.volume_mounts

            if self.volumes:
                _spec["volumes"] = self.volumes

            if self.wal_compression is not None:
                _spec["walCompression"] = self.wal_compression

            if self.web:
                _spec["web"] = self.web

    # End of generated code
